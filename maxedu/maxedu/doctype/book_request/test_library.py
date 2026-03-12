"""
Library Management System – Test Suite
Run with:  bench run-tests --app maxedu --module maxedu.maxedu.doctype.book_request.test_library
"""
import frappe
import unittest
from frappe.utils import today, add_days, date_diff


class TestLibraryFlow(unittest.TestCase):

    # ──────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────

    def _make_member(self, member_type="Student"):
        """Create a Library Member and return the doc."""
        m = frappe.get_doc({
            "doctype": "Library Member",
            "member_type": member_type,
            "full_name": f"Test {member_type}",
            "email": frappe.generate_hash(length=6) + "@test.com",
            "phone": "9999999999",
            "join_date": today(),
            "expiry_date": add_days(today(), 365),
        })
        m.insert(ignore_permissions=True)
        self.addCleanup(
            frappe.delete_doc, "Library Member", m.name,
            force=True, ignore_permissions=True
        )
        return m

    def _make_book(self):
        """Create a Library Book."""
        b = frappe.get_doc({
            "doctype": "Library Book",
            "title": "Test Book " + frappe.generate_hash(length=4),
            "author": "Test Author",
        })
        b.insert(ignore_permissions=True)
        self.addCleanup(
            frappe.delete_doc, "Library Book", b.name,
            force=True, ignore_permissions=True
        )
        return b

    def _make_inventory(self, book_name, isbn=None, copy_type="Physical",
                        total_copies=2, borrow_period_days=14, fine_per_day=5):
        """Create a Library Book Inventory record."""
        inv = frappe.get_doc({
            "doctype": "Library Book Inventory",
            "book": book_name,
            "isbn": isbn or frappe.generate_hash(length=10).upper(),
            "copy_type": copy_type,
            "total_copies": total_copies,
            "available_copies": total_copies,
            "borrow_period_days": borrow_period_days,
            "fine_per_day": fine_per_day,
            "status": "Available",
        })
        inv.insert(ignore_permissions=True)
        self.addCleanup(
            frappe.delete_doc, "Library Book Inventory", inv.name,
            force=True, ignore_permissions=True
        )
        return inv

    def _make_request(self, member_name, book_name, request_type="Issue"):
        req = frappe.get_doc({
            "doctype": "Book Request",
            "member": member_name,
            "book": book_name,
            "request_date": today(),
            "request_type": request_type,
            "status": "Pending",
        })
        req.insert(ignore_permissions=True)
        self.addCleanup(
            frappe.delete_doc, "Book Request", req.name,
            force=True, ignore_permissions=True
        )
        return req

    def _create_issue(self, member_name, book_name, inv_name, due_days=14):
        issue = frappe.get_doc({
            "doctype": "Book Issue",
            "member": member_name,
            "book": book_name,
            "book_isbn": inv_name,
            "issue_date": today(),
            "due_date": add_days(today(), due_days),
            "fine_per_day": 5,
            "status": "Issued",
        })
        issue.insert(ignore_permissions=True)
        frappe.db.set_value("Library Book Inventory", inv_name, "is_issued", 1)
        current = frappe.db.get_value("Library Book Inventory", inv_name, "available_copies") or 0
        if current > 0:
            frappe.db.set_value("Library Book Inventory", inv_name, "available_copies", current - 1)
        self.addCleanup(
            frappe.delete_doc, "Book Issue", issue.name,
            force=True, ignore_permissions=True
        )
        return issue

    # ──────────────────────────────────────────────────────────────────
    # 1. Auto-naming tests
    # ──────────────────────────────────────────────────────────────────

    def test_library_member_student_id(self):
        m = self._make_member("Student")
        self.assertTrue(
            m.library_id.startswith("LIB-STU-"),
            f"Expected LIB-STU- prefix, got: {m.library_id}"
        )
        num_part = m.library_id.split("LIB-STU-")[1]
        self.assertEqual(len(num_part), 4)

    def test_library_member_instructor_id(self):
        m = self._make_member("Instructor")
        self.assertTrue(m.library_id.startswith("LIB-TCH-"))

    def test_library_member_staff_id(self):
        m = self._make_member("Staff")
        self.assertTrue(m.library_id.startswith("LIB-STF-"))

    def test_library_member_id_increments(self):
        m1 = self._make_member("Student")
        m2 = self._make_member("Student")
        n1 = int(m1.library_id.split("LIB-STU-")[1])
        n2 = int(m2.library_id.split("LIB-STU-")[1])
        self.assertEqual(n2, n1 + 1)

    # ──────────────────────────────────────────────────────────────────
    # 2. Inventory tests
    # ──────────────────────────────────────────────────────────────────

    def test_inventory_isbn_unique(self):
        book = self._make_book()
        isbn = frappe.generate_hash(length=10).upper()
        inv1 = self._make_inventory(book.name, isbn=isbn)
        with self.assertRaises(Exception):
            inv2 = frappe.get_doc({
                "doctype": "Library Book Inventory",
                "book": book.name,
                "isbn": isbn,   # duplicate
                "copy_type": "Physical",
                "total_copies": 1,
                "available_copies": 1,
            })
            inv2.insert(ignore_permissions=True)

    def test_physical_inventory_available_copies_set_on_insert(self):
        book = self._make_book()
        inv = self._make_inventory(book.name, total_copies=3)
        self.assertEqual(inv.available_copies, 3)

    def test_inventory_available_cannot_exceed_total(self):
        book = self._make_book()
        inv = self._make_inventory(book.name, total_copies=2)
        inv.available_copies = 5
        with self.assertRaises(frappe.ValidationError):
            inv.save()

    # ──────────────────────────────────────────────────────────────────
    # 3. Book Request → Issue flow
    # ──────────────────────────────────────────────────────────────────

    def test_approve_creates_book_issue(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name)

        req = self._make_request(member.name, book.name)
        req.status = "Approved"
        req.book_isbn = inv.name
        req.save(ignore_permissions=True)
        req.reload()

        self.assertEqual(req.status, "Issued")

        issue_name = frappe.db.get_value("Book Issue", {"book_request": req.name})
        self.assertIsNotNone(issue_name, "Book Issue was not created on Approval")

        is_issued = frappe.db.get_value("Library Book Inventory", inv.name, "is_issued")
        self.assertEqual(is_issued, 1)

        avail = frappe.db.get_value("Library Book Inventory", inv.name, "available_copies")
        self.assertEqual(avail, 1)  # started at 2 → 1

        # Cleanup issue before linked docs are deleted
        if issue_name:
            frappe.delete_doc("Book Issue", issue_name, force=True, ignore_permissions=True)

    def test_approve_without_isbn_throws(self):
        member = self._make_member()
        book = self._make_book()
        req = self._make_request(member.name, book.name)
        req.status = "Approved"
        req.book_isbn = None
        with self.assertRaises(frappe.ValidationError):
            req.save(ignore_permissions=True)

    def test_approve_already_issued_copy_throws(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name)
        frappe.db.set_value("Library Book Inventory", inv.name, "is_issued", 1)

        req = self._make_request(member.name, book.name)
        req.status = "Approved"
        req.book_isbn = inv.name
        with self.assertRaises(frappe.ValidationError):
            req.save(ignore_permissions=True)

        # Reset so cleanup doesn't choke on stale state
        frappe.db.set_value("Library Book Inventory", inv.name, "is_issued", 0)

    # ──────────────────────────────────────────────────────────────────
    # 4. Book Return flow
    # ──────────────────────────────────────────────────────────────────

    def test_return_on_time_no_fine(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name)
        issue = self._create_issue(member.name, book.name, inv.name, due_days=14)

        issue.return_date = today()
        issue.save(ignore_permissions=True)
        issue.reload()

        self.assertEqual(issue.status, "Returned")
        self.assertEqual(issue.total_fine or 0, 0)

    def test_return_late_calculates_fine(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name, fine_per_day=10)
        # due_days=-5 means due date is 5 days in the past
        issue = self._create_issue(member.name, book.name, inv.name, due_days=-5)

        issue.return_date = today()
        issue.save(ignore_permissions=True)
        issue.reload()

        self.assertEqual(issue.status, "Returned")
        self.assertGreater(issue.total_fine, 0, "Expected a fine for late return")
        self.assertEqual(issue.days_overdue, 5)
        self.assertEqual(issue.total_fine, 50)  # 5 days × ₹10

    def test_return_increments_available_copies(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name, total_copies=2)
        issue = self._create_issue(member.name, book.name, inv.name)

        avail_before = frappe.db.get_value("Library Book Inventory", inv.name, "available_copies")
        issue.return_date = today()
        issue.save(ignore_permissions=True)

        avail_after = frappe.db.get_value("Library Book Inventory", inv.name, "available_copies")
        self.assertEqual(avail_after, avail_before + 1)

    def test_return_marks_inventory_available(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name)
        issue = self._create_issue(member.name, book.name, inv.name)

        issue.return_date = today()
        issue.save(ignore_permissions=True)

        is_issued = frappe.db.get_value("Library Book Inventory", inv.name, "is_issued")
        self.assertEqual(is_issued, 0)

    # ──────────────────────────────────────────────────────────────────
    # 5. Overdue detection
    # ──────────────────────────────────────────────────────────────────

    def test_overdue_status_set_automatically(self):
        member = self._make_member()
        book = self._make_book()
        inv = self._make_inventory(book.name)
        issue = self._create_issue(member.name, book.name, inv.name, due_days=-3)

        # No return_date → should become Overdue
        issue.save(ignore_permissions=True)
        issue.reload()
        self.assertEqual(issue.status, "Overdue")

    # ──────────────────────────────────────────────────────────────────
    # 6. Reservation flow
    # ──────────────────────────────────────────────────────────────────

    def test_reservation_created_when_no_copies(self):
        member = self._make_member()
        book = self._make_book()
        req = self._make_request(member.name, book.name, request_type="Reservation")
        req.status = "Approved"
        req.save(ignore_permissions=True)
        req.reload()
        self.assertEqual(req.status, "Reserved")

    def test_duplicate_reservation_throws(self):
        member = self._make_member()
        book = self._make_book()

        req1 = self._make_request(member.name, book.name, request_type="Reservation")
        req1.status = "Approved"
        req1.save(ignore_permissions=True)
        req1.reload()

        req2 = self._make_request(member.name, book.name, request_type="Reservation")
        req2.status = "Approved"
        with self.assertRaises(frappe.ValidationError):
            req2.save(ignore_permissions=True)