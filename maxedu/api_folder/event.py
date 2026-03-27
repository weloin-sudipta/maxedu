import frappe
from maxedu.api import format_time


@frappe.whitelist()
def get_all_events():
    """
    Get calendar events for the currently logged-in student.
    If student exists, filters events where the student belongs to one of the event's student groups.
    If no student record found, returns all events without any filtering.
    Returns structured event data with child table info (tags, programs, student groups).
    """
    try:
        student = frappe.db.get_value(
            "Student",
            {"student_email_id": frappe.session.user},
            "name"
        )

        if not student:
            # Also try matching by user field
            student = frappe.db.get_value("Student", {"user": frappe.session.user}, "name")

        if student:
            # Fetch events where the student is in one of the linked student groups
            events = frappe.db.sql(
                """
                SELECT DISTINCT ce.name, ce.event_name, ce.date, ce.start_time,
                       ce.end_time, ce.room, ce.description
                FROM `tabCalendar event` ce
                LEFT JOIN `tabCalendar Student Group` csg ON csg.parent = ce.name
                LEFT JOIN `tabStudent Group Student` sgs ON sgs.parent = csg.student_group
                WHERE sgs.student = %s
                   OR NOT EXISTS (
                       SELECT 1 FROM `tabCalendar Student Group` csg2
                       WHERE csg2.parent = ce.name
                   )
                ORDER BY ce.date ASC
                """,
                student,
                as_dict=True
            )
        else:
            # No student found - return all events without filtering
            events = frappe.db.sql(
                """
                SELECT DISTINCT ce.name, ce.event_name, ce.date, ce.start_time,
                       ce.end_time, ce.room, ce.description
                FROM `tabCalendar event` ce
                ORDER BY ce.date ASC
                """,
                as_dict=True
            )

        if not events:
            return {"success": True, "events": [], "tags": []}

        event_names = [e.name for e in events]

        # Batch fetch child table data for all events
        event_tags_raw = frappe.db.get_all(
            "Calendar Event Tag",
            filters={"parent": ["in", event_names]},
            fields=["parent", "event_tag"]
        )

        event_programs_raw = frappe.db.get_all(
            "Calendar Program",
            filters={"parent": ["in", event_names]},
            fields=["parent", "program"]
        )

        event_student_groups_raw = frappe.db.get_all(
            "Calendar Student Group",
            filters={"parent": ["in", event_names]},
            fields=["parent", "student_group"]
        )

        # Build lookup maps
        tags_by_event = {}
        for t in event_tags_raw:
            tags_by_event.setdefault(t.parent, []).append(t.event_tag)

        programs_by_event = {}
        for p in event_programs_raw:
            programs_by_event.setdefault(p.parent, []).append(p.program)

        groups_by_event = {}
        for g in event_student_groups_raw:
            groups_by_event.setdefault(g.parent, []).append(g.student_group)

        # Build room name map
        room_ids = list({e.room for e in events if e.room})
        room_map = {}
        if room_ids:
            for r in frappe.db.get_all("Room", filters={"name": ["in", room_ids]}, fields=["name", "room_name"]):
                room_map[r.name] = r.room_name

        # Build formatted event list
        formatted_events = []
        all_tags = set()

        for event in events:
            event_tags = tags_by_event.get(event.name, [])
            all_tags.update(event_tags)

            formatted_events.append({
                "name": event.name,
                "event_name": event.event_name or "Untitled Event",
                "date": str(event.date) if event.date else None,
                "start_time": format_time(event.start_time) if event.start_time else None,
                "end_time": format_time(event.end_time) if event.end_time else None,
                "room": room_map.get(event.room, event.room) if event.room else None,
                "description": event.description or "",
                "tags": event_tags,
                "programs": programs_by_event.get(event.name, []),
                "student_groups": groups_by_event.get(event.name, []),
            })

        return {
            "success": True,
            "events": formatted_events,
            "tags": sorted(all_tags)
        }

    except Exception as e:
        frappe.log_error(f"Error in get_all_events: {str(e)}", "Calendar Events API Error")
        return {"success": False, "events": [], "tags": [], "error": str(e)}

@frappe.whitelist()
def get_all_event_tags():
    """
    Return all distinct event tags used across Calendar Events.
    """
    try:
        tags = frappe.db.get_all(
            "Calendar Event Tag",
            fields=["event_tag"],
            distinct=True,
            pluck="event_tag"
        )
        return {"success": True, "tags": sorted(tags) if tags else []}
    except Exception as e:
        frappe.log_error(f"Error in get_all_event_tags: {str(e)}", "Calendar Event Tags API Error")
        return {"success": False, "tags": [], "error": str(e)}