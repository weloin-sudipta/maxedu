import frappe
from frappe.utils import getdate, today, get_link_to_form


def get_student_from_user():
    user = frappe.session.user

    student = frappe.db.get_value(
        "Student",
        {"student_email_id": user},
        "name"
    )
    return student

@frappe.whitelist()
def get_assignments():
    student = get_student_from_user()
    if not student:
        return []

    assignments = frappe.get_all(
        "Student Assignment",
        filters={"student": student},
        fields=[
            "name",
            "title",
            "course",
            "topic",
            "due_date",
            "status",
            "difficulty",
            "assignment_file",
            "submission_file",
            "evaluated_score",
            "remarks",
        ],
        order_by="due_date desc",
    )

    for a in assignments:
        if a.get("course"):
            course_name = frappe.db.get_value("Course", a["course"], "course_name")
            a["course_name"] = course_name or a["course"]
        if a.get("topic"):
            topic_name = frappe.db.get_value("Topic", a["topic"], "topic_name")
            a["topic_name"] = topic_name or a["topic"]

        if a["status"] == "Active" and a.get("due_date") and getdate(a["due_date"]) < getdate(today()):
            a["status"] = "Overdue"

    return assignments


@frappe.whitelist()
def submit_assignment(assignment_name, submission_file=None):
    student = get_student_from_user()
    if not student:
        return {"error": "Student not found"}

    doc = frappe.get_doc("Student Assignment", assignment_name)
    if doc.student != student:
        frappe.throw("You can only submit your own assignments")

    doc.status = "Submitted"
    if submission_file:
        doc.submission_file = submission_file
    doc.save(ignore_permissions=True)

    return {"status": "success", "message": "Assignment submitted successfully"}


@frappe.whitelist()
def get_instructor_courses():
    full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    instructor = frappe.db.get_value("Instructor", {"name": full_name}, "name")
    if not instructor:
        return []
    
    # Use Course Schedule to get courses for the instructor
    courses = frappe.db.sql("""
        SELECT DISTINCT course as name, course as course_name
        FROM `tabCourse Schedule`
        WHERE instructor = %s
    """, (instructor,), as_dict=True)
    
    return courses


@frappe.whitelist()
def get_instructor_student_groups(course=None):
    full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    instructor = frappe.db.get_value("Instructor", {"name": full_name}, "name")
    if not instructor:
        return []
    
    # Use Course Schedule to get student groups for this instructor
    sql = """
        SELECT DISTINCT student_group as name, student_group as student_group_name, course
        FROM `tabCourse Schedule`
        WHERE instructor = %s
    """
    params = [instructor]
    
    if course:
        sql += " AND course = %s"
        params.append(course)
        
    groups = frappe.db.sql(sql, tuple(params), as_dict=True)
    return [g for g in groups if g.get("name")]


@frappe.whitelist()
def get_instructor_assignment_templates(course=None):
    full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    instructor = frappe.db.get_value("Instructor", {"name": full_name}, "name")
    if not instructor:
        return []
    
    filters = {"instructor": instructor}
    if course:
        filters["course"] = course
        
    templates = frappe.get_all("Assignment Template",
        filters=filters,
        fields=[
            "name", "title", "course", "topic", "due_date", 
            "status", "assign_to", "student_group", "difficulty", "description"
        ],
        order_by="creation desc"
    )
    
    for t in templates:
        # Get submission stats
        stats = frappe.db.sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Submitted' THEN 1 ELSE 0 END) as submitted,
                SUM(CASE WHEN status = 'Evaluated' THEN 1 ELSE 0 END) as evaluated
            FROM `tabStudent Assignment`
            WHERE assignment_template = %s
        """, (t.name,), as_dict=True)[0]
        t.stats = stats
        
        if t.course:
            t.course_name = frappe.db.get_value("Course", t.course, "course_name")
            
    return templates


@frappe.whitelist()
def create_assignment_template(data):
    if isinstance(data, str):
        import json
        data = json.loads(data)
        
    doc = frappe.get_doc({
        "doctype": "Assignment Template",
        **data
    })
    doc.insert()
    return doc.name


@frappe.whitelist()
def publish_assignment_template(template_name):
    template = frappe.get_doc("Assignment Template", template_name)
    if template.status == "Published":
        return {"status": "info", "message": "Already published"}
        
    if template.assign_to == "Student Group":
        students = frappe.get_all("Student Group Student",
            filters={"parent": template.student_group},
            fields=["student"]
        )
    else:
        # Use Course Enrollment - more direct and reliable
        students = frappe.get_all("Course Enrollment",
            filters={"course": template.course},
            fields=["student"]
        )
    
    created_count = 0
    for s in students:
        # Avoid duplicates
        if not frappe.db.exists("Student Assignment", {
            "student": s.student,
            "assignment_template": template.name
        }):
            new_assign = frappe.get_doc({
                "doctype": "Student Assignment",
                "title": template.title,
                "course": template.course,
                "topic": template.topic,
                "description": template.description,
                "assignment_file": template.assignment_file,
                "due_date": template.due_date,
                "difficulty": template.difficulty,
                "student": s.student,
                "assignment_template": template.name,
                "status": "Active"
            })
            new_assign.insert(ignore_permissions=True)
            created_count += 1
            
    template.status = "Published"
    template.save()
    
    return {
        "status": "success", 
        "message": f"Published to {created_count} students",
        "created_count": created_count
    }


@frappe.whitelist()
def grade_assignment(assignment_name, score, remarks=None):
    doc = frappe.get_doc("Student Assignment", assignment_name)
    doc.evaluated_score = score
    if remarks:
        doc.remarks = remarks
    doc.status = "Evaluated"
    doc.save(ignore_permissions=True)
    return {"status": "success"}


@frappe.whitelist()
def get_template_submissions(template_name):
    submissions = frappe.get_all("Student Assignment",
        filters={"assignment_template": template_name},
        fields=[
            "name", "student", "student_name", "status", 
            "submission_file", "evaluated_score", "remarks"
        ]
    )
    return submissions


def on_enrollment(doc, method):
    """Event hook for Program Enrollment on_submit"""
    for course_row in doc.get("courses"):
        # Find all Published templates for this course that are 'All Enrolled'
        templates = frappe.get_all("Assignment Template",
            filters={
                "course": course_row.course,
                "status": "Published",
                "assign_to": "All Enrolled"
            },
            fields=["name", "title", "topic", "description", "assignment_file", "due_date", "difficulty"]
        )
        
        for t in templates:
            if not frappe.db.exists("Student Assignment", {
                "student": doc.student,
                "assignment_template": t.name
            }):
                frappe.get_doc({
                    "doctype": "Student Assignment",
                    "title": t.title,
                    "course": course_row.course,
                    "topic": t.topic,
                    "description": t.description,
                    "assignment_file": t.assignment_file,
                    "due_date": t.due_date,
                    "difficulty": t.difficulty,
                    "student": doc.student,
                    "assignment_template": t.name,
                    "status": "Active"
                }).insert(ignore_permissions=True)
