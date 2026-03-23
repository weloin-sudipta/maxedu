import frappe
from frappe.model.document import Document


class Institute(Document):

    def before_save(self):
        self.set_listed_by()

    def set_listed_by(self):
        if not self.listed_by:
            self.listed_by = frappe.session.user