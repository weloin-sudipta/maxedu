import frappe
from frappe.model.document import Document


class LibraryBookInventory(Document):

    def before_insert(self):
        if not self.added_by:
            self.added_by = frappe.session.user

    def before_save(self):
        # For Physical copies, sync available_copies on first save
        if self.copy_type == "Physical" and self.is_new():
            self.available_copies = self.total_copies

    def validate(self):
        if self.copy_type == "Physical":
            if (self.total_copies or 0) < 0:
                frappe.throw("Total Copies cannot be negative.")
            if (self.available_copies or 0) > (self.total_copies or 0):
                frappe.throw("Available copies cannot be greater than total copies.")
            if self.fine_per_day and (self.fine_per_day < 0):
                frappe.throw("Fine per day cannot be negative.")
        if self.copy_type == "Online" and not self.ebook_file:
            frappe.msgprint(
                "Tip: Please attach the eBook file for online copies.",
                alert=True
            )