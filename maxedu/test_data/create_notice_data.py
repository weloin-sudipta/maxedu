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

    # Ensure Roles exist
    for role in ["Staff", "Principal", "System Manager"]:
        if not frappe.db.exists("Role", role):
            role_doc = frappe.get_doc({"doctype": "Role", "role_name": role})
            role_doc.insert(ignore_permissions=True)

    # 1. Create Form Fields for Notice
    fields_data = [
        {"field_name": "notice_type", "field_label": "Notice Type", "field_type": "Select", "options": "Notice\nNews"},
        {"field_name": "title", "field_label": "Title", "field_type": "Data"},
        {"field_name": "description", "field_label": "Description", "field_type": "Text"},
        {"field_name": "category", "field_label": "Category", "field_type": "Select", "options": "Event\nAcademics\nLibrary\nAdministration"},
        {"field_name": "is_pinned", "field_label": "Is Pinned", "field_type": "Check"}
    ]
    
    for f in fields_data:
        if not frappe.db.exists("Form Field", {"field_name": f["field_name"]}):
            doc = frappe.get_doc({"doctype": "Form Field", **f})
            doc.insert(ignore_permissions=True)
    
    # 2. Create Form
    if not frappe.db.exists("Form", {"form_name": "Notice & News"}):
        form_doc = frappe.get_doc({
            "doctype": "Form",
            "form_name": "Notice & News",
            "is_active": 1
        })
        form_doc.insert(ignore_permissions=True)
        
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "notice_type"}, "name"), "is_required": 1, "order": 1})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "title"}, "name"), "is_required": 1, "order": 2})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "description"}, "name"), "is_required": 1, "order": 3})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "category"}, "name"), "is_required": 0, "order": 4})
        form_doc.append("fields", {"field": frappe.db.get_value("Form Field", {"field_name": "is_pinned"}, "name"), "is_required": 0, "order": 5})
        form_doc.save(ignore_permissions=True)
    else:
        form_doc = frappe.get_last_doc("Form", {"form_name": "Notice & News"})

    # 3. Create Approval Policy
    if not frappe.db.exists("Approval Policy", {"form": form_doc.name}):
        policy_doc = frappe.get_doc({
            "doctype": "Approval Policy",
            "form": form_doc.name,
            "is_active": 1
        })
        policy_doc.insert(ignore_permissions=True)
        
        policy_doc.append("steps", {"approved_by": "Role", "role": "Principal", "order": 1, "approval_mode": "Any One"})
        policy_doc.append("steps", {"approved_by": "Role", "role": "System Manager", "order": 2, "approval_mode": "Any One"})
        policy_doc.save(ignore_permissions=True)
    else:
        policy_doc = frappe.get_last_doc("Approval Policy", {"form": form_doc.name})

    staff_email = "staff@example.com"
    if not frappe.db.exists("User", staff_email):
        user = frappe.get_doc({"doctype": "User", "email": staff_email, "first_name": "Test Staff", "send_welcome_email": 0})
        user.append("roles", {"role": "Staff"})
        user.flags.ignore_permissions = True
        user.insert()
        
    admin_email = "Administrator" # usually exists

    # Create dummy Notice 1 (Approved, Pinned)
    app1_data = {
        "notice_type": "Notice",
        "title": "Annual Hackathon Announced",
        "description": "The Computer Science dept is hosting a 24-hour hackathon. Register soon!",
        "category": "Event",
        "is_pinned": 1
    }
    app1 = frappe.get_doc({
        "doctype": "Application", "form": form_doc.name, "applicant": staff_email,
        "status": "Approved", "current_step": 3, "data": json.dumps(app1_data)
    }).insert(ignore_permissions=True)
    
    # Create dummy Notice 2 (Approved, Unpinned)
    app2_data = {
        "notice_type": "Notice",
        "title": "Semester Exams Prep",
        "description": "Semester exams will start next month. Course guides have been updated.",
        "category": "Academics",
        "is_pinned": 0
    }
    app2 = frappe.get_doc({
        "doctype": "Application", "form": form_doc.name, "applicant": staff_email,
        "status": "Approved", "current_step": 3, "data": json.dumps(app2_data)
    }).insert(ignore_permissions=True)
    
    # Create dummy News (Approved)
    app3_data = {
        "notice_type": "News",
        "title": "Campus Café Upgrades",
        "description": "We are adding 4 new vendors to the campus café opening next week.",
        "category": "Administration",
        "is_pinned": 0
    }
    app3 = frappe.get_doc({
        "doctype": "Application", "form": form_doc.name, "applicant": staff_email,
        "status": "Approved", "current_step": 3, "data": json.dumps(app3_data)
    }).insert(ignore_permissions=True)
    
    # Create dummy Notice (Pending - shouldn't show)
    app4_data = {
        "notice_type": "Notice",
        "title": "Secret Surprise Party",
        "description": "Don't tell anyone, this is pending approval.",
        "category": "Event",
        "is_pinned": 1
    }
    app4 = frappe.get_doc({
        "doctype": "Application", "form": form_doc.name, "applicant": staff_email,
        "status": "Pending", "current_step": 1, "data": json.dumps(app4_data)
    }).insert(ignore_permissions=True)

    frappe.db.commit()
    print("Test data for Notice & News created properly.")

if __name__ == "__main__":
    create_test_data()
