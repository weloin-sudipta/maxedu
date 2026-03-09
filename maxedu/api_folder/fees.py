import frappe

# @frappe.whitelist()
# def get_my_fee():
#     student = frappe.get_doc("Student",{"student_email_id",frappe.session.user})
#     course = frappe.get_doc("Program Enrollment",{"student",student.name})
#     return course.fees

@frappe.whitelist()
def get_my_fee():
    student = frappe.get_doc("Student", {"student_email_id": frappe.session.user})
    fees = frappe.get_doc("Fees", {"student": student.name})

    components_list = []

    for component in fees.get("components"):
        components_list.append({
            "fees_category": component.get("fees_category") or None,
            "amount": component.get("amount") or 0
        })

    return {
        "feesId": fees.name or None,
        "program": fees.get("program") or None,
        "currency": fees.get("currency") or None,
        "total_fees": fees.get("grand_total") or 0,
        "due_date": fees.get("due_date") or None,
        "grand_total_in_words": fees.get("grand_total_in_words") or None,
        "outstanding_amount": fees.get("outstanding_amount") or 0,
        "student_name": student.get("student_name") or None,
        "components": components_list
    }