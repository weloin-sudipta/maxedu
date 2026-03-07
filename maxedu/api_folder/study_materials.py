import frappe


def get_student_from_user():
    user = frappe.session.user
    students = frappe.get_all("Student", filters={"user": user}, fields=["name"], limit=1)
    if not students:
        students = frappe.get_all(
            "Student",
            filters={"student_email_id": user},
            fields=["name"],
            limit=1,
        )
    return students[0].name if students else None


@frappe.whitelist()
def get_study_materials():
    student = get_student_from_user()
    if not student:
        return []

    enrollments = frappe.get_all(
        "Course Enrollment",
        filters={"student": student},
        fields=["course"],
    )

    if not enrollments:
        return []

    courses = [e.course for e in enrollments]

    materials = frappe.get_all(
        "Study Material",
        filters={"course": ["in", courses]},
        fields=[
            "name",
            "title",
            "course",
            "topic",
            "category",
            "file",
            "file_type",
            "file_size",
            "upload_date",
            "description",
        ],
        order_by="upload_date desc",
    )

    for m in materials:
        if m.get("course"):
            course_name = frappe.db.get_value("Course", m["course"], "course_name")
            m["course_name"] = course_name or m["course"]
        if m.get("topic"):
            topic_name = frappe.db.get_value("Topic", m["topic"], "topic_name")
            m["topic_name"] = topic_name or m["topic"]

    return materials
