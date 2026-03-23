import frappe
from frappe.model.document import Document
# import re

class FormField(Document):
    pass
#     def before_insert(self):
#         if not self.field_name and self.field_label:
#             self.field_name = self.generate_fieldname(self.field_label)

#     def validate(self):
#         if self.field_label and not self.field_name:
#             self.field_name = self.generate_fieldname(self.field_label)

#     def generate_fieldname(self, label):
#         fieldname = label.lower()
#         fieldname = re.sub(r'[^a-z0-9 ]', '', fieldname)
#         fieldname = re.sub(r'\s+', '_', fieldname)
#         return fieldname
