import frappe

@frappe.whitelist()
def get_my_profile():
    user = frappe.get_doc("Instructor",{"instructor_email":frappe.session.user})
    teacher = frappe.get_doc("User",{"email":frappe.session.user})
    return {
        "user": user,
        "teacher": teacher
    }