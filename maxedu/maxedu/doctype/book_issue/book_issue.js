frappe.ui.form.on("Book Issue", {
    refresh: function (frm) {
        // Filter book_isbn: only show copies of the selected book
        // frm.set_query("book_isbn", function() {
        //     let filters = {
        //         book: frm.doc.book,
        //         copy_type: "Physical"
        //     };
        //     // On new records, only show available (not issued) copies
        //     if (frm.is_new()) {
        //         filters.is_issued = 0;
        //     }
        //     return { filters: filters };
        // });
    },

    book: function (frm) {
        if (frm.doc.book) {
            frappe.call({
                method: "maxedu.maxedu.doctype.book_issue.book_issue.get_book_isbns",
                args: { book: frm.doc.book },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        frm.set_df_property("book_isbn", "options", r.message);
                    } else {
                        frm.set_df_property("book_isbn", "options", []);
                        frappe.msgprint(__("No physical copies with ISBNs available for this book."));
                    }
                    if (!r.message || !r.message.includes(frm.doc.book_isbn)) {
                        frm.set_value("book_isbn", ""); // Clear if invalid
                    }
                }
            });
        } else {
            frm.set_df_property("book_isbn", "options", []);
            frm.set_value("book_isbn", "");
        }
    },

    book_request: function (frm) {
        // Only run if a book request is selected
        if (!frm.doc.book_request) return;

        frappe.db.get_doc("Book Request", frm.doc.book_request).then(doc => {
            // Set member and member_name
            frm.set_value("member", doc.member);
            frm.set_value("member_name", doc.member_name);

            // Set book and book title
            frm.set_value("book", doc.book);
            frm.set_value("book_title", doc.book_title);

            // Set issue_date from request date
            if (doc.request_date) {
                frm.set_value("issue_date", doc.request_date);
            }

            // Trigger book fetch to populate ISBNs
            if (frm.doc.book) {
                frm.trigger("book");
            }
            // Set Book ISBN if already selected in request
            if (doc.book_isbn) {
                // The options will be set by the book trigger asynchronously,
                // so we might need a slight delay or rely on the user to select
                setTimeout(() => {
                    frm.set_value("book_isbn", doc.book_isbn);
                }, 500);
            }

            // Optionally, set due date based on borrow period
            if (doc.borrow_period_days) {
                frm.set_value("due_date", doc.due_date);
            }

            // Set status default
            frm.set_value("status", "Issued");
        });
    },

    return_date: function (frm) {
        // Show a preview of fine when return date is set
        if (frm.doc.return_date && frm.doc.due_date) {
            let diff = frappe.datetime.get_day_diff(frm.doc.return_date, frm.doc.due_date);
            if (diff > 0) {
                let fine = diff * (frm.doc.fine_per_day || 0);
                frappe.show_alert({
                    message: `⚠️ Book is ${diff} day(s) late. Estimated fine: ${format_currency(fine)}`,
                    indicator: "orange"
                }, 8);
            }
        }
    }
});