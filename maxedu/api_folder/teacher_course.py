import frappe
from .teacher_greading import get_my_courses


@frappe.whitelist()
def get_course_topics():
    teacherdata = get_my_courses()

    if not teacherdata or teacherdata.get("error"):
        return teacherdata

    instructor_log = teacherdata.get("instructor_log", [])

    # Extract course names
    course_names = [
        log.get("course")
        for log in instructor_log
        if log.get("course")
    ]

    # Remove duplicates
    course_names = list(set(course_names))

    courses = []

    for course_name in course_names:
        try:
            course_doc = frappe.get_doc("Course", course_name)

            # Convert to dict so it's JSON serializable
            course_dict = course_doc.as_dict()

            # Optional: keep only topics cleanly
            course_dict["topics"] = course_doc.get("topics")

            courses.append(course_dict)

        except frappe.DoesNotExistError:
            continue

    return courses

@frappe.whitelist()
def get_teacher_details():
    return frappe.get_doc("Instructor","Mr. Davis")