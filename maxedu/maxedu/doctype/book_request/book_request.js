frappe.ui.form.on("Book Request", {
    refresh: function(frm) {
        // Filter: only show available books (those which have physical copies not all issued)
        frm.set_query("book", function() {
            // For Issue requests, show books that have at least one available physical copy
            if (frm.doc.request_type === "Issue") {
                return {
                    query: "maxedu.maxedu.doctype.book_request.book_request.get_available_books"
                };
            }
            return {};
        });

        // Filter book_isbn: only show availble physical copies of the selected book
        frm.set_query("book_isbn", function() {
            return {
                filters: {
                    book: frm.doc.book,
                    is_issued: 0,
                    copy_type: "Physical"
                }
            };
        });
    },

    request_type: function(frm) {
        // Clear book and isbn when request type changes
        frm.set_value("book", "");
        frm.set_value("book_isbn", "");
    },

    book: function(frm) {
        // Clear ISBN selection when book changes
        frm.set_value("book_isbn", "");
    }
});
