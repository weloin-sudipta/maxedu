import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class StudentAssignment(Document):
    def before_save(self):
        if self.status == "Active" and self.due_date and getdate(self.due_date) < getdate(today()):
            self.status = "Overdue"
