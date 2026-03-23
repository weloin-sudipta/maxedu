import frappe


def after_install():
    setup_custom_doctypes()
    create_student_custom_fields()
    create_programme_custom_fields()
    create_roles()


def setup_custom_doctypes():
    frappe.reload_doc("maxedu", "doctype", "student_assignment")
    frappe.reload_doc("maxedu", "doctype", "study_material")
    frappe.reload_doc("maxedu", "doctype", "institute")
    frappe.reload_doc("education", "doctype", "program")


def create_student_custom_fields():
    fields = [
        {
            "fieldname": "caste",
            "label": "Caste",
            "fieldtype": "Data",
            "insert_after": "nationality"
        },
        {
            "fieldname": "religion",
            "label": "Religion",
            "fieldtype": "Data",
            "insert_after": "blood_group"
        },
        {
            "fieldname": "parent_mobile_number",
            "label": "Parent Mobile Number",
            "fieldtype": "Data",
            "insert_after": "student_mobile_number"
        },
        {
            "fieldname": "hostel_facility",
            "label": "Hostel Facility",
            "fieldtype": "Select",
            "options": "Yes\nNo",
            "insert_after": "pincode"
        },
    ]

    for field in fields:
        if not frappe.db.exists(
            "Custom Field",
            {"dt": "Student", "fieldname": field["fieldname"]}
        ):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Student",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()


def create_programme_custom_fields():
    fields = [
        {
            "fieldname": "institute",
            "label": "Institute",
            "fieldtype": "Link",
            "options": "Institute",
            "insert_after": "program_name",
            "in_list_view": 1,
            "reqd":1,
            "in_standard_filter": 1
        }
    ]

    for field in fields:
        if not frappe.db.exists(
            "Custom Field",
            {"dt": "Program", "fieldname": field["fieldname"]}
        ):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Program",
                **field
            }).insert(ignore_permissions=True)

    frappe.db.commit()


def create_roles():
    roles = ["Librarian"]

    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            role = frappe.new_doc("Role")
            role.role_name = role_name
            role.insert(ignore_permissions=True)

    frappe.db.commit()