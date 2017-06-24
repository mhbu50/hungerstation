frappe.ui.form.on('Project', {
	onload: function(frm) {
    if(frm.doc.__islocal ) {
   var new_row1 = frm.add_child("tasks");
      new_row1.title = "Data Entry";
      var new_row2 = frm.add_child("tasks");
      new_row2.title = "QA";
      var new_row3 = frm.add_child("tasks");
      new_row3.title = "Control";
      var new_row4 = frm.add_child("tasks");
      new_row4.title = "Printer";
      var new_row5 = frm.add_child("tasks");
      new_row5.title = "Finance";

   }
}
});
