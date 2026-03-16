import frappe
from frappe.utils import getdate, today


def get_student_from_user():
    user = frappe.session.user

    student = frappe.db.get_value(
        "Student",
        {"student_email_id": user},
        "name"
    )
    return student

@frappe.whitelist()
def get_assignments():
    student = get_student_from_user()
    if not student:
        return []

    assignments = frappe.get_all(
        "Student Assignment",
        filters={"student": student},
        fields=[
            "name",
            "title",
            "course",
            "topic",
            "due_date",
            "status",
            "difficulty",
            "assignment_file",
            "submission_file",
            "evaluated_score",
            "remarks",
        ],
        order_by="due_date desc",
    )

    for a in assignments:
        if a.get("course"):
            course_name = frappe.db.get_value("Course", a["course"], "course_name")
            a["course_name"] = course_name or a["course"]
        if a.get("topic"):
            topic_name = frappe.db.get_value("Topic", a["topic"], "topic_name")
            a["topic_name"] = topic_name or a["topic"]

        if a["status"] == "Active" and a.get("due_date") and getdate(a["due_date"]) < getdate(today()):
            a["status"] = "Overdue"

    return assignments


@frappe.whitelist()
def submit_assignment(assignment_name, submission_file=None):
    student = get_student_from_user()
    if not student:
        return {"error": "Student not found"}

    doc = frappe.get_doc("Student Assignment", assignment_name)
    if doc.student != student:
        frappe.throw("You can only submit your own assignments")

    doc.status = "Submitted"
    if submission_file:
        doc.submission_file = submission_file
    doc.save(ignore_permissions=True)

    return {"status": "success", "message": "Assignment submitted successfully"}
