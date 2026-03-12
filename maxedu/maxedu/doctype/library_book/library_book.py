import frappe
from frappe.model.document import Document

class LibraryBook(Document):

    def validate(self):

        if self.publication_year:
            if self.publication_year > frappe.utils.now_datetime().year:
                frappe.throw("Publication year cannot be in the future")