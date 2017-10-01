// Copyright (c) 2017, Accurate Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('City', {
  validate: function(frm) {
    frm.set_value("name1", frm.doc.name1.charAt(0).toUpperCase() + frm.doc.name1.slice(1));
  }
});
