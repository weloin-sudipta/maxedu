import sys
import os
sys.path.insert(0, ".")
import importlib
import frappe
import json
from frappe.utils import nowdate, add_days

def create_test_data():
    frappe.init(site='dev.localhost')
    frappe.connect()

    # Ensure Instructor Role exists
    if not frappe.db.exists("Role", "Instructor"):
        role_doc = frappe.get_doc({"doctype": "Role", "role_name": "Instructor"})
        role_doc.insert(ignore_permissions=True)
        print("Created Role: Instructor")

    # 1. Create Form Fields
    fields_data = [
        {"field_name": "leave_type", "field_label": "Leave Type", "field_type": "Select", "options": "Sick Leave\nCasual Leave"},
        {"field_name": "from_date", "field_label": "From Date", "field_type": "Date"},
        {"field_name": "to_date", "field_label": "To Date", "field_type": "Date"},
        {"field_name": "reason", "field_label": "Reason", "field_type": "Data"}
    ]
    
    for f in fields_data:
        if not frappe.db.exists("Form Field", {"field_name": f["field_name"]}):
            doc = frappe.get_doc({"doctype": "Form Field", **f})
            doc.insert(ignore_permissions=True)
            print(f"Created Form Field: {f['field_name']}")
    
    # 2. Create Form
    if not frappe.db.exists("Form", {"form_name": "Leave Application"}):
        form_doc = frappe.get_doc({
            "doctype": "Form",
            "form_name": "Leave Application",
            "is_active": 1
        })
        form_doc.insert(ignore_permissions=True)
        
        # Add fields
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "leave_type"}, "name"), "is_required": 1, "order": 1})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "from_date"}, "name"), "is_required": 1, "order": 2})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "to_date"}, "name"), "is_required": 1, "order": 3})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "reason"}, "name"), "is_required": 1, "order": 4})
        form_doc.save(ignore_permissions=True)
        print("Created Form: Leave Application")
    else:
        form_doc = frappe.get_last_doc("Form", {"form_name": "Leave Application"})
        print("Form Leave Application already exists")

    # 3. Create Approval Policy
    if not frappe.db.exists("Approval Policy", {"form": form_doc.name}):
        policy_doc = frappe.get_doc({
            "doctype": "Approval Policy",
            "form": form_doc.name,
            "is_active": 1
        })
        policy_doc.insert(ignore_permissions=True)
        
        policy_doc.append("steps", {"approved_by": "Role", "role": "Instructor", "order": 1, "approval_mode": "Any One"})
        policy_doc.append("steps", {"approved_by": "Role", "role": "System Manager", "order": 2, "approval_mode": "Any One"})
        policy_doc.save(ignore_permissions=True)
        print("Created Approval Policy")
    else:
        policy_doc = frappe.get_last_doc("Approval Policy", {"form": form_doc.name})
        print("Approval Policy already exists")

    # 4. Create Application (Student applies)
    student_email = "student@example.com"
    if not frappe.db.exists("User", student_email):
        user = frappe.get_doc({"doctype": "User", "email": student_email, "first_name": "Test Student", "send_welcome_email": 0})
        user.flags.ignore_permissions = True
        user.insert()

    instructor_email = "instructor@example.com"
    if not frappe.db.exists("User", instructor_email):
        user = frappe.get_doc({"doctype": "User", "email": instructor_email, "first_name": "Test Instructor", "send_welcome_email": 0})
        user.append("roles", {"role": "Instructor"})
        user.flags.ignore_permissions = True
        user.insert()
    else:
        user = frappe.get_doc("User", instructor_email)
        if not next((r for r in user.roles if r.role == 'Instructor'), None):
            user.append("roles", {"role": "Instructor"})
            user.save(ignore_permissions=True)

    app_data = {
        "leave_type": "Sick Leave",
        "from_date": nowdate(),
        "to_date": add_days(nowdate(), 2),
        "reason": "Feeling unwell"
    }
    
    app_doc = frappe.get_doc({
        "doctype": "Application",
        "form": form_doc.name,
        "applicant": student_email,
        "status": "Pending",
        "current_step": 1,
        "data": json.dumps(app_data)
    })
    app_doc.flags.ignore_permissions = True
    app_doc.insert()
    print(f"Created Application: {app_doc.name}")

    # 5. Instructor Approves
    log1 = frappe.get_doc({
        "doctype": "Application Approval Log",
        "application": app_doc.name,
        "approver": instructor_email,
        "role": "Instructor",
        "status": "Approved",
        "order": 1
    })
    log1.insert(ignore_permissions=True)
    print("Instructor approved.")
    
    app_doc.current_step = 2
    app_doc.save(ignore_permissions=True)

    # 6. System Manager Approves
    log2 = frappe.get_doc({
        "doctype": "Application Approval Log",
        "application": app_doc.name,
        "approver": "Administrator",
        "role": "System Manager",
        "status": "Approved",
        "order": 2
    })
    log2.insert(ignore_permissions=True)
    print("System Manager approved.")
    
    app_doc.status = "Approved"
    app_doc.approved_by = "Administrator"
    app_doc.save(ignore_permissions=True)
    
    frappe.db.commit()
    print("Data creation complete. Application is Approved.")

if __name__ == "__main__":
    create_test_data()
