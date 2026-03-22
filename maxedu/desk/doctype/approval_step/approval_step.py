import frappe
from frappe.model.document import Document

class ApprovalStep(Document):
    def validate(self):
        if self.approved_by == "User" and not self.user:
            frappe.throw("Please select a User")

        if self.approved_by == "Role" and not self.role:
            frappe.throw("Please select a Role")
