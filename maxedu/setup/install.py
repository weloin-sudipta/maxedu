import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    setup_institute_dependencies()

def setup_institute_dependencies():
    # 1. Create Roles
    roles = ["Institute Admin"]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)

    # 2. Add Custom Fields to Institute
    custom_fields = {
        "Institute": [
            {"fieldname": "institute_picture", "label": "Institute Picture", "fieldtype": "Attach Image", "insert_after": "institute_name"},
            {"fieldname": "details", "label": "Details", "fieldtype": "Text Editor", "insert_after": "status"},
            {"fieldname": "admin", "label": "Institute Admin", "fieldtype": "Link", "options": "User", "insert_after": "listed_by"}
        ],
        "Program": [
            {"fieldname": "institute", "label": "Institute", "fieldtype": "Link", "options": "Institute"}
        ],
        "Course": [
            {"fieldname": "institute", "label": "Institute", "fieldtype": "Link", "options": "Institute"}
        ],
        "Student": [
            {"fieldname": "institute", "label": "Institute", "fieldtype": "Link", "options": "Institute"}
        ],
        "Instructor": [
            {"fieldname": "institute", "label": "Institute", "fieldtype": "Link", "options": "Institute"}
        ],
        "User": [
            {"fieldname": "institute", "label": "Institute", "fieldtype": "Link", "options": "Institute"}
        ]
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    
    # 3. Create testing data
    if not frappe.db.exists("Institute", {"institute_name": "MaxEdu Global Academy"}):
        inst = frappe.get_doc({
            "doctype": "Institute",
            "institute_name": "MaxEdu Global Academy",
            "institute_code": "MAX",
            "details": "A premier institution for global education.",
            "admin": "Administrator",
            "status": "Active"
        })
        inst.insert(ignore_permissions=True)
        inst_name = inst.name
    else:
        inst_name = frappe.db.get_value("Institute", {"institute_name": "MaxEdu Global Academy"}, "name")
        
    # Tag an existing program if any
    programs = frappe.get_all("Program", limit=1)
    if programs:
        frappe.db.set_value("Program", programs[0].name, "institute", inst_name)
        
    courses = frappe.get_all("Course", limit=1)
    if courses:
        frappe.db.set_value("Course", courses[0].name, "institute", inst_name)
    
    frappe.db.commit()
    print("Maxedu Institute Flow Setup After Install Successfully!")