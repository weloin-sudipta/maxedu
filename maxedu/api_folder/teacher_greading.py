import frappe

@frappe.whitelist()
def get_my_courses():
    user = frappe.session.user
    full_name = frappe.db.get_value("User", user, "full_name")

    # Try finding instructor by name matching full_name (user's ID or full_name)
    instructor_name = frappe.db.get_value("Instructor", {"name": full_name}, "name")

    if not instructor_name:
        # Fallback 1: instructor_email matching session user
        instructor_name = frappe.db.get_value("Instructor", {"instructor_email": user}, "name")

    if not instructor_name:
        # Fallback 2: instructor_name matching user full_name
        instructor_name = frappe.db.get_value("Instructor", {"instructor_name": full_name}, "name")

    if not instructor_name:
        return {"error": "Instructor not found for this user"}

    instructor = frappe.get_doc("Instructor", instructor_name).as_dict()

    instructor_logs = frappe.get_all(
        "Instructor Log",
        filters={"parent": instructor["name"]},
        fields=["name", "academic_year", "academic_term", "program", "course"],
        order_by="idx asc"
    )

    instructor["instructor_log"] = instructor_logs
    return instructor


@frappe.whitelist()
def get_my_exams():
    # Reuse get_my_courses to get instructor + logs
    instructor_data = get_my_courses()

    if isinstance(instructor_data, dict) and instructor_data.get("error"):
        return instructor_data

    instructor_logs = instructor_data.get("instructor_log", [])

    if not instructor_logs:
        return []

    # Loop through each log and fetch matching Assessment Plans
    all_exams = []
    seen = set()

    for log in instructor_logs:
        exams = frappe.get_all(
            "Assessment Plan",
            filters={
                "course":        log["course"],
                "program":       log["program"],
                "academic_year": log["academic_year"],
                "academic_term": log["academic_term"],
            },
            fields="*"
        )
        for exam in exams:
            if exam["name"] not in seen:
                seen.add(exam["name"])
                all_exams.append(exam)

    return all_exams


import frappe

# ─────────────────────────────────────────────────────────────────────────────
# API 1: Get all students + their existing result (if any) for an Assessment Plan
# Call this when teacher selects an exam from the dropdown
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def get_exam_students(assessment_plan):
    """
    Returns:
    {
        "plan": { ...assessment plan fields... },
        "students": [
            {
                "student": "EDU-STU-2026-00001",
                "student_name": "Edward Thomas",
                "result_id": "EDU-ASR-2026-00001",   # null if not graded yet
                "score": 85.0,                        # null if not graded yet
                "grade": "A",                         # null if not graded yet
                "comment": "Good work"                # null if not graded yet
            },
            ...
        ]
    }
    """
    # Step 1: Fetch the Assessment Plan details
    plan = frappe.get_doc("Assessment Plan", assessment_plan)

    # Step 2: Get all students in the student group
    student_group_members = frappe.get_all(
        "Student Group Student",                  # child table
        filters={"parent": plan.student_group},
        fields=["student", "student_name"],
        order_by="idx asc"
    )

    # Step 3: For each student, check if a result already exists
    students_data = []
    for member in student_group_members:
        existing_result = frappe.get_all(
            "Assessment Result",
            filters={
                "assessment_plan": assessment_plan,
                "student": member["student"]
            },
            fields=["name", "total_score", "grade", "comment"],
            limit=1
        )

        students_data.append({
            "student":      member["student"],
            "student_name": member["student_name"],
            "result_id":    existing_result[0]["name"]         if existing_result else None,
            "score":        existing_result[0]["total_score"]  if existing_result else None,
            "grade":        existing_result[0]["grade"]        if existing_result else None,
            "comment":      existing_result[0]["comment"]      if existing_result else None,
        })

    return {
        "plan": {
            "name":                   plan.name,
            "assessment_name":        plan.assessment_name,
            "course":                 plan.course,
            "program":                plan.program,
            "academic_year":          plan.academic_year,
            "academic_term":          plan.academic_term,
            "student_group":          plan.student_group,
            "assessment_group":       plan.assessment_group,
            "grading_scale":          plan.grading_scale,
            "maximum_assessment_score": plan.maximum_assessment_score,
            "schedule_date":          plan.schedule_date,
            "from_time":              plan.from_time,
            "to_time":                plan.to_time,
            "examiner_name":          plan.examiner_name,
        },
        "students": students_data
    }


# ─────────────────────────────────────────────────────────────────────────────
# API 2: Submit / Update grades for all students in one call
# Call this when teacher clicks "Submit All Grades"
# ─────────────────────────────────────────────────────────────────────────────
@frappe.whitelist()
def submit_exam_results(assessment_plan, results):
    """
    results (JSON array passed from frontend):
    [
        {
            "student": "EDU-STU-2026-00001",
            "score": 85,
            "comment": "Well done"
        },
        ...
    ]
    """
    import json

    # Frappe passes JSON as string from frontend — parse it
    if isinstance(results, str):
        results = json.loads(results)

    # Fetch plan details (needed to fill required fields on Assessment Result)
    plan = frappe.get_doc("Assessment Plan", assessment_plan)

    response = []

    for result in results:
        student  = result.get("student")
        score    = float(result.get("score", 0))
        comment  = result.get("comment", "")

        # Check if a result already exists for this student
        existing = frappe.get_all(
            "Assessment Result",
            filters={
                "assessment_plan": assessment_plan,
                "student": student
            },
            fields=["name", "docstatus"],
            limit=1
        )

        if existing:
            # ── UPDATE existing result ────────────────────────────────────
            result_doc = frappe.get_doc("Assessment Result", existing[0]["name"])

            # If already submitted (docstatus=1), cancel → amend → resubmit
            if result_doc.docstatus == 1:
                result_doc.cancel()
                result_doc = frappe.copy_doc(result_doc)
                result_doc.amended_from = existing[0]["name"]

            # Update scores in the criteria table
            for detail in result_doc.details:
                detail.score = score   # set each criteria score

            result_doc.comment = comment
            result_doc.save()

            if result_doc.docstatus == 0:
                result_doc.submit()

            response.append({"student": student, "status": "updated", "result": result_doc.name})

        else:
            # ── CREATE new Assessment Result ──────────────────────────────
            result_doc = frappe.get_doc({
                "doctype":        "Assessment Result",
                "assessment_plan": assessment_plan,
                "student":        student,
                "program":        plan.program,
                "course":         plan.course,
                "academic_year":  plan.academic_year,
                "academic_term":  plan.academic_term,
                "student_group":  plan.student_group,
                "assessment_group": plan.assessment_group,
                "grading_scale":  plan.grading_scale,
                "comment":        comment,
                # Fill the assessment criteria detail rows
                "details": [
                    {
                        "assessment_criteria": d.assessment_criteria,
                        "maximum_score":       d.maximum_score,
                        "score":               score,  # assign full score to single criteria
                    }
                    for d in plan.assessment_criteria   # child table on Assessment Plan
                ]
            })

            result_doc.insert()
            result_doc.submit()   # docstatus → 1 (submitted)

            response.append({"student": student, "status": "created", "result": result_doc.name})

    return response