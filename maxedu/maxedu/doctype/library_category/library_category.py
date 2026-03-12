import frappe
from frappe.model.document import Document

class LibraryCategory(Document):

    def validate(self):
        self.category_name = self.category_name.strip()