import frappe

@frappe.whitelist()
def get_all_leave_application():
    return frappe.get_all(
        "Student Leave Application",
        fields=["name", "student", "from_date", "to_date", "reason", "workflow_state"],
        order_by="creation desc"
    )