import frappe
from maxedu.approval_desk.services import submit_application, approve_step, reject_step

@frappe.whitelist()
def api_submit_application(application_name):
    doc = frappe.get_doc("Application", application_name)
    submit_application(doc)
    return {"status": "success", "message": "Application submitted successfully."}

@frappe.whitelist()
def api_approve_step(application_name):
    approve_step(application_name, frappe.session.user)
    return {"status": "success", "message": "Step approved successfully."}

@frappe.whitelist()
def api_reject_step(application_name):
    reject_step(application_name, frappe.session.user)
    return {"status": "success", "message": "Step rejected successfully."}
