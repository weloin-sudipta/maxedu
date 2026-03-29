import frappe
from frappe.utils import add_days, today, getdate, add_months


def create_test_data():
    """Create comprehensive test data for maxedu application."""
    frappe.flags.ignore_permissions = True

    try:
        _create_academic_year()
        _create_academic_term()
        _create_student_category()
        _create_room()
        _create_holiday_list()
        _create_guardian()
        _create_instructor()
        _create_grading_scale()
        _create_topics()
        _create_course()
        _create_program()
        student_id = _create_student()
        _create_program_enrollment(student_id)
        _create_course_enrollment(student_id)
        _create_student_group(student_id)
        _create_student_attendance(student_id)
        _create_study_materials()
        _create_student_assignments(student_id)

        frappe.db.commit()
        print("Test data created successfully!")
        return {"status": "success"}
    except Exception as e:
        frappe.db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}
    finally:
        frappe.flags.ignore_permissions = False


def _create_academic_year():
    if not frappe.db.exists("Academic Year", "2025-2026"):
        doc = frappe.get_doc({
            "doctype": "Academic Year",
            "academic_year_name": "2025-2026",
            "year_start_date": "2025-06-01",
            "year_end_date": "2026-05-31",
        })
        doc.insert()
        print("Created Academic Year: 2025-2026")


def _create_academic_term():
    if not frappe.db.exists("Academic Term", "2025-2026 (Term 1)"):
        doc = frappe.get_doc({
            "doctype": "Academic Term",
            "academic_year": "2025-2026",
            "term_name": "Term 1",
            "term_start_date": "2025-06-01",
            "term_end_date": "2025-11-30",
        })
        doc.insert()
        print("Created Academic Term: Term 1")

    if not frappe.db.exists("Academic Term", "2025-2026 (Term 2)"):
        doc = frappe.get_doc({
            "doctype": "Academic Term",
            "academic_year": "2025-2026",
            "term_name": "Term 2",
            "term_start_date": "2025-12-01",
            "term_end_date": "2026-05-31",
        })
        doc.insert()
        print("Created Academic Term: Term 2")


def _create_student_category():
    if not frappe.db.exists("Student Category", "General"):
        frappe.get_doc({
            "doctype": "Student Category",
            "category": "General",
        }).insert()
        print("Created Student Category: General")


def _create_room():
    if not frappe.db.exists("Room", "Room 101"):
        frappe.get_doc({
            "doctype": "Room",
            "room_name": "Room 101",
            "room_number": "101",
            "seating_capacity": 40,
        }).insert()
        print("Created Room: 101")


def _create_holiday_list():
    hl_name = "Academic Holidays 2025-2026"
    if frappe.db.exists("Holiday List", hl_name):
        return

    holidays = [
        {"holiday_date": "2025-08-15", "description": "Independence Day"},
        {"holiday_date": "2025-10-02", "description": "Gandhi Jayanti"},
        {"holiday_date": "2025-10-20", "description": "Dussehra"},
        {"holiday_date": "2025-11-01", "description": "Diwali"},
        {"holiday_date": "2025-12-25", "description": "Christmas"},
        {"holiday_date": "2026-01-26", "description": "Republic Day"},
        {"holiday_date": "2026-03-14", "description": "Holi"},
    ]

    frappe.get_doc({
        "doctype": "Holiday List",
        "holiday_list_name": hl_name,
        "from_date": "2025-06-01",
        "to_date": "2026-05-31",
        "holidays": holidays,
    }).insert()

    companies = frappe.get_all("Company", fields=["name"])
    for company in companies:
        frappe.db.set_value("Company", company.name, "default_holiday_list", hl_name)

    education_settings = frappe.get_single("Education Settings")
    if hasattr(education_settings, "default_holiday_list"):
        education_settings.default_holiday_list = hl_name
        education_settings.save()

    print(f"Created Holiday List: {hl_name}")


def _create_guardian():
    if not frappe.db.exists("Guardian", {"guardian_name": "Robert Thomas"}):
        frappe.get_doc({
            "doctype": "Guardian",
            "guardian_name": "Robert Thomas",
            "email_address": "robert.thomas@example.com",
            "mobile_number": "9876543210",
            "occupation": "Software Engineer",
        }).insert()
        print("Created Guardian: Robert Thomas")

    if not frappe.db.exists("Guardian", {"guardian_name": "Mary Thomas"}):
        frappe.get_doc({
            "doctype": "Guardian",
            "guardian_name": "Mary Thomas",
            "email_address": "mary.thomas@example.com",
            "mobile_number": "9876543211",
            "occupation": "Doctor",
        }).insert()
        print("Created Guardian: Mary Thomas")


def _create_instructor():
    if frappe.db.exists("Instructor", {"instructor_name": "Prof. Sharma"}):
        return

    instructor_user = "prof.sharma@example.com"
    if not frappe.db.exists("User", instructor_user):
        user = frappe.get_doc({
            "doctype": "User",
            "email": instructor_user,
            "first_name": "Prof.",
            "last_name": "Sharma",
            "roles": [{"role": "Instructor"}],
            "send_welcome_email": 0,
        })
        user.insert()

    frappe.get_doc({
        "doctype": "Instructor",
        "instructor_name": "Prof. Sharma",
        "user": instructor_user,
        "instructor_log": [
            {
                "academic_year": "2025-2026",
                "academic_term": "2025-2026 (Term 1)",
                "program": "Class 12 Science",
                "course": "Advanced Mathematics",
            },
            {
                "academic_year": "2025-2026",
                "academic_term": "2025-2026 (Term 1)",
                "program": "Class 12 Science",
                "course": "Physics",
            }
        ]
    }).insert()
    print("Created Instructor: Prof. Sharma")


def _create_grading_scale():
    if frappe.db.exists("Grading Scale", "Standard Grading"):
        return

    frappe.get_doc({
        "doctype": "Grading Scale",
        "grading_scale_name": "Standard Grading",
        "intervals": [
            {"grade_code": "A+", "threshold": 90, "grade_description": "Outstanding"},
            {"grade_code": "A", "threshold": 80, "grade_description": "Excellent"},
            {"grade_code": "B+", "threshold": 70, "grade_description": "Very Good"},
            {"grade_code": "B", "threshold": 60, "grade_description": "Good"},
            {"grade_code": "C", "threshold": 50, "grade_description": "Average"},
            {"grade_code": "D", "threshold": 40, "grade_description": "Below Average"},
            {"grade_code": "F", "threshold": 0, "grade_description": "Fail"},
        ],
    }).insert()
    print("Created Grading Scale: Standard Grading")


def _create_topics():
    topics = [
        {"name_val": "Algebra", "desc": "Linear equations, quadratic equations, polynomials"},
        {"name_val": "Trigonometry", "desc": "Sin, Cos, Tan identities and applications"},
        {"name_val": "Calculus", "desc": "Differentiation and Integration fundamentals"},
        {"name_val": "Mechanics", "desc": "Newton's laws of motion, energy, momentum"},
        {"name_val": "Thermodynamics", "desc": "Heat, temperature, laws of thermodynamics"},
        {"name_val": "Optics", "desc": "Light, reflection, refraction, lenses"},
        {"name_val": "Organic Chemistry", "desc": "Carbon compounds, hydrocarbons, reactions"},
        {"name_val": "Inorganic Chemistry", "desc": "Periodic table, bonding, metals"},
        {"name_val": "Cell Biology", "desc": "Cell structure, mitosis, meiosis"},
        {"name_val": "Genetics", "desc": "DNA, RNA, heredity, mutations"},
        {"name_val": "Poetry Analysis", "desc": "Analysis of literary poems and techniques"},
        {"name_val": "Essay Writing", "desc": "Structure, argumentation, and style"},
        {"name_val": "Ancient History", "desc": "Civilizations, empires, and cultures"},
        {"name_val": "Modern History", "desc": "Industrial revolution to present day"},
        {"name_val": "Programming Basics", "desc": "Variables, loops, functions, data structures"},
    ]

    for t in topics:
        if not frappe.db.exists("Topic", t["name_val"]):
            frappe.get_doc({
                "doctype": "Topic",
                "topic_name": t["name_val"],
                "description": t["desc"],
            }).insert()

    print(f"Created {len(topics)} Topics")


def _create_course():
    courses = [
        {
            "name_val": "Advanced Mathematics",
            "topics": ["Algebra", "Trigonometry", "Calculus"],
        },
        {
            "name_val": "Physics",
            "topics": ["Mechanics", "Thermodynamics", "Optics"],
        },
        {
            "name_val": "Chemistry",
            "topics": ["Organic Chemistry", "Inorganic Chemistry"],
        },
        {
            "name_val": "Biology",
            "topics": ["Cell Biology", "Genetics"],
        },
        {
            "name_val": "English Literature",
            "topics": ["Poetry Analysis", "Essay Writing"],
        },
        {
            "name_val": "History",
            "topics": ["Ancient History", "Modern History"],
        },
        {
            "name_val": "Computer Science",
            "topics": ["Programming Basics"],
        },
    ]

    for c in courses:
        if not frappe.db.exists("Course", c["name_val"]):
            topic_rows = []
            for t_name in c["topics"]:
                topic_id = frappe.db.get_value("Topic", {"topic_name": t_name}, "name")
                if topic_id:
                    topic_rows.append({"topic": topic_id})

            frappe.get_doc({
                "doctype": "Course",
                "course_name": c["name_val"],
                "default_grading_scale": "Standard Grading" if frappe.db.exists("Grading Scale", "Standard Grading") else None,
                "topics": topic_rows,
            }).insert()

    print(f"Created {len(courses)} Courses")


def _create_program():
    if frappe.db.exists("Program", "Class 12 Science"):
        return

    courses = ["Advanced Mathematics", "Physics", "Chemistry", "Biology", "English Literature", "History", "Computer Science"]
    course_rows = []
    for c_name in courses:
        if frappe.db.exists("Course", c_name):
            course_rows.append({"course": c_name})

    frappe.get_doc({
        "doctype": "Program",
        "program_name": "Class 12 Science",
        "courses": course_rows,
    }).insert()
    print("Created Program: Class 12 Science")


def _create_student():
    test_email = "edward.thomas@example.com"

    if not frappe.db.exists("User", test_email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": test_email,
            "first_name": "Edward",
            "last_name": "Thomas",
            "roles": [{"role": "Student"}],
            "send_welcome_email": 0,
            "new_password": "Edw@rd#Th0m4s!2026",
        })
        user.insert()
        print(f"Created User: {test_email}")

    existing = frappe.get_all("Student", filters={"student_email_id": test_email}, fields=["name"], limit=1)
    if existing:
        student_id = existing[0].name
        print(f"Student already exists: {student_id}")
        return student_id

    father = frappe.get_all("Guardian", filters={"guardian_name": "Robert Thomas"}, fields=["name"], limit=1)
    mother = frappe.get_all("Guardian", filters={"guardian_name": "Mary Thomas"}, fields=["name"], limit=1)

    guardians = []
    if father:
        guardians.append({"guardian": father[0].name, "guardian_name": "Robert Thomas", "relation": "Father"})
    if mother:
        guardians.append({"guardian": mother[0].name, "guardian_name": "Mary Thomas", "relation": "Mother"})

    student = frappe.get_doc({
        "doctype": "Student",
        "first_name": "Edward",
        "last_name": "Thomas",
        "student_email_id": test_email,
        "user": test_email,
        "date_of_birth": "2008-05-15",
        "gender": "Male",
        "blood_group": "B+",
        "nationality": "Indian",
        "student_mobile_number": "9998887776",
        "address_line_1": "42 MG Road, Koramangala",
        "address_line_2": "Near Indiranagar Metro",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "pincode": "560034",
        "joining_date": "2025-06-01",
        "guardians": guardians,
    })
    student.insert()

    try:
        student.caste = "General"
        student.religion = "Christianity"
        student.parent_mobile_number = "9876543210"
        student.hostel_facility = "No"
        student.save()
    except Exception:
        pass

    print(f"Created Student: {student.name} ({test_email})")
    return student.name


def _create_program_enrollment(student_id):
    existing = frappe.get_all(
        "Program Enrollment",
        filters={"student": student_id, "program": "Class 12 Science"},
        limit=1,
    )
    if existing:
        return

    frappe.get_doc({
        "doctype": "Program Enrollment",
        "student": student_id,
        "program": "Class 12 Science",
        "academic_year": "2025-2026",
        "academic_term": "2025-2026 (Term 1)",
        "enrollment_date": "2025-06-01",
    }).insert()
    print("Created Program Enrollment")


def _create_course_enrollment(student_id):
    courses = ["Advanced Mathematics", "Physics", "Chemistry", "Biology", "English Literature", "History", "Computer Science"]

    for c_name in courses:
        if not frappe.db.exists("Course", c_name):
            continue
        existing = frappe.get_all(
            "Course Enrollment",
            filters={"student": student_id, "course": c_name},
            limit=1,
        )
        if existing:
            continue

        program = "Class 12 Science" if frappe.db.exists("Program", "Class 12 Science") else None
        frappe.get_doc({
            "doctype": "Course Enrollment",
            "student": student_id,
            "course": c_name,
            "program_enrollment": frappe.get_all(
                "Program Enrollment",
                filters={"student": student_id},
                fields=["name"],
                limit=1,
            )[0].name if program else None,
            "enrollment_date": "2025-06-01",
        }).insert()

    print(f"Created Course Enrollments for {len(courses)} courses")


def _create_student_group(student_id):
    if frappe.db.exists("Student Group", "Class 12 Science - 2025"):
        return

    frappe.get_doc({
        "doctype": "Student Group",
        "student_group_name": "Class 12 Science - 2025",
        "group_based_on": "Batch",
        "academic_year": "2025-2026",
        "academic_term": "2025-2026 (Term 1)",
        "program": "Class 12 Science",
        "students": [{"student": student_id, "active": 1}],
    }).insert()
    print("Created Student Group")


def _create_student_attendance(student_id):
    existing = frappe.get_all(
        "Student Attendance",
        filters={"student": student_id, "docstatus": 1},
        limit=1,
    )
    if existing:
        print("Attendance already exists, skipping")
        return

    student_group = frappe.get_all("Student Group", filters={"program": "Class 12 Science"}, fields=["name"], limit=1)
    sg_name = student_group[0].name if student_group else None

    holiday_dates = set()
    hl = frappe.get_all("Holiday List", limit=1)
    if hl:
        holidays = frappe.get_all("Holiday", filters={"parent": hl[0].name}, fields=["holiday_date"])
        holiday_dates = {str(getdate(h.holiday_date)) for h in holidays}

    import random
    start_date = getdate("2025-09-01")
    end_date = getdate(today())
    current = start_date
    count = 0

    while current <= end_date:
        if current.weekday() in (5, 6) or str(current) in holiday_dates:
            current = add_days(current, 1)
            continue

        rand = random.random()
        if rand < 0.88:
            status = "Present"
        elif rand < 0.96:
            status = "Absent"
        else:
            status = "Present"

        att = frappe.get_doc({
            "doctype": "Student Attendance",
            "student": student_id,
            "student_group": sg_name,
            "date": str(current),
            "status": status,
        })
        att.insert()
        att.submit()
        count += 1
        current = add_days(current, 1)

    print(f"Created {count} attendance records")


def _create_study_materials():
    existing = frappe.get_all("Study Material", limit=1)
    if existing:
        print("Study materials already exist, skipping")
        return

    materials = [
        {"title": "Calculus Ch 4: Differentiation Rules", "course": "Advanced Mathematics", "topic_name": "Calculus", "category": "Lecture Notes"},
        {"title": "Algebra Complete Formula Sheet", "course": "Advanced Mathematics", "topic_name": "Algebra", "category": "Lecture Notes"},
        {"title": "Trigonometry Practice Problems", "course": "Advanced Mathematics", "topic_name": "Trigonometry", "category": "Question Bank"},
        {"title": "Annual Physics Syllabus 2025-26", "course": "Physics", "topic_name": "Mechanics", "category": "Syllabus"},
        {"title": "Newton's Laws Lab Manual", "course": "Physics", "topic_name": "Mechanics", "category": "Lab Manuals"},
        {"title": "Thermodynamics Quick Revision Notes", "course": "Physics", "topic_name": "Thermodynamics", "category": "Lecture Notes"},
        {"title": "Optics Question Bank - Mid Term", "course": "Physics", "topic_name": "Optics", "category": "Question Bank"},
        {"title": "Chemistry Lab Safety Protocol", "course": "Chemistry", "topic_name": "Organic Chemistry", "category": "Lab Manuals"},
        {"title": "Organic Chemistry Reaction Mechanisms", "course": "Chemistry", "topic_name": "Organic Chemistry", "category": "Lecture Notes"},
        {"title": "Periodic Table Reference Sheet", "course": "Chemistry", "topic_name": "Inorganic Chemistry", "category": "Syllabus"},
        {"title": "Cell Biology Diagrams & Notes", "course": "Biology", "topic_name": "Cell Biology", "category": "Lecture Notes"},
        {"title": "Genetics Problem Set", "course": "Biology", "topic_name": "Genetics", "category": "Question Bank"},
        {"title": "Poetry Analysis Notes - Shakespeare", "course": "English Literature", "topic_name": "Poetry Analysis", "category": "Lecture Notes"},
        {"title": "Essay Writing Guide", "course": "English Literature", "topic_name": "Essay Writing", "category": "Lecture Notes"},
        {"title": "Mid-Term History Sample Papers", "course": "History", "topic_name": "Modern History", "category": "Question Bank"},
        {"title": "Python Programming Basics", "course": "Computer Science", "topic_name": "Programming Basics", "category": "Lecture Notes"},
    ]

    for m in materials:
        topic_id = None
        if m.get("topic_name"):
            topic_id = frappe.db.get_value("Topic", {"topic_name": m["topic_name"]}, "name")

        frappe.get_doc({
            "doctype": "Study Material",
            "title": m["title"],
            "course": m["course"],
            "topic": topic_id,
            "category": m["category"],
            "file": "/assets/maxedu/sample.pdf",
            "file_type": "PDF",
            "file_size": "2.4 MB",
            "upload_date": add_days(today(), -random_int(1, 60)),
        }).insert()

    print(f"Created {len(materials)} study materials")


def _create_student_assignments(student_id):
    existing = frappe.get_all("Student Assignment", filters={"student": student_id}, limit=1)
    if existing:
        print("Assignments already exist, skipping")
        return

    assignments = [
        {"title": "Trigonometry Problem Set 4", "course": "Advanced Mathematics", "topic_name": "Trigonometry", "due_offset": 14, "difficulty": 80, "status": "Active"},
        {"title": "Calculus Integration Worksheet", "course": "Advanced Mathematics", "topic_name": "Calculus", "due_offset": 21, "difficulty": 75, "status": "Active"},
        {"title": "Mechanics Lab Report", "course": "Physics", "topic_name": "Mechanics", "due_offset": 10, "difficulty": 60, "status": "Active"},
        {"title": "Atomic Structure Lab Report", "course": "Chemistry", "topic_name": "Organic Chemistry", "due_offset": 7, "difficulty": 45, "status": "Active"},
        {"title": "Analysis of Shakespearean Sonnets", "course": "English Literature", "topic_name": "Poetry Analysis", "due_offset": -5, "difficulty": 60, "status": "Submitted"},
        {"title": "The Industrial Revolution Essay", "course": "History", "topic_name": "Modern History", "due_offset": -10, "difficulty": 90, "status": "Overdue"},
        {"title": "Cell Division Diagram Assignment", "course": "Biology", "topic_name": "Cell Biology", "due_offset": -15, "difficulty": 50, "status": "Evaluated"},
        {"title": "Python Programming Exercise 1", "course": "Computer Science", "topic_name": "Programming Basics", "due_offset": -20, "difficulty": 40, "status": "Evaluated"},
        {"title": "Genetics Punnett Square Practice", "course": "Biology", "topic_name": "Genetics", "due_offset": 5, "difficulty": 55, "status": "Active"},
        {"title": "Thermodynamics Numerical Problems", "course": "Physics", "topic_name": "Thermodynamics", "due_offset": -3, "difficulty": 85, "status": "Submitted"},
    ]

    for a in assignments:
        topic_id = None
        if a.get("topic_name"):
            topic_id = frappe.db.get_value("Topic", {"topic_name": a["topic_name"]}, "name")

        doc = frappe.get_doc({
            "doctype": "Student Assignment",
            "title": a["title"],
            "course": a["course"],
            "topic": topic_id,
            "student": student_id,
            "due_date": add_days(today(), a["due_offset"]),
            "difficulty": a["difficulty"],
            "status": a["status"],
        })

        if a["status"] == "Evaluated":
            doc.evaluated_score = 85 if "Cell" in a["title"] else 92
            doc.remarks = "Good work!" if doc.evaluated_score >= 85 else "Needs improvement"

        doc.insert()

    print(f"Created {len(assignments)} assignments")


def random_int(a, b):
    import random
    return random.randint(a, b)


if __name__ == "__main__":
    create_test_data()
