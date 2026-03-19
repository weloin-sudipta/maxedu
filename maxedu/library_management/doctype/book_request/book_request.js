// Copyright (c) 2024, weloin and contributors
// For license information, please see license.txt

frappe.ui.form.on("Book Request", {
	setup: function(frm) {
		frm.set_query("member", function() {
			if (frm.doc.library) {
				return {
					filters: {
						library: frm.doc.library
					}
				};
			}
		});
	}
});
