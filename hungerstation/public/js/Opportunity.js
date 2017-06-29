
frappe.ui.form.on('Opportunity', {
refresh:function(frm){
  console.log("onload_post_render");
  $("div>ul>li>a:contains('Quotation')").remove();
  $("div.form-links").remove();
  if(!frm.doc.__islocal && frm.doc.status!=="Lost") {
    console.log("ccccccccccc");
      frm.add_custom_button(__('Customer'),
        function() {
          frm.trigger("make_customer");
        }, __("Make"));
  }
},
make_customer: function(frm) {
  frappe.model.open_mapped_doc({
    method: "hungerstation.hungerstation.tools.make_customer",
    frm: cur_frm
  })
}
});
