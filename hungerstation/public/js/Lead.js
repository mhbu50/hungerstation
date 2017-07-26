frappe.ui.form.on('Lead', {
refresh: function(frm) {
    $("div.form-dashboard").remove();
  setTimeout(function(){
    $("div>ul>li>a:contains('Quotation')").remove();
    $("div>ul>li>a:contains('Customer')").remove();
  }, 150);
},validate:function(frm){
   frm.set_value("lead_name",frm.doc.company_name);
    console.log("validate done");
}
});
