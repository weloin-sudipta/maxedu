
import frappe
from frappe import _
from functools import lru_cache


def format_time(time_obj):
    """Format time/timedelta/string to HH:MM string"""
    if not time_obj:
        return ""
    if isinstance(time_obj, str):
        return time_obj
    if hasattr(time_obj, 'strftime'):
        return time_obj.strftime("%H:%M")
    total_seconds = int(time_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def create_error_response(error, context="API Error", **defaults):
    """Create standardized error response"""
    frappe.log_error(f"Error in {context}: {str(error)}", context)
    return {"success": False, "error": str(error), **defaults}

@lru_cache(maxsize=64)
def _cached_grading_scale_details(scale_name: str):
    intervals = frappe.db.get_all(
        "Grading Scale Interval",
        filters={"parent": scale_name},
        fields=["grade_code", "threshold"],
        order_by="threshold desc"
    )
    serialized = tuple(
        (interval.grade_code, float(interval.threshold))
        for interval in intervals
    )
    failing_grade = serialized[-1][0] if serialized else None
    return serialized, failing_grade


def get_grading_scale_details(grading_scale):
    """Return grading scale intervals and lowest threshold grade for quick reuse."""
    if not grading_scale:
        return {"intervals": [], "failing_grade": None}

    intervals, failing_grade = _cached_grading_scale_details(str(grading_scale))
    return {
        "intervals": [{"grade": grade, "threshold": threshold} for grade, threshold in intervals],
        "failing_grade": failing_grade
    }

def get_current_student():
    """
    Get the student record for the currently logged-in user
    Returns student name or None if not found
    """
    user = frappe.session.user
    return frappe.db.get_value("Student", {"user": user}, "name")

def get_student_enrollment(student, fields=None):
    """
    Get the current program enrollment for a student
    Returns enrollment data or None if not found

    Args:
        student: Student ID
        fields: List of fields to fetch or single field name
    """
    if fields is None:
        fields = ["program", "name"]

    return frappe.db.get_value(
        "Program Enrollment",
        {"student": student, "docstatus": 1},
        fields,
        as_dict=True if isinstance(fields, list) else False,
        order_by="enrollment_date desc"
    )

@lru_cache(maxsize=128)
def _cached_student_groups_for_program(student: str, program: str):
    if not student or not program:
        return ()

    student_group = frappe.qb.DocType("Student Group")
    student_group_students = frappe.qb.DocType("Student Group Student")

    student_groups_query = (
        frappe.qb.from_(student_group)
        .inner_join(student_group_students)
        .on(student_group.name == student_group_students.parent)
        .select(student_group_students.parent)
        .where(student_group_students.student == student)
        .where(student_group.program == program)
        .where(student_group_students.active == 1)
        .run()
    )

    if not student_groups_query:
        return ()

    return tuple(sg[0] for sg in student_groups_query)


def get_student_groups_for_program(student, program):
    """
    Get student groups for a student in a specific program
    Returns list of student group names

    Args:
        student: Student ID
        program: Program name
    """
    if not student or not program:
        return []

    return list(_cached_student_groups_for_program(student, program))


get_student_groups_for_program.cache_clear = _cached_student_groups_for_program.cache_clear


@lru_cache(maxsize=128)
def _cached_instructor_name(instructor_id: str):
    return frappe.db.get_value("Instructor", instructor_id, "instructor_name") or "TBD"


def get_instructor_name(instructor_id):
    """Get instructor full name from ID with safe default"""
    if not instructor_id:
        return "TBD"
    return _cached_instructor_name(str(instructor_id))


get_instructor_name.cache_clear = _cached_instructor_name.cache_clear

def get_next_class_time(course_code, program, student):
    """
    Get the next scheduled class time for a specific course
    Returns formatted datetime string or None if no upcoming class
    """
    try:
        from frappe.utils import now_datetime, get_datetime

        current_datetime = now_datetime()

        student_groups = get_student_groups_for_program(student, program)
        if not student_groups:
            return None

        next_schedule = frappe.db.get_value(
            "Course Schedule",
            {
                "course": course_code,
                "program": program,
                "student_group": ["in", student_groups],
                "schedule_date": [">=", current_datetime.date()]
            },
            ["schedule_date", "from_time", "to_time", "room"],
            as_dict=True,
            order_by="schedule_date asc, from_time asc"
        )

        if not next_schedule or not next_schedule.schedule_date:
            return None

        schedule_datetime = get_datetime(f"{next_schedule.schedule_date} {next_schedule.from_time}")

        if schedule_datetime < current_datetime:
            next_future_schedule = frappe.db.get_value(
                "Course Schedule",
                {
                    "course": course_code,
                    "program": program,
                    "student_group": ["in", student_groups],
                    "schedule_date": [">", current_datetime.date()]
                },
                ["schedule_date", "from_time", "to_time", "room"],
                as_dict=True,
                order_by="schedule_date asc, from_time asc"
            )

            if not next_future_schedule:
                return None

            next_schedule = next_future_schedule
            schedule_datetime = get_datetime(f"{next_schedule.schedule_date} {next_schedule.from_time}")

        day_name = schedule_datetime.strftime("%A")
        date_str = schedule_datetime.strftime("%b %d")

        return {
            "datetime": schedule_datetime.isoformat(),
            "day": day_name,
            "date": date_str,
            "time": format_time(next_schedule.from_time),
            "location": next_schedule.room or "TBD"
        }

    except Exception as e:
        frappe.log_error(f"Error in get_next_class_time: {str(e)}", "Next Class Time Error")
        return None





@frappe.whitelist()
def update_student_profile(first_name, last_name, phone, bio):
    """
    Update both User and Student profile information
    Updates the User record and linked Student record with new name and contact info
    """
    try:
        user = frappe.session.user

        user_doc = frappe.get_doc("User", user)
        user_doc.update({"first_name": first_name, "last_name": last_name, "phone": phone, "bio": bio})
        user_doc.save(ignore_permissions=True)

        student_id = get_current_student()
        if student_id:
            student_doc = frappe.get_doc("Student", student_id, ignore_permissions=True)
            student_doc.update({"first_name": first_name, "last_name": last_name})
            if phone:
                student_doc.student_mobile_number = phone
            student_doc.save(ignore_permissions=True)

            return {"success": True, "message": "Profile updated successfully", "user_updated": True, "student_updated": True}

        return {"success": True, "message": "User profile updated successfully", "user_updated": True, "student_updated": False}

    except Exception as e:
        return create_error_response(e, "Update Student Profile Error", message="Failed to update profile")

@frappe.whitelist()
def get_student_results():
    """
    Get academic results for the currently logged-in student
    Returns results grouped by academic term with course-wise grades
    """
    default_stats = {"total_courses": 0, "courses_passed": 0, "courses_failed": 0}
    default_response = {"success": True, "message": "", "results": {}, "academic_terms": [], "statistics": default_stats, "grading_scales": {}}

    try:
        student = get_current_student()
        if not student:
            return {**default_response, "success": False, "message": "No student record found for current user"}

        assessment_results = frappe.db.get_all(
            "Assessment Result",
            filters={"student": student, "docstatus": 1},
            fields=["name", "course", "academic_term", "academic_year", "grade", "total_score", "maximum_score", "assessment_group", "program", "grading_scale"],
            order_by="academic_year desc, academic_term desc"
        )

        if not assessment_results:
            return {**default_response, "message": "No assessment results found"}
        
        # Prefetch grading scale intervals and derive failing grade per scale
        grading_scales_data = {}
        failing_grade_by_scale = {}
        unique_grading_scales = {r.grading_scale for r in assessment_results if r.grading_scale}
        for grading_scale_name in unique_grading_scales:
            scale_details = get_grading_scale_details(grading_scale_name)
            grading_scales_data[grading_scale_name] = scale_details["intervals"]
            failing_grade = scale_details.get("failing_grade")
            if failing_grade:
                failing_grade_by_scale[grading_scale_name] = failing_grade
        
        academic_terms = list(dict.fromkeys([
            r.academic_term or r.academic_year or "No Term"
            for r in assessment_results
        ]))

        # Prefetch course names to avoid per-row lookups
        course_scores = {}
        unique_courses = {r.course for r in assessment_results if r.course}
        course_map = {}
        if unique_courses:
            for c in frappe.db.get_all("Course", filters={"name": ["in", list(unique_courses)]}, fields=["name", "course_name"]):
                course_map[c.name] = c.course_name
        for result in assessment_results:
            term = result.academic_term or result.academic_year or "No Term"
            course_key = result.course

            if term not in course_scores:
                course_scores[term] = {}

            course_name = course_map.get(result.course, result.course)

            if result.maximum_score and result.maximum_score > 0:
                percentage = round((float(result.total_score or 0) / float(result.maximum_score)) * 100, 2)
            else:
                percentage = 0

            # Determine pass/fail using precomputed failing grade map when available
            status = "Pending"
            if result.grade and result.grading_scale and result.grading_scale in failing_grade_by_scale:
                status = "Failed" if result.grade == failing_grade_by_scale[result.grading_scale] else "Passed"

            course_data = {
                "id": result.name,
                "courseCode": result.course,
                "courseName": course_name,
                "grade": result.grade or "N/A",
                "totalScore": float(result.total_score or 0),
                "maximumScore": float(result.maximum_score or 0),
                "percentage": percentage,
                "status": status,
                "assessmentGroup": result.assessment_group or "Assessment",
                "gradingScale": result.grading_scale  # Send grading scale name to frontend
            }

            if course_key not in course_scores[term] or percentage > course_scores[term][course_key]["percentage"]:
                course_scores[term][course_key] = course_data

        results_by_term = {term: list(courses.values()) for term, courses in course_scores.items()}

        all_percentages = [c["percentage"] for courses in course_scores.values() for c in courses.values()]
        courses_passed = sum(1 for courses in course_scores.values() for c in courses.values() if c["status"] == "Passed")
        courses_failed = sum(1 for courses in course_scores.values() for c in courses.values() if c["status"] == "Failed")
        avg_percentage = round(sum(all_percentages) / len(all_percentages), 2) if all_percentages else 0
        
        avg_grade = "N/A"
        if avg_percentage and assessment_results:
            grading_scale = next((r.grading_scale for r in assessment_results if r.grading_scale), None)
            if grading_scale and grading_scale in grading_scales_data:
                intervals = grading_scales_data[grading_scale]
                for interval in intervals:
                    if avg_percentage >= float(interval["threshold"]):
                        avg_grade = interval["grade"]
                        break
                else:
                    avg_grade = intervals[-1]["grade"] if intervals else "N/A"

        statistics = {
            "total_courses": len(all_percentages),
            "courses_passed": courses_passed,
            "courses_failed": courses_failed,
            "average_percentage": avg_percentage,
            "average_grade": avg_grade
        }

        return {
            "success": True, 
            "results": results_by_term, 
            "academic_terms": academic_terms, 
            "statistics": statistics,
            "grading_scales": grading_scales_data  # Send all grading scale intervals to frontend
        }

    except Exception as e:
        return create_error_response(e, "Student Results API Error", results={}, academic_terms=[], statistics=default_stats, grading_scales={})

def get_grade_point_value(grade):
    """Get numeric grade point value for a letter grade (0-4 scale)"""
    if not grade:
        return 0.0

    grade_points = {
        "A+": 4.0, "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0, "D-": 0.7,
        "F": 0.0, "E": 0.0
    }
    return grade_points.get(grade.upper(), 0.0)

def determine_grade_status(grade, grading_scale=None):
    """
    Determine if a grade is passing or failing based on the grading scale
    In the Education app, the last grade (lowest threshold) is typically the failing grade
    All other grades are considered passing
    
    Example: A, B, C, D = Pass; F = Fail
    """
    if not grade:
        return "Pending"
    
    try:
        scale_to_use = grading_scale
        if not scale_to_use:
            scale_to_use = frappe.db.get_value(
                "Grading Scale",
                {"docstatus": 1},
                "name",
                order_by="creation desc"
            )

        if scale_to_use:
            scale_details = get_grading_scale_details(scale_to_use)
            failing_grade = scale_details.get("failing_grade")
            if failing_grade:
                return "Failed" if grade == failing_grade else "Passed"
            if scale_details.get("intervals"):
                return "Passed"

        return "Pending"
        
    except Exception as e:
        frappe.log_error(f"Error in determine_grade_status: {str(e)}", "Grade Status Determination Error")
        return "Pending"

def get_grade_from_grading_scale(grading_scale, percentage):
    """
    Get grade letter from percentage score using the Education app's grading scale
    This uses the same logic as the Education app's get_grade() function
    
    Args:
        grading_scale: Name of the Grading Scale document
        percentage: Score percentage (0-100)
    
    Returns:
        Grade code (e.g., 'A', 'B+', 'C', etc.)
    """
    try:
        if not grading_scale:
            return "N/A"

        scale_details = get_grading_scale_details(grading_scale)
        intervals = scale_details.get("intervals", [])

        if intervals:
            for interval in intervals:
                if percentage >= float(interval["threshold"]):
                    return interval["grade"]
            return intervals[-1]["grade"]
        
        return "N/A"

    except Exception as e:
        frappe.log_error(f"Error in get_grade_from_grading_scale: {str(e)}", "Grade Calculation Error")
        return "N/A"

@frappe.whitelist()
def get_student_profile_stats():
    """
    Get quick stats for student profile page
    Returns enrollment counts and certificate information
    """
    default_response = {"success": True, "stats": {"total_courses": 0, "completed_courses": 0, "certificates": 0}}

    try:
        student = get_current_student()
        if not student:
            return {**default_response, "success": False, "message": "No student record found"}

        total_courses = frappe.db.count("Course Enrollment", {"student": student})

        completed_courses = 0
        course_enrollments = frappe.db.get_all(
            "Course Enrollment",
            filters={"student": student},
            fields=["course"],
            pluck="course"
        )

        if course_enrollments:
            assessment_results = frappe.db.get_all(
                "Assessment Result",
                filters={"student": student, "docstatus": 1, "course": ["in", course_enrollments]},
                fields=["course", "grade", "grading_scale", "creation"],
                order_by="creation desc"
            )

            latest_results_by_course = {}
            for result in assessment_results:
                course_code = result.course
                if course_code and course_code not in latest_results_by_course:
                    latest_results_by_course[course_code] = result

            for course in course_enrollments:
                latest = latest_results_by_course.get(course)
                if not latest or not latest.grade:
                    continue

                if latest.grading_scale:
                    failing_grade = get_grading_scale_details(latest.grading_scale).get("failing_grade")
                    if failing_grade is not None:
                        if latest.grade != failing_grade:
                            completed_courses += 1
                        continue

                if determine_grade_status(latest.grade, latest.grading_scale) == "Passed":
                    completed_courses += 1

        return {
            "success": True,
            "stats": {
                "total_courses": total_courses,
                "completed_courses": completed_courses
            }
        }

    except Exception as e:
        return create_error_response(e, "Student Profile Stats API Error", stats={"total_courses": 0, "completed_courses": 0, "certificates": 0})

@frappe.whitelist()
def get_student_recent_activity():
    """
    Get recent activity for student profile page
    Returns a list of recent activities (enrollments, completions, assessments)
    """
    default_response = {"success": True, "activities": []}

    try:
        student = get_current_student()
        if not student:
            return {**default_response, "success": False, "message": "No student record found"}

        activities = []

        cutoff_date = frappe.utils.add_days(frappe.utils.today(), -30)

        recent_enrollments = frappe.db.get_all(
            "Course Enrollment",
            filters={
                "student": student,
                "enrollment_date": [">=", cutoff_date]
            },
            fields=["course", "enrollment_date", "creation"],
            order_by="creation desc",
            limit=5
        )
        # Prefetch course names used in enrollments and results
        recent_results = frappe.db.get_all(
            "Assessment Result",
            filters={
                "student": student,
                "docstatus": 1,
                "creation": [">=", cutoff_date]
            },
            fields=["course", "grade", "creation", "assessment_group", "grading_scale"],
            order_by="creation desc",
            limit=5
        )
        course_ids = {e.course for e in recent_enrollments} | {r.course for r in recent_results}
        course_map = {}
        if course_ids:
            for c in frappe.db.get_all("Course", filters={"name": ["in", list(course_ids)]}, fields=["name", "course_name"]):
                course_map[c.name] = c.course_name

        for enrollment in recent_enrollments:
            course_name = course_map.get(enrollment.course, enrollment.course)
            activities.append({
                "title": f"Enrolled in {course_name}",
                "time": get_relative_time(enrollment.creation),
                "icon": "book-open",
                "color": "bg-purple-600",
                "timestamp": enrollment.creation
            })

        for result in recent_results:
            course_name = course_map.get(result.course, result.course)
            status = determine_grade_status(result.grade, result.grading_scale)
            if status == "Passed":
                activities.append({
                    "title": f"Completed {course_name}",
                    "time": get_relative_time(result.creation),
                    "icon": "check-circle",
                    "color": "bg-green-600",
                    "timestamp": result.creation
                })
            else:
                activities.append({
                    "title": f"Assessed in {course_name}",
                    "time": get_relative_time(result.creation),
                    "icon": "file-text",
                    "color": "bg-blue-600",
                    "timestamp": result.creation
                })

        if frappe.db.exists("DocType", "Certificate"):
            recent_certificates = frappe.db.get_all(
                "Certificate",
                filters={
                    "student": student,
                    "docstatus": 1,
                    "creation": [">=", cutoff_date]
                },
                fields=["name", "creation"],
                order_by="creation desc",
                limit=3
            )

            for cert in recent_certificates:
                activities.append({
                    "title": "Earned Achievement Badge",
                    "time": get_relative_time(cert.creation),
                    "icon": "award",
                    "color": "bg-yellow-600",
                    "timestamp": cert.creation
                })

        activities.sort(key=lambda x: x["timestamp"], reverse=True)

        for activity in activities:
            activity.pop("timestamp", None)

        activities = activities[:5]

        if not activities:
            activities.append({
                "title": "Welcome to MaxEdu!",
                "time": "Recently",
                "icon": "user",
                "color": "bg-blue-600"
            })

        return {"success": True, "activities": activities}

    except Exception as e:
        return create_error_response(e, "Student Recent Activity API Error", activities=[])

def get_relative_time(datetime_str):
    """Convert datetime to relative time string (e.g., '2 hours ago', '3 days ago')"""
    try:
        from frappe.utils import get_datetime, now_datetime, time_diff_in_hours, time_diff_in_seconds

        dt = get_datetime(datetime_str)
        now = now_datetime()
        diff_seconds = time_diff_in_seconds(now, dt)

        if diff_seconds < 60:
            return "Just now"
        elif diff_seconds < 3600:
            minutes = int(diff_seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif diff_seconds < 86400:
            hours = int(diff_seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff_seconds < 604800:
            days = int(diff_seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        else:
            weeks = int(diff_seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"

    except Exception as e:
        frappe.log_error(f"Error in get_relative_time: {str(e)}")
        return "Recently"


@frappe.whitelist()
def get_student_calendar_events():
    """
    Get calendar events for the currently logged-in student
    Filters events based on the student's program
    Returns events with date, time, location, and program information
    """
    default_response = {"success": True, "events": []}
    
    try:
        student = get_current_student()
        if not student:
            return {**default_response, "success": False, "message": "No student record found"}
        
        # Get student's program enrollment
        enrollment = get_student_enrollment(student, fields=["program", "name"])
        if not enrollment or not enrollment.get("program"):
            return {**default_response, "message": "No program enrollment found"}
        
        student_program = enrollment.get("program")
        
        # Fetch all calendar events
        events = frappe.db.get_all(
            "Calendar event",
            fields=["name", "event_name", "date", "start_time", "end_time", "room"],
            order_by="date asc"
        )
        
        # Prefetch room names for events with rooms
        filtered_events = []
        room_ids = list({e.room for e in events if getattr(e, "room", None)}) if events else []
        room_map = {}
        if room_ids:
            for r in frappe.db.get_all("Room", filters={"name": ["in", room_ids]}, fields=["name", "room_name"]):
                room_map[r.name] = r.room_name

        for event in events:
            # Get program child table records to check if event has program restrictions
            event_programs = frappe.db.get_all(
                "Calendar Program",
                filters={"parent": event.name},
                fields=["program"],
                pluck="program"
            )

            # If programs are specified, only show if student's program is in the list
            if event_programs and student_program not in event_programs:
                continue

            # Get room name if available
            room_name = room_map.get(event.room) if event.room else None

            # Format event data
            filtered_events.append({
                "id": event.name,
                "title": event.event_name,
                "date": event.date,
                "time": f"{format_time(event.start_time)} - {format_time(event.end_time)}" if event.start_time and event.end_time else None,
                "startTime": format_time(event.start_time),
                "endTime": format_time(event.end_time),
                "location": room_name or (event.room if event.room else None),
                "description": event.event_name,
                "color": "blue"  # Default color, can be customized based on event type
            })
        
        return {
            "success": True,
            "events": filtered_events,
            "student_program": student_program
        }
        
    except Exception as e:
        return create_error_response(e, "Calendar Events API Error", events=[])

@frappe.whitelist()
def get_student_dashboard_data():
    default_response = {
        "success": True,
        "student_info": None,
        "schedule": [],
        "courses": [],
        "fees": {"fees": [], "total_outstanding": 0, "currency": "USD"},
        "attendance": {"percentage": 0, "total_days": 0, "present_days": 0, "absent_days": 0},
        "gpa": {"score_percentage": 0, "total_courses": 0},
        "assignments": []
    }

    try:
        # Get current user
        user = frappe.session.user
        
        # Fetch student record
        student = frappe.db.get_value(
            "Student",
            {"user": user},
            ["name", "first_name", "last_name", "student_name", "student_email_id", "student_mobile_number"],
            as_dict=True
        )
        
        if not student:
            return {**default_response, "success": False, "message": "No student record found"}
        
        student_id = student.name
        
        # Fetch user image
        user_image = frappe.db.get_value("User", user, "user_image")
        
        # Fetch program enrollment
        enrollment = frappe.db.get_value(
            "Program Enrollment",
            {"student": student_id, "docstatus": ["<", 2]},
            ["name", "program", "academic_year", "academic_term", "student_batch_name", "enrollment_date"],
            as_dict=True,
            order_by="enrollment_date desc"
        )
        
        # Build student info
        student_info = {
            "name": student.student_name or f"{student.first_name} {student.last_name or ''}".strip(),
            "studentId": student_id,
            "program": enrollment.program if enrollment else "Not Enrolled",
            "semester": (enrollment.academic_term or enrollment.academic_year or "N/A") if enrollment else "N/A",
            "image": user_image or "",
            "academicYear": enrollment.academic_year if enrollment else None,
            "academicTerm": enrollment.academic_term if enrollment else None,
            "studentBatch": enrollment.student_batch_name if enrollment else None
        }
        
        # Fetch all data in parallel using the existing helper functions
        # We'll call the internal logic directly to avoid redundant student lookups
        
        # Schedule data - Using Class Schedule
        schedule_data = []
        try:
            if enrollment and enrollment.program:
                # Get class schedules for the student's program
                class_schedules = frappe.db.get_all(
                    "Class Schedule",
                    fields=[
                        "name",
                        "course",
                        "instructor",
                        "program",
                        "`from`",
                        "`to`",
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                        "sunday"
                    ],
                    filters={"program": enrollment.program}
                )
                
                # Map days to their checkbox field names
                day_mapping = {
                    "Monday": "monday",
                    "Tuesday": "tuesday",
                    "Wednesday": "wednesday",
                    "Thursday": "thursday",
                    "Friday": "friday",
                    "Saturday": "saturday",
                    "Sunday": "sunday"
                }
                
                # Prefetch course names and rooms for all schedules
                course_ids = {s.course for s in class_schedules if s.course}
                course_map = {}
                room_map = {}
                if course_ids:
                    for c in frappe.db.get_all("Course", filters={"name": ["in", list(course_ids)]}, fields=["name", "course_name", "room"]):
                        course_map[c.name] = c.course_name
                        room_map[c.name] = c.room or "TBD"

                # Expand each class schedule into individual day schedules
                for schedule in class_schedules:
                    course_name = course_map.get(schedule.course, schedule.course)
                    # Get room/location from prefetch
                    location = room_map.get(schedule.course, "TBD")
                    
                    # For each day that's checked, create a schedule entry
                    for day_name, day_field in day_mapping.items():
                        if schedule.get(day_field) == 1:  # Day is checked
                            schedule_data.append({
                                "courseName": course_name,
                                "courseCode": schedule.course,
                                "instructor": get_instructor_name(schedule.instructor),
                                "dayOfWeek": day_name,
                                "startTime": format_time(schedule.get("from")),
                                "endTime": format_time(schedule.get("to")),
                                "location": location
                            })
        except Exception as e:
            frappe.log_error(f"Error fetching schedule in dashboard: {str(e)}")
        
        # Courses data
        courses_data = []
        try:
            if enrollment:
                course_enrollments = frappe.db.get_all(
                    "Course Enrollment",
                    filters={"student": student_id},
                    fields=["course", "program", "enrollment_date"],
                    order_by="enrollment_date desc"
                )
                # Prefetch course names
                course_ids = {ce.course for ce in course_enrollments if ce.course}
                course_map = {}
                if course_ids:
                    for c in frappe.db.get_all("Course", filters={"name": ["in", list(course_ids)]}, fields=["name", "course_name"]):
                        course_map[c.name] = c.course_name

                # Prefetch instructors per course+program
                schedule_instructors = {}
                if course_enrollments:
                    sched = frappe.db.get_all(
                        "Course Schedule",
                        filters={"program": enrollment.program, "course": ["in", list(course_ids)]},
                        fields=["course", "instructor"]
                    )
                    for s in sched:
                        # last one wins; acceptable for display
                        schedule_instructors[s.course] = s.instructor

                # Prefetch latest grade per course for the student
                grades = frappe.db.get_all(
                    "Assessment Result",
                    filters={"student": student_id, "docstatus": 1, "course": ["in", list(course_ids)]},
                    fields=["course", "grade", "creation", "grading_scale"],
                    order_by="creation desc"
                )
                latest_grade = {}
                for g in grades:
                    if g.course not in latest_grade:
                        latest_grade[g.course] = g.grade or "N/A"

                for ce in course_enrollments:
                    name = course_map.get(ce.course, ce.course)
                    instructor_id = schedule_instructors.get(ce.course)
                    grade = latest_grade.get(ce.course, "N/A")
                    next_class = get_next_class_time(ce.course, ce.program, student_id)
                    courses_data.append({
                        "id": ce.course,
                        "name": name,
                        "code": ce.course,
                        "teacher": get_instructor_name(instructor_id),
                        "grade": grade,
                        "next_class": next_class
                    })
        except Exception as e:
            frappe.log_error(f"Error fetching courses in dashboard: {str(e)}")
        
        # Fees data
        fees_data = {"fees": [], "total_outstanding": 0, "currency": "USD"}
        try:
            default_currency = frappe.defaults.get_global_default("currency") or "USD"
            invoices = frappe.db.get_all(
                "Sales Invoice",
                filters={"student": student_id, "docstatus": ["!=", 2]},
                fields=["name", "posting_date", "due_date", "status", "grand_total", "outstanding_amount", "currency", "remarks", "customer_name"],
                order_by="posting_date desc"
            )
            
            total_outstanding = sum(inv.get("outstanding_amount", 0) for inv in invoices)
            
            fee_list = []
            for inv in invoices:
                fee_structure = inv.get("remarks", "")[:50] if inv.get("remarks") else f"Fee for {inv.customer_name}" if inv.get("customer_name") else "Tuition Fee"
                
                fee_list.append({
                    "name": inv.name,
                    "posting_date": inv.posting_date,
                    "due_date": inv.due_date,
                    "status": inv.status,
                    "grand_total": float(inv.grand_total or 0),
                    "outstanding_amount": float(inv.outstanding_amount or 0),
                    "paid_amount": float(inv.grand_total or 0) - float(inv.outstanding_amount or 0),
                    "currency": inv.currency,
                    "fee_structure": fee_structure,
                    "remarks": inv.remarks or ""
                })
            
            fees_data = {
                "fees": fee_list,
                "total_outstanding": float(total_outstanding),
                "currency": invoices[0].currency if invoices else default_currency
            }
        except Exception as e:
            frappe.log_error(f"Error fetching fees in dashboard: {str(e)}")
        
        # Attendance data
        attendance_data = {"percentage": 0, "total_days": 0, "present_days": 0, "absent_days": 0}
        try:
            attendance_records = frappe.db.get_all(
                "Student Attendance",
                filters={"student": student_id, "docstatus": 1},
                fields=["status"]
            )
            
            if attendance_records:
                total_days = len(attendance_records)
                present_days = sum(1 for r in attendance_records if r.status == "Present")
                absent_days = sum(1 for r in attendance_records if r.status == "Absent")
                leave_days = sum(1 for r in attendance_records if r.status == "Leave")
                attended_days = present_days + leave_days
                percentage = round((attended_days / total_days * 100), 2) if total_days > 0 else 0
                
                attendance_data = {
                    "percentage": percentage,
                    "total_days": total_days,
                    "present_days": present_days,
                    "absent_days": absent_days,
                    "leave_days": leave_days
                }
        except Exception as e:
            frappe.log_error(f"Error fetching attendance in dashboard: {str(e)}")
        
        # GPA/Score data
        gpa_data = {"score_percentage": 0, "total_courses": 0}
        try:
            if enrollment:
                filters = {"student": student_id, "docstatus": 1}
                if enrollment.academic_term:
                    filters["academic_term"] = enrollment.academic_term
                elif enrollment.academic_year:
                    filters["academic_year"] = enrollment.academic_year
                
                assessment_results = frappe.db.get_all(
                    "Assessment Result",
                    filters=filters,
                    fields=["course", "total_score", "maximum_score"],
                    order_by="creation desc"
                )
                
                if assessment_results:
                    course_scores = {}
                    for result in assessment_results:
                        if result.maximum_score and result.maximum_score > 0:
                            percentage = (float(result.total_score or 0) / float(result.maximum_score)) * 100
                            if result.course not in course_scores or percentage > course_scores[result.course]:
                                course_scores[result.course] = percentage
                    
                    if course_scores:
                        avg_percentage = sum(course_scores.values()) / len(course_scores)
                        gpa_data = {
                            "score_percentage": round(avg_percentage, 1),
                            "total_courses": len(course_scores)
                        }
        except Exception as e:
            frappe.log_error(f"Error fetching GPA in dashboard: {str(e)}")
        
        # Assignments data
        assessment_data = []
        try:
            if enrollment:
                from frappe.utils import getdate, today, add_days
                
                student_groups = get_student_groups_for_program(student_id, enrollment.program)
                
                if student_groups:
                    today_date = getdate(today())
                    future_date = add_days(today_date, 30)
                    
                    assessment_plans = frappe.db.get_all(
                        "Assessment Plan",
                        filters={
                            "student_group": ["in", student_groups],
                            "schedule_date": ["between", [today_date, future_date]],
                            "docstatus": ["!=", 2]
                        },
                        fields=["name", "assessment_name", "assessment_group", "course", "schedule_date", "from_time", "room"],
                        order_by="schedule_date asc, from_time asc"
                    )
                    
                    for plan in assessment_plans:
                        schedule_date = getdate(plan.schedule_date)
                        course_name = frappe.db.get_value("Course", plan.course, "course_name") or plan.course
                        
                        description = course_name
                        if plan.from_time:
                            description += f" • {format_time(plan.from_time)}"
                        if plan.room:
                            description += f" • {plan.room}"
                        
                        assessment_data.append({
                            "id": plan.name,
                            "day": schedule_date.strftime("%d"),
                            "month": schedule_date.strftime("%b").upper(),
                            "title": plan.assessment_name or f"{plan.assessment_group} - {course_name}",
                            "description": description,
                            "date": plan.schedule_date
                        })
        except Exception as e:
            frappe.log_error(f"Error fetching assignments in dashboard: {str(e)}")
        
        return {
            "success": True,
            "student_info": student_info,
            "schedule": schedule_data,
            "courses": courses_data,
            "fees": fees_data,
            "attendance": attendance_data,
            "gpa": gpa_data,
            "assessments": assessment_data
        }
        
    except Exception as e:
        return create_error_response(
            e,
            "Student Dashboard API Error",
            student_info=None,
            schedule=[],
            courses=[],
            fees={"fees": [], "total_outstanding": 0, "currency": "USD"},
            attendance={"percentage": 0},
            gpa={"score_percentage": 0},
            assignments=[]
        )# Get user role
        
@frappe.whitelist()
def get_user_role(user):
    roles = frappe.get_roles(user)
    if "Student" in roles:
        return "Student"
    elif "Instructor" in roles:
        return "Instructor"
    elif "Administrator" in roles:
        return "Administrator"
    else:
        return "User"

@frappe.whitelist()
def generate_routine(generator_name):
    from ortools.sat.python import cp_model
    import frappe.utils
    
    gen = frappe.get_doc("Routine Generator", generator_name)
    
    try:
        model = cp_model.CpModel()
        
        # Data Extract
        classes = [d.student_group for d in gen.student_groups]
        days = [d.day for d in gen.days]
        periods = [d.period for d in gen.periods]
        
        # Teacher-Subject Mapping
        teacher_subject_map = {}
        teachers = set()
        subjects = set()
        for d in gen.instructor_map:
            if d.instructor not in teacher_subject_map:
                teacher_subject_map[d.instructor] = []
            if d.course not in teacher_subject_map[d.instructor]:
                teacher_subject_map[d.instructor].append(d.course)
            teachers.add(d.instructor)
            subjects.add(d.course)
            
        teachers = list(teachers)
        subjects = list(subjects)
        
        # Pairs
        teacher_subject_pairs = []
        for t in teachers:
            for s in teacher_subject_map.get(t, []):
                teacher_subject_pairs.append((t, s))
                
        if not teacher_subject_pairs:
            frappe.throw("No instructor-course mappings found.")
            
        pair_index = {i:p for i,p in enumerate(teacher_subject_pairs)}
        pair_reverse = {v:k for k,v in pair_index.items()}
        
        # Limits
        teacher_week_limit = {t: (gen.min_classes_per_instructor_per_week, gen.max_classes_per_instructor_per_week) for t in teachers}
        
        teacher_class_preference = {}
        for pref in gen.preferences:
            teacher_class_preference[(pref.instructor, pref.student_group)] = pref.weight
            
        locked_assignments = []
        for lk in gen.hard_locks:
            locked_assignments.append((lk.student_group, lk.day, lk.period, lk.instructor, lk.course))
            
        # Variables
        schedule = {}
        for c in classes:
            for d in days:
                for p in periods:
                    schedule[(c, d, p)] = model.NewIntVar(0, len(teacher_subject_pairs)-1, f"{c}_{d}_{p}")
                    
        # Teacher conflict (max 1 class at same time)
        for d in days:
            for p in periods:
                for t in teachers:
                    vars_same_time = []
                    for c in classes:
                        for i, (teacher, sub) in pair_index.items():
                            if teacher == t:
                                b = model.NewBoolVar(f"cf_{c}_{d}_{p}_{t}")
                                model.Add(schedule[(c,d,p)] == i).OnlyEnforceIf(b)
                                model.Add(schedule[(c,d,p)] != i).OnlyEnforceIf(b.Not())
                                vars_same_time.append(b)
                    model.Add(sum(vars_same_time) <= 1)
                    
        # Max 2 subjects per day (or dynamic)
        for c in classes:
            for d in days:
                for s in subjects:
                    subject_count = []
                    for p in periods:
                        for i, (t, sub) in pair_index.items():
                            if sub == s:
                                b = model.NewBoolVar(f"sc_{c}_{d}_{p}_{s}")
                                model.Add(schedule[(c,d,p)] == i).OnlyEnforceIf(b)
                                model.Add(schedule[(c,d,p)] != i).OnlyEnforceIf(b.Not())
                                subject_count.append(b)
                    model.Add(sum(subject_count) <= gen.max_classes_per_subject_per_day)
                    
        # Teacher max 2 classes per day
        for t in teachers:
            for d in days:
                daily = []
                for c in classes:
                    for p in periods:
                        for i, (teacher, sub) in pair_index.items():
                            if teacher == t:
                                b = model.NewBoolVar(f"dc_{t}_{d}_{c}_{p}")
                                model.Add(schedule[(c,d,p)] == i).OnlyEnforceIf(b)
                                model.Add(schedule[(c,d,p)] != i).OnlyEnforceIf(b.Not())
                                daily.append(b)
                model.Add(sum(daily) <= gen.max_classes_per_instructor_per_day)
                
        # Weekly Load
        for t in teachers:
            weekly = []
            for c in classes:
                for d in days:
                    for p in periods:
                        for i, (teacher, sub) in pair_index.items():
                            if teacher == t:
                                b = model.NewBoolVar(f"wk_{t}_{c}_{d}_{p}")
                                model.Add(schedule[(c,d,p)] == i).OnlyEnforceIf(b)
                                model.Add(schedule[(c,d,p)] != i).OnlyEnforceIf(b.Not())
                                weekly.append(b)
            min_l, max_l = teacher_week_limit[t]
            model.Add(sum(weekly) >= min_l)
            model.Add(sum(weekly) <= max_l)
            
        # Hard locks
        for c, d, p, t, s in locked_assignments:
            if (t,s) in pair_reverse:
                idx = pair_reverse[(t,s)]
                model.Add(schedule[(c,d,p)] == idx)
                
        # Objective & preferences
        score = []
        for (t,c), weight in teacher_class_preference.items():
            for d in days:
                for p in periods:
                    for i, (teacher, sub) in pair_index.items():
                        if teacher == t:
                            b = model.NewBoolVar(f"pref_{t}_{c}_{d}_{p}")
                            model.Add(schedule[(c,d,p)] == i).OnlyEnforceIf(b)
                            model.Add(schedule[(c,d,p)] != i).OnlyEnforceIf(b.Not())
                            score.append(b * weight)
                            
        model.Maximize(sum(score))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10
        result = solver.Solve(model)
        
        if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            # Clear old Course Schedules for these classes (Optional, or just create new ones)
            # For this MVP, we create Course Schedule records.
            for c in classes:
                frappe.db.delete("Course Schedule", {"student_group": c})
                
            from datetime import timedelta, datetime
            # Map "Mon", "Tue" to upcoming dates. For simplicity, just pick next week's dates.
            # We will just create a "Course Schedule" entry with generic times.
            day_map = {"Sun":0, "Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5, "Sat":6}
            
            # Find next Monday
            today = frappe.utils.nowdate()
            today_dt = frappe.utils.getdate(today)
            start_of_week = today_dt + timedelta(days=-today_dt.weekday(), weeks=1)
            
            for c in classes:
                for d in days:
                    target_date = start_of_week + timedelta(days=day_map.get(d,0)-1)
                    for p in periods:
                        idx = solver.Value(schedule[(c,d,p)])
                        t, s = pair_index[idx]
                        
                        # Handle Room dependency
                        default_room_name = f"Room {c}"
                        if not frappe.db.exists("Room", {"room_name": default_room_name}):
                            r = frappe.get_doc({"doctype": "Room", "room_name": default_room_name, "room_capacity": 50}).insert(ignore_permissions=True)
                            room_id = r.name
                        else:
                            room_id = frappe.db.get_value("Room", {"room_name": default_room_name}, "name")
                        
                        # Time slots assumption: period 1 = 9:00 AM
                        start_time = f"{8+p:02d}:00:00"
                        end_time = f"{9+p:02d}:00:00"
                        
                        sch = frappe.new_doc("Course Schedule")
                        sch.student_group = c
                        sch.instructor = t
                        sch.course = s
                        sch.room = room_id
                        sch.schedule_date = target_date
                        sch.from_time = start_time
                        sch.to_time = end_time
                        sch.insert(ignore_permissions=True)
                        
            gen.status = "Completed"
            gen.save(ignore_permissions=True)
            frappe.db.commit()
            return "Timetable Generated Successfully!"
        else:
            gen.status = "Failed"
            gen.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.throw("No feasible timetable could be generated with the given constraints.")
            
    except Exception as e:
        gen.status = "Failed"
        gen.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.throw(f"Error during generation: {str(e)}")

@frappe.whitelist()
def get_student_schedule():
    default_response = {"success": True, "timetable": {}}
    user = frappe.session.user
    student = frappe.db.get_value("Student", {"user": user}, "name")
    if not student:
        return {**default_response, "success": False, "message": "No student record found"}
        
    student_groups = frappe.db.get_all("Student Group Student", {"student": student, "active": 1}, pluck="parent")
    # For testing: if Edward isn't explicitly in class10, we'll fetch all or just one just to test
    if not student_groups:
        # fallback to the first active group for testing
        student_groups = [frappe.db.get_value("Student Group", {"docstatus": 0}, "name")]
        
    schedules = frappe.db.get_all(
        "Course Schedule",
        filters={"student_group": ["in", student_groups]},
        fields=["name", "course", "instructor", "schedule_date", "from_time", "to_time", "room", "student_group"],
        order_by="schedule_date asc, from_time asc"
    )
    
    from collections import defaultdict
    formatted = defaultdict(list)
    for s in schedules:
        day_name = frappe.utils.getdate(s.schedule_date).strftime("%A")
        course_name = frappe.db.get_value("Course", s.course, "course_name") or s.course
        instructor_name = frappe.db.get_value("Instructor", s.instructor, "instructor_name") or s.instructor

        formatted[day_name].append({
            "subject": course_name,
            "teacher": instructor_name,
            "startTime": format_time(s.from_time),
            "endTime": format_time(s.to_time),
            "room": s.room,
            "type": "Lecture"
        })
        
    return {"success": True, "timetable": dict(formatted), "student_group": student_groups[0] if student_groups else None}

