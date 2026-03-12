# Copyright (c) 2026, Maxedu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryMember(Document):

    def before_insert(self):
        if not self.library_id:
            self.library_id = self.generate_library_id()
            self.name = self.library_id

    def generate_library_id(self):
        prefix_map = {
            "Student": "LIB-STU-",
            "Instructor": "LIB-TCH-",
            "Staff": "LIB-STF-"
        }
        prefix = prefix_map.get(self.member_type)
        if not prefix:
            frappe.throw(f"Invalid member type: {self.member_type}")

        # Find the max existing ID for this prefix
        last_id = frappe.db.sql(
            """SELECT library_id FROM `tabLibrary Member`
               WHERE library_id LIKE %s
               ORDER BY library_id DESC LIMIT 1""",
            (prefix + "%",),
            as_dict=True
        )

        if last_id and last_id[0].library_id:
            # Extract the numeric part and increment
            last_num = int(last_id[0].library_id.replace(prefix, ""))
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"
