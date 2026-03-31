import frappe
from frappe.utils import nowdate

from .teacher_course import get_course_topics

def get_student_from_user():
    user = frappe.session.user
    students = frappe.get_all("Student", filters={"user": user}, fields=["name"], limit=1)
    if not students:
        students = frappe.get_all(
            "Student",
            filters={"student_email_id": user},
            fields=["name"],
            limit=1,
        )
    return students[0].name if students else None


@frappe.whitelist()
def get_study_materials():
    student = get_student_from_user()
    if not student:
        return []

    enrollments = frappe.get_all(
        "Course Enrollment",
        filters={"student": student},
        fields=["course"],
    )

    if not enrollments:
        return []

    courses = [e.course for e in enrollments]

    materials = frappe.get_all(
        "Study Material",
        filters={"course": ["in", courses]},
        fields=[
            "name",
            "title",
            "course",
            "topic",
            "category",
            "file",
            "file_type",
            "file_size",
            "upload_date",
            "description",
        ],
        order_by="upload_date desc",
    )

    for m in materials:
        # Get course name
        if m.get("course"):
            course_name = frappe.db.get_value("Course", m["course"], "course_name")
            m["course_name"] = course_name or m["course"]
        
        # Get topic name - FIXED: Check if topic exists and get its name
        if m.get("topic"):
            # Try to find topic by name (since you're storing topic name directly)
            topic_doc = frappe.db.get_value("Topic", {"topic_name": m["topic"]}, "topic_name")
            if topic_doc:
                m["topic_name"] = topic_doc
            else:
                # If not found by topic_name, try as document name
                topic_name = frappe.db.get_value("Topic", m["topic"], "topic_name")
                m["topic_name"] = topic_name or m["topic"]
        else:
            m["topic_name"] = None

    return materials

@frappe.whitelist()
def create_study_material():
    try:
        # Get form data
        title = frappe.form_dict.get('title')
        course = frappe.form_dict.get('course')
        topic = frappe.form_dict.get('topic')
        category = frappe.form_dict.get('category')
        upload_date = frappe.form_dict.get('upload_date')
        description = frappe.form_dict.get('description')
        
        # Get the uploaded file
        uploaded_file = frappe.request.files.get('file')
        
        # Validation
        if not title:
            return {"success": False, "message": "Title is required"}
        
        if not course:
            return {"success": False, "message": "Course is required"}
        
        if not uploaded_file:
            return {"success": False, "message": "File is required"}
        
        # Validate course exists
        if not frappe.db.exists("Course", course):
            return {"success": False, "message": f"Course '{course}' does not exist"}
        
        # Handle topic
        topic_name = None
        if topic:
            topic_list = frappe.get_all("Topic", filters={"topic_name": topic}, fields=["name"])
            if topic_list:
                topic_name = topic_list[0].name
            elif frappe.db.exists("Topic", topic):
                topic_name = topic
            else:
                return {"success": False, "message": f"Topic '{topic}' does not exist"}
        
        # Save the file first
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": uploaded_file.filename,
            "folder": "Home/Attachments",
            "is_private": 0,
            "content": uploaded_file.read()
        })
        file_doc.insert()
        
        # Create Study Material with the file URL (to satisfy mandatory field)
        study_material = frappe.get_doc({
            "doctype": "Study Material",
            "title": title,
            "course": course,
            "topic": topic_name,
            "category": category,
            "upload_date": upload_date or nowdate(),
            "description": description,
            "file": file_doc.file_url,  # Now file field has a value
            "file_name": uploaded_file.filename,
            "status": "Active"
        })
        study_material.insert()
        
        # Link file to study material
        file_doc.db_set("attached_to_doctype", "Study Material")
        file_doc.db_set("attached_to_name", study_material.name)
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": "Study material created successfully",
            "data": {
                "name": study_material.name,
                "title": study_material.title,
                "course": study_material.course,
                "topic": study_material.topic,
                "category": study_material.category,
                "file": file_doc.file_url,
                "file_name": uploaded_file.filename,
                "upload_date": str(study_material.upload_date),
                "description": study_material.description,
                "status": study_material.status
            }
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Error creating study material: {str(e)}", "Study Material API")
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def get_materials_by_teacher():
    courses = get_course_topics()

    if not courses:
        return {"success": False, "message": "No courses found for the teacher"}

    course_names = [c.get("course_name") for c in courses if c.get("course_name")]

    materials = frappe.get_all(
        "Study Material",
        filters={"course": ["in", course_names]},
        fields=[
            "name",
            "title",
            "course",
            "topic",
            "category",
            "file",
            "file_type",
            "file_size",
            "upload_date",
            "description",
        ],
        order_by="upload_date desc",
    )

    return {"success": True, "materials": materials}