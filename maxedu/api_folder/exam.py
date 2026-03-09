import frappe
from .student import get_student_group

@frappe.whitelist()
def get_exams():
    student_groups = get_student_group()
    exams = []

    for group in student_groups:
        group_exams = frappe.get_all(
            "Assessment Plan",
            filters={"student_group": group["parent"]},
            fields=[
                "name",
                "assessment_name",
                "course",
                "assessment_group",
                "schedule_date",
                "from_time",
                "to_time",
                "room",
                "examiner_name",
                "maximum_assessment_score",
                "student_group",
                "academic_year",
                "grading_scale",
                "program"
            ]
        )

        for exam in group_exams:
            exams.append({
                "exam_id": exam.get("name"),
                "subject": exam.get("assessment_name"),
                "course": exam.get("course"),
                "exam_type": exam.get("assessment_group"),
                "date": exam.get("schedule_date"),
                "start_time": exam.get("from_time"),
                "end_time": exam.get("to_time"),
                "room": exam.get("room"),
                "examiner": exam.get("examiner_name"),
                "max_score": exam.get("maximum_assessment_score"),
                "student_group": exam.get("student_group"),
                "academic_year": exam.get("academic_year"),
                "grading_scale": exam.get("grading_scale"),
                "program": exam.get("program")
            })

    return exams

@frappe.whitelist()
def get_results():
    student = frappe.get_doc(
        "Student",
        {"student_email_id": frappe.session.user}
    )

    assessment_result = frappe.get_all(
        "Assessment Result",
        filters={"student": student.name},
        fields="*"
    )

    return assessment_result 