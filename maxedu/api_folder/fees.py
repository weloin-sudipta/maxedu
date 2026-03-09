import frappe

# @frappe.whitelist()
# def get_my_fee():
#     student = frappe.get_doc("Student",{"student_email_id",frappe.session.user})
#     course = frappe.get_doc("Program Enrollment",{"student",student.name})
#     return course.fees

@frappe.whitelist()
def get_my_fee():
    student = frappe.get_doc("Student", {"student_email_id": frappe.session.user})
    
    fees_list = frappe.get_all("Fees", filters={"student": student.name}, limit_page_length=1)
    
    if not fees_list:
        return {"message": "No fees found for this student", "components": []}

    fees = frappe.get_doc("Fees", fees_list[0].name)
    
    components_list = [
        {"fees_category": c.fees_category, "amount": c.amount} for c in fees.components
    ]
    return {
        "feesId": fees.name,
        "program": fees.program,
        "currency": fees.currency,
        "total_fees": fees.grand_total,
        "due_date": fees.due_date,
        "grand_total_in_words": fees.grand_total_in_words,
        "outstanding_amount": fees.outstanding_amount,
        "student_name": student.student_name,
        "components": components_list
    }