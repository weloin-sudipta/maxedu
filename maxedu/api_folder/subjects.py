import frappe

@frappe.whitelist()
def get_program():
    user = frappe.session.user

    data = frappe.db.sql("""
        SELECT
            ce.course as course_id,
            c.course_name,
            ct.name as topic_row,
            ct.topic,
            ct.topic_name
        FROM `tabStudent` s
        INNER JOIN `tabCourse Enrollment` ce
            ON ce.student = s.name
        INNER JOIN `tabCourse` c
            ON c.name = ce.course
        LEFT JOIN `tabCourse Topic` ct
            ON ct.parent = c.name
        WHERE s.student_email_id = %s
    """, (user,), as_dict=True)

    if not data:
        return {"courses": []}

    courses_map = {}

    for row in data:
        cid = row.course_id

        if cid not in courses_map:
            courses_map[cid] = {
                "course_id": cid,
                "course_name": row.course_name,
                "topics": []
            }

        if row.topic:
            courses_map[cid]["topics"].append({
                "name": row.topic_row,
                "topic": row.topic,
                "topic_name": row.topic_name
            })

    return {"courses": list(courses_map.values())}
