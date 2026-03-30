import frappe
from .teacher_greading import get_my_courses, get_my_exams


@frappe.whitelist()
def get_my_profile():
    """Get basic current user info"""
    user_email = frappe.session.user
    
    try:
        instructor = frappe.get_doc("Instructor", {"instructor_email": user_email})
    except:
        return {"error": "Instructor profile not found"}
    
    teacher = frappe.get_doc("User", {"email": user_email})
    
    return {
        "instructor": instructor.as_dict(),
        "user": teacher.as_dict()
    }


@frappe.whitelist()
def get_teacher_dashboard():
    """Get comprehensive teacher dashboard information"""
    user_email = frappe.session.user
    
    try:
        instructor_doc = frappe.get_doc("Instructor", {"instructor_email": user_email})
        instructor_dict = instructor_doc.as_dict()
    except:
        return {"error": "Instructor profile not found"}
    
    # Get instructor logs (courses)
    courses_data = get_my_courses()
    if isinstance(courses_data, dict) and courses_data.get("error"):
        courses_data = None
    
    # Get exams/assessments 
    exams_data = get_my_exams()
    
    # Get student groups
    student_groups = frappe.get_all(
        "Student Group Instructor",
        filters={"instructor": instructor_doc.name},
        fields=["name", "parent"],
        as_list=True
    )
    student_group_ids = [sg[1] for sg in student_groups]
    
    student_groups_list = frappe.get_all(
        "Student Group",
        filters={"name": ["in", student_group_ids]},
        fields=["name", "student_group_name", "program", "academic_year", "academic_term"]
    ) if student_group_ids else []
    
    # Get course schedules
    course_schedules = frappe.get_all(
        "Course Schedule",
        filters={"instructor": instructor_doc.name},
        fields=["name", "course", "course_name", "from_date", "to_date", "department", "student_group_name"],
        order_by="from_date desc",
        limit_page_length=10
    )
    
    # Get statistics
    stats = {
        "total_courses": len(courses_data.get("instructor_log", [])) if courses_data else 0,
        "total_exams": len(exams_data) if exams_data else 0,
        "total_student_groups": len(student_groups_list),
        "total_schedules": len(course_schedules)
    }
    
    return {
        "profile": instructor_dict,
        "courses": courses_data.get("instructor_log", []) if courses_data else [],
        "exams": exams_data or [],
        "student_groups": student_groups_list,
        "course_schedules": course_schedules,
        "statistics": stats
    }


@frappe.whitelist()
def get_teacher_full_info():
    """Get complete teacher information including department, employee details, etc."""
    user_email = frappe.session.user
    
    try:
        instructor_doc = frappe.get_doc("Instructor", {"instructor_email": user_email})
    except:
        return {"error": "Instructor profile not found"}
    
    instructor_dict = instructor_doc.as_dict()
    
    # Get employee info if linked
    employee_info = None
    if instructor_dict.get("employee"):
        employee_info = frappe.get_doc("Employee", instructor_dict["employee"]).as_dict()
    
    # Get department info
    department_info = None
    if instructor_dict.get("department"):
        department_info = frappe.get_doc("Department", instructor_dict["department"]).as_dict()
    
    # Get user info
    user_info = frappe.get_doc("User", {"email": user_email}).as_dict()
    
    # Get institute info
    institute_info = None
    if instructor_dict.get("institute"):
        institute_info = frappe.get_doc("Institute", instructor_dict["institute"]).as_dict()
    
    # Get all courses with full details
    courses_data = get_my_courses()
    courses_with_details = []
    
    if courses_data and not courses_data.get("error"):
        for log in courses_data.get("instructor_log", []):
            course_doc = frappe.get_doc("Course", log["course"]).as_dict()
            courses_with_details.append({
                "course_info": course_doc,
                "program": log.get("program"),
                "academic_year": log.get("academic_year"),
                "academic_term": log.get("academic_term")
            })
    
    # Get activity summary
    assessment_plans = frappe.get_all(
        "Assessment Plan",
        filters={"supervisor": instructor_doc.name},
        fields=["name", "course", "course_name", "start_date", "end_date"],
        order_by="creation desc"
    )
    
    assignments = frappe.get_all(
        "Assignment Template",
        filters={"instructor": instructor_doc.name},
        fields=["name", "title", "course", "due_date"],
        order_by="creation desc",
        limit_page_length=10
    )
    
    return {
        "instructor": instructor_dict,
        "user": user_info,
        "employee": employee_info,
        "department": department_info,
        "institute": institute_info,
        "courses": courses_with_details,
        "assignments": assignments
    }

@frappe.whitelist()
def get_teacher_pending_tasks():
    """Get pending tasks (attendance, mark entry, review) for the dashboard"""
    user_email = frappe.session.user
    from frappe.utils import today, getdate
    
    try:
        instructor_doc = frappe.get_doc("Instructor", {"instructor_email": user_email})
        instructor = instructor_doc.name
    except Exception:
        return {"attendance_pending": [], "mark_entry_pending": [], "review_pending": [], "error": "Instructor not found"}
    
    attendance_pending = []
    mark_entry_pending = []
    review_pending = []
    
    # 1. Attendance Pending
    try:
        # Get course schedules up to today that might not have attendance
        schedules = frappe.get_all(
            "Course Schedule", 
            filters={
                "instructor": instructor,
                "schedule_date": ("<=", today())
            },
            fields=[
                "name", "course", "course_name", "student_group", "schedule_date",
                "from_time", "to_time", "student_group"
            ],
            order_by="schedule_date desc",
            limit=20
        )
        
        for sch in schedules:
            # Check if attendance is already taken (assuming Student Attendance records would exist)
            attendance_count = frappe.db.count("Student Attendance", {"course_schedule": sch.name})
            if attendance_count == 0:
                # Find total students for this group
                total_students = frappe.db.count("Student Group Student", {"parent": sch.student_group}) if sch.student_group else 0
                
                attendance_pending.append({
                    "schedule_id": sch.name,
                    "course_name": sch.course_name or sch.course,
                    "batch": sch.student_group or "N/A",
                    "schedule_date": sch.schedule_date,
                    "start_time": sch.from_time,
                    "end_time": sch.to_time,
                    "total_students": total_students
                })
                
                if len(attendance_pending) >= 5:
                    break
    except Exception as e:
        frappe.log_error(f"Error fetching attendance pending: {str(e)}")
        
    # 2. Mark Entry Pending
    try:
        # In Frappe Education, Assessment Plan has supervisor or we use instructor courses
        assessment_plans = frappe.get_all(
            "Assessment Plan",
            filters={"supervisor": instructor},
            fields=["name", "assessment_name", "course", "academic_term", "schedule_date", "student_group"],
            order_by="schedule_date desc",
            limit=20
        )
        for plan in assessment_plans:
            # Rough estimation of total students enrolled
            total_students = frappe.db.count("Student Group Student", {"parent": plan.student_group}) if plan.student_group else 0
            if total_students == 0 and plan.course:
                total_students = frappe.db.count("Course Enrollment", {"course": plan.course, "academic_term": plan.academic_term})
                
            marks_entered_count = frappe.db.count("Assessment Result", {"assessment_plan": plan.name})
            
            # If not all marks are entered
            if total_students > 0 and marks_entered_count < total_students:
                mark_entry_pending.append({
                    "assessment_id": plan.name,
                    "assessment_title": plan.assessment_name or plan.name,
                    "course": plan.course,
                    "academic_term": plan.academic_term or "N/A",
                    "assessment_date": plan.schedule_date,
                    "total_students": total_students,
                    "marks_entered_count": marks_entered_count,
                    "pending_count": total_students - marks_entered_count
                })
                
                if len(mark_entry_pending) >= 5:
                    break
    except Exception as e:
        frappe.log_error(f"Error fetching mark entry pending: {str(e)}")
        
    # 3. Review Pending
    try:
        # Assuming Maxedu uses 'Assignment Template' and 'Student Assignment'
        templates = frappe.get_all("Assignment Template", filters={"instructor": instructor}, pluck="name")
        if templates:
            submissions = frappe.get_all(
                "Student Assignment",
                filters={
                    "assignment_template": ("in", templates),
                    "status": "Submitted"
                },
                fields=["name", "student_name", "assignment_template", "course", "creation", "title"],
                order_by="creation desc",
                limit=5
            )
            for sub in submissions:
                review_pending.append({
                    "submission_id": sub.name,
                    "student_name": sub.student_name or "Unknown Student",
                    "assignment_title": sub.title or sub.assignment_template,
                    "course": sub.course,
                    "submission_date": sub.creation
                })
    except Exception as e:
        frappe.log_error(f"Error fetching review pending: {str(e)}")
        
    return {
        "success": True,
        "attendance_pending": attendance_pending,
        "mark_entry_pending": mark_entry_pending,
        "review_pending": review_pending
    }