import frappe
from frappe.utils import getdate, today, add_months, add_days, get_first_day, get_last_day


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


def _get_leave_dates(student, first_day, last_day):
    """Get all dates that fall within approved leave applications for the given range."""
    leave_dates = set()

    leaves = frappe.get_all(
        "Student Leave Application",
        filters={
            "student": student,
            "docstatus": 1,
            "from_date": ["<=", str(last_day)],
            "to_date": [">=", str(first_day)],
        },
        fields=["from_date", "to_date", "mark_as_present"],
    )

    for leave in leaves:
        d = max(getdate(leave.from_date), getdate(first_day))
        end = min(getdate(leave.to_date), getdate(last_day))
        while d <= end:
            if not leave.mark_as_present:
                leave_dates.add(str(d))
            d = getdate(add_days(d, 1))

    return leave_dates


@frappe.whitelist()
def get_attendance():
    student = get_student_from_user()
    if not student:
        return {"error": "Student not found"}

    month = frappe.form_dict.get("month")
    year = frappe.form_dict.get("year")

    if month is not None and year is not None:
        month = int(month) + 1  # JS months are 0-indexed, Python is 1-indexed
        year = int(year)
    else:
        now = getdate(today())
        month = now.month
        year = now.year

    from datetime import date, timedelta

    if month > 12:
        month = 1
        year += 1

    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year, 12, 31)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    records = frappe.get_all(
        "Student Attendance",
        filters={
            "student": student,
            "date": ["between", [str(first_day), str(last_day)]],
            "docstatus": 1,
        },
        fields=["date", "status", "leave_application"],
        order_by="date asc",
    )

    leave_dates = _get_leave_dates(student, first_day, last_day)

    attendance_map = {}
    for r in records:
        d = getdate(r.date)
        key = f"{d.year}-{d.month - 1}-{d.day}"

        if r.leave_application or str(d) in leave_dates:
            attendance_map[key] = "L"
        elif r.status == "Present":
            attendance_map[key] = "P"
        else:
            attendance_map[key] = "A"

    # Also add leave dates that have no attendance record
    for date_str in leave_dates:
        d = getdate(date_str)
        if getdate(first_day) <= d <= getdate(last_day):
            key = f"{d.year}-{d.month - 1}-{d.day}"
            if key not in attendance_map:
                attendance_map[key] = "L"

    return attendance_map


@frappe.whitelist()
def get_attendance_summary():
    student = get_student_from_user()
    if not student:
        return {"error": "Student not found"}

    now = getdate(today())
    months_data = []

    for i in range(6):
        d = add_months(now, -i)
        first = get_first_day(d)
        last = get_last_day(d)

        records = frappe.get_all(
            "Student Attendance",
            filters={
                "student": student,
                "date": ["between", [str(first), str(last)]],
                "docstatus": 1,
            },
            fields=["status", "leave_application", "count(*) as cnt"],
            group_by="status",
        )

        leave_dates = _get_leave_dates(student, first, last)

        # Count attendance with leave_application linked
        leave_att_count = 0
        if leave_dates:
            leave_att_records = frappe.get_all(
                "Student Attendance",
                filters={
                    "student": student,
                    "date": ["between", [str(first), str(last)]],
                    "docstatus": 1,
                    "leave_application": ["is", "set"],
                },
            )
            leave_att_count = len(leave_att_records)

        present = 0
        absent = 0
        for r in records:
            if r.status == "Present":
                present = r.cnt
            elif r.status == "Absent":
                absent = r.cnt

        # Leave days = leave_application linked records + leave dates without attendance records
        dates_with_attendance = set()
        all_att = frappe.get_all(
            "Student Attendance",
            filters={
                "student": student,
                "date": ["between", [str(first), str(last)]],
                "docstatus": 1,
            },
            fields=["date"],
        )
        for a in all_att:
            dates_with_attendance.add(str(getdate(a.date)))

        leave_only_count = len(leave_dates - dates_with_attendance)
        leave = leave_att_count + leave_only_count

        # Adjust: if leave_application records were counted in present/absent, subtract them
        present = max(0, present - leave_att_count)

        total = present + absent + leave
        percent = round((present / total) * 100) if total > 0 else 0

        month_name = d.strftime("%B %Y")
        months_data.append({
            "name": month_name,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percent": percent,
        })

    total_present = sum(m["present"] for m in months_data)
    total_absent = sum(m["absent"] for m in months_data)
    total_leave = sum(m["leave"] for m in months_data)
    grand_total = total_present + total_absent + total_leave
    rate = round((total_present / grand_total) * 100, 1) if grand_total > 0 else 0

    return {
        "rate": rate,
        "total_present": total_present,
        "total_absent": total_absent,
        "total_leave": total_leave,
        "months": months_data,
    }
