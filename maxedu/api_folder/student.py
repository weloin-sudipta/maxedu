import frappe

@frappe.whitelist()
def get_student_group():
    user = frappe.session.user

    student = frappe.get_doc("Student", {"user": user})
    student_id = student.name

    student_groups = frappe.get_all(
        "Student Group Student",
        filters={"student": student_id},
        fields=["parent"]
    )

    return student_groups

@frappe.whitelist(allow_guest=True)
def get_student_by_institute():
    teacher_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    institute_name = frappe.db.get_value(
        "Instructor",
        {"instructor_name": teacher_name},
        "institute"
    )
    students = frappe.get_all("Student", filters={"institute": institute_name}, fields=["name"])
    
    # Extract list of student names from the array
    student_names = [s["name"] for s in students]
    
    programmes = frappe.get_all(
        "Program Enrollment",
        filters={"student": ["in", student_names]},
        fields="*"
    )
    return programmes
   
    