frappe.ui.form.on("Book Request", {

    // onload: function(frm) {
    //     if (!frm.doc.request_date) {
    //         frm.set_value("request_date", frappe.datetime.get_today());
    //     }
    // },

    refresh: function(frm) {
        frm.set_query("book", function () {
            return {
                query: "maxedu.maxedu.doctype.book_request.book_request.get_available_books"
            };
        });
    }

});