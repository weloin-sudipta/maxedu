import frappe
from frappe import _

def create_user_for_instructor(doc, method=None):
    """
    Called before_save of Instructor.
    Creates a User record if it doesn't exist and links it to the Instructor.
    """
    if not doc.instructor_email:
        return

    if not doc.user:
        # Check if User already exists with this email
        user_name = frappe.db.get_value("User", {"email": doc.instructor_email}, "name")
        
        if not user_name:
            # Create a new User
            # Split instructor_name into first and last name
            name_parts = doc.instructor_name.strip().split(" ")
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            user = frappe.get_doc({
                "doctype": "User",
                "email": doc.instructor_email,
                "first_name": first_name,
                "last_name": last_name,
                "send_welcome_email": 1,
                "user_type": "System User", # Instructors are typically system users in this context
                "roles": [{"role": "Instructor"}]
            })
            user.insert(ignore_permissions=True)
            user_name = user.name
            
        doc.user = user_name
