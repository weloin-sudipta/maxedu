import frappe
from frappe import _

def create_user_for_instructor(doc, method=None):
    """
    Called before_save of Instructor.
    Creates a User record if it doesn't exist and links it to the Instructor.
    Requires 'instructor_email' and 'user' custom fields on Instructor doctype.
    """
    instructor_email = getattr(doc, "instructor_email", None)
    if not instructor_email:
        return

    existing_user = getattr(doc, "user", None)
    if existing_user:
        return

    # Check if User already exists with this email
    user_name = frappe.db.get_value("User", {"email": instructor_email}, "name")

    if not user_name:
        # Create a new User
        name_parts = (doc.instructor_name or "").strip().split(" ")
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = frappe.get_doc({
            "doctype": "User",
            "email": instructor_email,
            "first_name": first_name,
            "last_name": last_name,
            "send_welcome_email": 1,
            "user_type": "System User",
            "institute": getattr(doc, "institute", None),
            "roles": [{"role": "Instructor"}]
        })
        user.insert(ignore_permissions=True)
        user_name = user.name

    doc.user = user_name
