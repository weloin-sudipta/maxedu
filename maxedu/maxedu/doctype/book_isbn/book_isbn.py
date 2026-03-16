# Copyright (c) 2026
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BookISBN(Document):

    def validate(self):
        """Basic validation for ISBN"""
        if self.isbn:
            self.isbn = self.isbn.strip()

        # Prevent very short ISBN numbers
        if len(self.isbn) < 10:
            frappe.throw("ISBN must be at least 10 characters long.")