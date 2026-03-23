import sys
import os
sys.path.insert(0, ".")
import frappe

def create_doctypes():
    frappe.init(site='dev.localhost')
    frappe.connect()

    # Create Child Tables
    def create_child_table(name, fields):
        if not frappe.db.exists("DocType", name):
            frappe.get_doc({
                "doctype": "DocType",
                "name": name,
                "module": "Maxedu",
                "custom": 1,
                "istable": 1,
                "fields": fields
            }).insert(ignore_permissions=True)

    create_child_table("Routine Day", [
        {"fieldname": "day", "label": "Day", "fieldtype": "Select", "options": "Mon\nTue\nWed\nThu\nFri\nSat\nSun", "in_list_view": 1, "reqd": 1}
    ])
    
    create_child_table("Routine Period", [
        {"fieldname": "period", "label": "Period", "fieldtype": "Int", "in_list_view": 1, "reqd": 1}
    ])

    create_child_table("Routine Class", [
        {"fieldname": "student_group", "label": "Student Group", "fieldtype": "Link", "options": "Student Group", "in_list_view": 1, "reqd": 1}
    ])

    create_child_table("Routine Instructor Map", [
        {"fieldname": "instructor", "label": "Instructor", "fieldtype": "Link", "options": "Instructor", "in_list_view": 1, "reqd": 1},
        {"fieldname": "course", "label": "Course", "fieldtype": "Link", "options": "Course", "in_list_view": 1, "reqd": 1}
    ])

    create_child_table("Routine Hard Lock", [
        {"fieldname": "student_group", "label": "Student Group", "fieldtype": "Link", "options": "Student Group", "in_list_view": 1},
        {"fieldname": "day", "label": "Day", "fieldtype": "Select", "options": "Mon\nTue\nWed\nThu\nFri\nSat\nSun", "in_list_view": 1},
        {"fieldname": "period", "label": "Period", "fieldtype": "Int", "in_list_view": 1},
        {"fieldname": "instructor", "label": "Instructor", "fieldtype": "Link", "options": "Instructor", "in_list_view": 1},
        {"fieldname": "course", "label": "Course", "fieldtype": "Link", "options": "Course", "in_list_view": 1}
    ])

    create_child_table("Routine Preference", [
        {"fieldname": "instructor", "label": "Instructor", "fieldtype": "Link", "options": "Instructor", "in_list_view": 1},
        {"fieldname": "student_group", "label": "Student Group", "fieldtype": "Link", "options": "Student Group", "in_list_view": 1},
        {"fieldname": "weight", "label": "Weight", "fieldtype": "Int", "in_list_view": 1, "default": "5"}
    ])

    # Main DocType
    if not frappe.db.exists("DocType", "Routine Generator"):
        frappe.get_doc({
            "doctype": "DocType",
            "name": "Routine Generator",
            "module": "Maxedu",
            "custom": 1,
            "autoname": "format:RT-{YYYY}-{MM}-{####}",
            "fields": [
                {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Draft\nCompleted\nFailed", "default": "Draft", "read_only": 1},
                {"fieldname": "academic_term", "label": "Academic Term", "fieldtype": "Link", "options": "Academic Term"},
                
                {"fieldname": "constants_tab", "label": "Constants", "fieldtype": "Tab Break"},
                {"fieldname": "max_classes_per_instructor_per_day", "label": "Max Classes / Instructor / Day", "fieldtype": "Int", "default": "2"},
                {"fieldname": "max_classes_per_subject_per_day", "label": "Max Classes / Subject / Day", "fieldtype": "Int", "default": "2"},
                {"fieldname": "min_classes_per_instructor_per_week", "label": "Min Classes / Instructor / Week", "fieldtype": "Int", "default": "8"},
                {"fieldname": "max_classes_per_instructor_per_week", "label": "Max Classes / Instructor / Week", "fieldtype": "Int", "default": "12"},

                {"fieldname": "structure_tab", "label": "Structure", "fieldtype": "Tab Break"},
                {"fieldname": "days", "label": "Days", "fieldtype": "Table", "options": "Routine Day"},
                {"fieldname": "periods", "label": "Periods", "fieldtype": "Table", "options": "Routine Period"},
                {"fieldname": "student_groups", "label": "Student Groups", "fieldtype": "Table", "options": "Routine Class"},
                
                {"fieldname": "instructors_tab", "label": "Instructors Mapping", "fieldtype": "Tab Break"},
                {"fieldname": "instructor_map", "label": "Instructor Map", "fieldtype": "Table", "options": "Routine Instructor Map"},

                {"fieldname": "constraints_tab", "label": "Constraints", "fieldtype": "Tab Break"},
                {"fieldname": "hard_locks", "label": "Hard Locks", "fieldtype": "Table", "options": "Routine Hard Lock"},
                {"fieldname": "preferences", "label": "Instructor Preferences (Soft)", "fieldtype": "Table", "options": "Routine Preference"}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Institute Admin", "read": 1, "write": 1, "create": 1, "delete": 1},
                {"role": "Administrator", "read": 1, "write": 1, "create": 1, "delete": 1}
            ]
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Add custom server script for generating the button/action
        server_script_name = "Generate Routine API"
        if not frappe.db.exists("Server Script", server_script_name):
            frappe.get_doc({
                "doctype": "Server Script",
                "name": server_script_name,
                "script_type": "API",
                "api_method": "maxedu.api.generate_routine",
                "allow_guest": 0,
                "script": "import maxedu.api\nmaxedu.api.generate_routine()"
            }).insert(ignore_permissions=True)
            
        frappe.db.commit()
    print("Routine Generator DocTypes bootstrapped.")

if __name__ == "__main__":
    create_doctypes()
