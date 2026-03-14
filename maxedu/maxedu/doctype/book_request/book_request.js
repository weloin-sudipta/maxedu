frappe.ui.form.on("Book Request", {

    // onload: function(frm) {
    //     if (frm.doc.book && frm.doc.request_date && !frm.doc.due_date) {

    //         frappe.db.get_value(
    //             "Library Book Inventory",
    //             { book: frm.doc.book, copy_type: "Physical" },
    //             "borrow_period_days",
    //             function(r) {
    //                 if (r && r.borrow_period_days) {
    //                     let due = frappe.datetime.add_days(
    //                         frm.doc.request_date,
    //                         r.borrow_period_days
    //                     );
    //                     frm.set_value("due_date", due);
    //                 }
    //             }
    //         );

    //     }
    // },

    refresh: function (frm) {
        frm.set_query("book", function () {
            return {
                query: "maxedu.maxedu.doctype.book_request.book_request.get_available_books"
            };
        });
    }

});