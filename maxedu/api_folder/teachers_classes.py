import frappe
from frappe.utils import nowdate
from collections import defaultdict

@frappe.whitelist()
def get_my_classes():
    today = nowdate()

    # Get instructor
    teacher_name = frappe.db.get_value("User", frappe.session.user, "full_name")
    instructor_name = frappe.db.get_value(
        "Instructor",
        {"instructor_name": teacher_name},
        "name"
    )

    if not instructor_name:
        return {"success": False, "message": "No instructor record found", "classes": []}

    # Get today's schedules for the instructor
    schedules = frappe.get_all(
        "Course Schedule",
        filters={
            "instructor": instructor_name,
            "schedule_date": today
        },
        fields=[
            "name", "course", "title",
            "instructor", "instructor_name",
            "schedule_date", "from_time", "to_time",
            "room", "student_group", "program",
            "color", "class_schedule_color"
        ],
    )

    if not schedules:
        return {"success": True, "classes": []}

    # Get all student groups in the schedules
    student_group_ids = list({s.student_group for s in schedules if s.student_group})

    # Fetch all students in these groups
    student_group_students = frappe.get_all(
        "Student Group Student",
        filters={"parent": ["in", student_group_ids], "active": 1},
        fields=["parent", "student", "student_name"]
    )

    # Group students by student_group
    students_by_group = defaultdict(list)
    student_ids = []  # collect all student ids to fetch attendance
    for sgs in student_group_students:
        students_by_group[sgs.parent].append({
            "student": sgs.student,
            "student_name": sgs.student_name
        })
        student_ids.append(sgs.student)

    # Fetch all attendance for today schedules in one query
    course_schedule_ids = [s.name for s in schedules]
    attendance_records = frappe.get_all(
        "Student Attendance",
        filters={
            "student": ["in", student_ids],
            "course_schedule": ["in", course_schedule_ids]
        },
        fields=["student", "course_schedule", "status"]
    )

    # Map attendance: {(student, schedule): status}
    attendance_map = {(a.student, a.course_schedule): a.status for a in attendance_records}

    # Attach students + attendance to schedules
    result = []
    for schedule in schedules:
        group = schedule.student_group
        students_list = []
        for s in students_by_group.get(group, []):
            status = attendance_map.get((s["student"], schedule["name"]), None)
            students_list.append({
                "student": s["student"],
                "student_name": s["student_name"],
                "status": status  # None if not marked yet
            })
        result.append({
            **schedule,
            "students": students_list,
            "total_students": len(students_list)
        })

    return {"success": True, "classes": result,"instructor": instructor_name}


@frappe.whitelist()
def mark_attendance_bulk(students, course_schedule):
    import json

    # Parse input if string
    if isinstance(students, str):
        students = json.loads(students)

    results = {
        "success": [],
        "failed": []
    }

    for s in students:
        try:
            student_id = s.get("student")
            status = (s.get("status") or "Present").capitalize()

            # Check if record already exists
            existing_name = frappe.db.exists(
                "Student Attendance",
                {
                    "student": student_id,
                    "course_schedule": course_schedule
                }
            )

            if existing_name:
                # Update the existing doc instead of failing
                doc = frappe.get_doc("Student Attendance", existing_name)
                doc.status = status
                doc.save(ignore_permissions=True)
                doc.submit()
                results["success"].append(student_id)
                continue

            # Create new attendance doc if not exists
            doc = frappe.get_doc({
                "doctype": "Student Attendance",
                "student": student_id,
                "course_schedule": course_schedule,
                "status": status
            })
            doc.insert(ignore_permissions=True)
            doc.submit()

            results["success"].append(student_id)

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Bulk Attendance Error")
            results["failed"].append({
                "student": student_id,
                "reason": str(e)
            })

    return results