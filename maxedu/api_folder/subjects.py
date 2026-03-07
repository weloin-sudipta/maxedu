import frappe


@frappe.whitelist()
def get_program():
    user = frappe.session.user

    student = frappe.get_all(
        "Student",
        filters={"user": user},
        fields=["name"],
    )

    if not student:
        student = frappe.get_all(
            "Student",
            filters={"student_email_id": user},
            fields=["name"],
        )

    if not student:
        return {"courses": []}

    student_id = student[0].name

    enrollments = frappe.get_all(
        "Course Enrollment",
        filters={"student": student_id},
        fields=["name", "course"],
    )

    if not enrollments:
        return {"courses": []}

    courses = []
    for enrollment in enrollments:
        course = frappe.get_doc("Course", enrollment.course)

        topics = []
        for topic in course.get("topics") or []:
            topics.append({
                "name": topic.name,
                "topic": topic.topic,
                "topic_name": topic.topic_name,
            })

        courses.append({
            "course_id": course.name,
            "course_name": course.course_name,
            "topics": topics,
        })

    return {"courses": courses}
