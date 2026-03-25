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
   return frappe.get_all("Student",fields="*")
   
    