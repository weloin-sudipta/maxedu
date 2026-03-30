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
        "assessment_plans": assessment_plans,
        "assignments": assignments
    }