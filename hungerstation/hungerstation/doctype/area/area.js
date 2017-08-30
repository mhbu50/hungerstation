// Copyright (c) 2017, Accurate Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Area', {
	validate: function(frm) {
		frm.set_value("area",frm.doc.area.charAt(0).toUpperCase() + frm.doc.area.slice(1));
		frm.set_value("area_code",frm.doc.area_code.toUpperCase());
	}
});
