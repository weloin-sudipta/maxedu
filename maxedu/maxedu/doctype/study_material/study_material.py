import frappe
import os
from frappe.model.document import Document


class StudyMaterial(Document):
    def before_save(self):
        if self.file:
            ext = os.path.splitext(self.file)[1].upper().lstrip(".")
            self.file_type = ext or "FILE"

            file_doc = frappe.get_all(
                "File",
                filters={"file_url": self.file},
                fields=["file_size"],
                limit=1,
            )
            if file_doc:
                size = file_doc[0].file_size
                if size >= 1048576:
                    self.file_size = f"{size / 1048576:.1f} MB"
                else:
                    self.file_size = f"{size / 1024:.0f} KB"
