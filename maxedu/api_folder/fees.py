import frappe

@frappe.whitelist()
def get_my_fee():
    student = frappe.get_doc("Student",{"student_email_id",frappe.session.user})
    course = frappe.get_doc("Program Enrollment",{"student",student.name})
    return course.fees