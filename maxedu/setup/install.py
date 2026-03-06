import frappe

def after_install():
    create_student_custom_fields()

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
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Student",
                **field
            })

            custom_field.insert(ignore_permissions=True)

    frappe.db.commit()