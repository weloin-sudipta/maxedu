import frappe
from frappe.model.document import Document


class LibraryStaff(Document):

    def before_insert(self):
        if not self.staff_id:
            self.staff_id = self.generate_staff_id()
            self.name = self.staff_id

    def generate_staff_id(self):
        prefix = "LIB-EMP-"

        last_id = frappe.db.sql(
            """SELECT staff_id FROM `tabLibrary Staff`
               WHERE staff_id LIKE %s
               ORDER BY staff_id DESC LIMIT 1""",
            (prefix + "%",),
            as_dict=True
        )

        if last_id and last_id[0].staff_id:
            last_num = int(last_id[0].staff_id.replace(prefix, ""))
            new_num = last_num + 1
        else:
            new_num = 1

        return f"{prefix}{new_num:03d}"