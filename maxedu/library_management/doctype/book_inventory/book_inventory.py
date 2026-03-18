import frappe
from frappe.model.document import Document
from frappe.utils import now

class BookInventory(Document):
    
    def validate(self):
        if self.managed_by:
            roles = frappe.get_roles(self.managed_by)
            if "Librarian" not in roles:
                frappe.throw("Managed By must be a Librarian")
    
    def before_save(self):
        self.last_updated = now()