import frappe

@frappe.whitelist()
def test_working():
    return "working"

# --- Helper functions ---
def user_has_role(role):
    return role in frappe.get_roles(frappe.session.user)

def user_is_guest():
    return frappe.session.user == "Guest"

def get_user_role():
    if user_is_guest():
        return "Guest"
    elif user_has_role("Student"):
        return "Student"
    elif user_has_role("Teacher"):
        return "Teacher"
    elif user_has_role("Parent"):
        return "Parent"
    return None

# --- Main API ---
@frappe.whitelist()
def get_profile():
    if user_has_role("Student"):
        return get_student_profile()
    else:
        return {"error": "Profile information is only available for students."}

# --- Fetch full student profile ---
def get_student_profile():
    user = frappe.session.user
    if user_is_guest():
        return {"error": "Guest user has no profile."}

    # Get User doc
    user_doc = frappe.get_doc("User", user)
    user_email = user_doc.email

    try:
        # Get Student doc by email
        student_doc = frappe.get_doc("Student", {"student_email_id": user_email})

        # Map siblings safely
        siblings = []
        for sib in student_doc.get("siblings") or []:
            siblings.append({
                "full_name": sib.get("full_name"),
                "gender": sib.get("gender"),
                "studying_in_same_institute": sib.get("studying_in_same_institute"),
                "date_of_birth": sib.get("date_of_birth")
            })

        # Map guardians safely
        guardians = []
        for grd in student_doc.get("guardians") or []:
            guardians.append({
                "guardian_name": grd.get("guardian_name"),
                "relation": grd.get("relation"),
                "guardian_id": grd.get("guardian")
            })


        # Program
        program_enrollments = frappe.get_all(
            "Program Enrollment",
            filters={"student": student_doc.name},
            fields="*"
        )

        # Return full mapped student profile
        return {
            "student_id": student_doc.name,
            "full_name": student_doc.get("student_name") or None,
            "first_name": student_doc.get("first_name") or None,
            "middle_name": student_doc.get("middle_name") or None,
            "last_name": student_doc.get("last_name") or None,
            "email": student_doc.get("student_email_id") or None,
            "mobile_number": student_doc.get("student_mobile_number") or None,
            "parent_mobile_number": student_doc.get("parent_mobile_number") or None,
            "hostel_facility": student_doc.get("hostel_facility") or None,
            "date_of_birth": student_doc.get("date_of_birth") or None,
            "blood_group": student_doc.get("blood_group") or None,
            "gender": student_doc.get("gender") or None,
            "nationality": student_doc.get("nationality") or None,
            "category": student_doc.get("category") or None,
            "caste": student_doc.get("caste") or None,
            "religion": student_doc.get("religion") or None,
            "address_line_1": student_doc.get("address_line_1") or None,
            "address_line_2": student_doc.get("address_line_2") or None,
            "pincode": student_doc.get("pincode") or None,
            "city": student_doc.get("city") or None,
            "state": student_doc.get("state") or None,
            "country": student_doc.get("country") or None,
            "joining_date": student_doc.get("joining_date") or None,
            "date_of_leaving": student_doc.get("date_of_leaving") or None,
            "leaving_certificate_number": student_doc.get("leaving_certificate_number") or None,
            "reason_for_leaving": student_doc.get("reason_for_leaving") or None,
            "siblings": siblings,
            "guardians": guardians,
            "program_name": program_enrollments[0].program if program_enrollments else None,
            "program_session": program_enrollments[0].academic_year if program_enrollments else None,
            "program_enrollment_date": program_enrollments[0].enrollment_date if program_enrollments else None,
        }

    except frappe.DoesNotExistError:
        return {"error": "Student profile not found."}
    
    

import frappe

@frappe.whitelist()
def update_student_profile(data):
    import json

    if isinstance(data, str):
        data = json.loads(data)

    user = frappe.session.user

    if user == "Guest":
        return {"error": "Guest cannot update profile"}

    # Get user
    user_doc = frappe.get_doc("User", user)

    # Get student using email
    student_doc = frappe.get_doc("Student", {
        "student_email_id": user_doc.email
    })

    # ---- Update Student Fields ----
    student_doc.student_name = data.get("name")
    student_doc.student_mobile_number = data.get("mobile_number")
    student_doc.category = data.get("category")
    student_doc.caste = data.get("caste")
    student_doc.religion = data.get("religion")
    student_doc.blood_group = data.get("blood_group")
    student_doc.hostel_facility = data.get("hostel_facility")

    student_doc.address_line_1 = data.get("address_line_1")
    student_doc.address_line_2 = data.get("address_line_2")

    # ---- Update Guardians ----
    guardians = data.get("guardians", [])

    if guardians:
        student_doc.set("guardians", [])

        for g in guardians:
            student_doc.append("guardians", {
                "guardian": g.get("guardian_id"),
                "guardian_name": g.get("guardian_name"),
                "relation": g.get("relation")
            })

    student_doc.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "message": "Profile updated successfully",
        "student_id": student_doc.name
    }    