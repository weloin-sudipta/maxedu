import frappe


@frappe.whitelist()
def test_working():
    return "working"


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


@frappe.whitelist()
def get_profile():
    if user_has_role("Student"):
        return get_student_profile()
    else:
        return {"error": "Profile information is only available for students."}


def get_student_profile():
    user = frappe.session.user
    if user_is_guest():
        return {"error": "Guest user has no profile."}

    user_doc = frappe.get_doc("User", user)
    user_email = user_doc.email

    try:
        student_doc = frappe.get_doc("Student", {"student_email_id": user_email})

        siblings = []
        for sib in student_doc.get("siblings") or []:
            siblings.append({
                "full_name": sib.get("full_name"),
                "gender": sib.get("gender"),
                "studying_in_same_institute": sib.get("studying_in_same_institute"),
                "date_of_birth": sib.get("date_of_birth"),
            })

        guardians = []
        for grd in student_doc.get("guardians") or []:
            guardians.append({
                "guardian_name": grd.get("guardian_name"),
                "relation": grd.get("relation"),
                "guardian_id": grd.get("guardian"),
            })

        program_enrollments = frappe.get_all(
            "Program Enrollment",
            filters={"student": student_doc.name},
            fields="*",
        )

        photo_url = student_doc.get("image") or user_doc.get("user_image") or None

        return {
            "student_id": student_doc.name,
            "full_name": student_doc.get("student_name") or None,
            "student_name": student_doc.get("student_name") or None,
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
            "photo_url": photo_url,
            "program_name": program_enrollments[0].program if program_enrollments else None,
            "program_session": program_enrollments[0].academic_year if program_enrollments else None,
            "program_enrollment_date": program_enrollments[0].enrollment_date if program_enrollments else None,
        }

    except frappe.DoesNotExistError:
        return {"error": "Student profile not found."}


@frappe.whitelist()
def update_profile(data):
    data = frappe.parse_json(data)

    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)

    if data.get("firstName"):
        user_doc.first_name = data.get("firstName")
    if data.get("middleName") is not None:
        user_doc.middle_name = data.get("middleName")
    if data.get("lastName"):
        user_doc.last_name = data.get("lastName")
    if data.get("phone"):
        user_doc.phone = data.get("phone")
    if data.get("mobile"):
        user_doc.mobile_no = data.get("mobile")
    if data.get("language"):
        user_doc.language = data.get("language")
    if data.get("timezone"):
        user_doc.time_zone = data.get("timezone")

    if data.get("user_image"):
        user_doc.user_image = data.get("user_image")

    user_doc.save(ignore_permissions=True)

    if data.get("user_image"):
        try:
            student_doc = frappe.get_doc("Student", {"student_email_id": user})
            student_doc.image = data.get("user_image")
            student_doc.save(ignore_permissions=True)
        except frappe.DoesNotExistError:
            pass

    return {
        "status": "success",
        "message": "Profile updated successfully",
    }


@frappe.whitelist()
def upload_profile_photo():
    user = frappe.session.user

    if not frappe.request or not frappe.request.files:
        return {"error": "No file uploaded"}

    filedata = frappe.request.files.get("file")
    if not filedata:
        return {"error": "No file uploaded"}

    from frappe.handler import upload_file

    ret = upload_file()

    file_url = ret.get("file_url") if isinstance(ret, dict) else ret.file_url

    user_doc = frappe.get_doc("User", user)
    user_doc.user_image = file_url
    user_doc.save(ignore_permissions=True)

    try:
        student_doc = frappe.get_doc("Student", {"student_email_id": user})
        student_doc.image = file_url
        student_doc.save(ignore_permissions=True)
    except frappe.DoesNotExistError:
        pass

    return {"file_url": file_url, "status": "success"}
