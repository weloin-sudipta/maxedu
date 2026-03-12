frappe.ui.form.on("Book Issue", {
    refresh: function(frm) {
        // Filter book_isbn: only show copies of the selected book
        frm.set_query("book_isbn", function() {
            let filters = {
                book: frm.doc.book,
                copy_type: "Physical"
            };
            // On new records, only show available (not issued) copies
            if (frm.is_new()) {
                filters.is_issued = 0;
            }
            return { filters: filters };
        });
    },

    book: function(frm) {
        frm.set_value("book_isbn", "");
    },

    return_date: function(frm) {
        // Show a preview of fine when return date is set
        if (frm.doc.return_date && frm.doc.due_date) {
            let due = frappe.datetime.str_to_obj(frm.doc.due_date);
            let ret = frappe.datetime.str_to_obj(frm.doc.return_date);
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
