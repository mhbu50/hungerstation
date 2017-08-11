frappe.ui.form.on('Opportunity', {
    refresh: function(frm) {
      $("div>ul>li>a:contains('Quotation')").remove();
      $("div.form-dashboard").hide();
console.log("ddd = ",$("div>ul>li>a:contains('Customer')"));
if (!frm.doc.__islocal && frm.doc.status !== "Lost" && frm.doc.status !== "Converted"
&& $("div>ul>li>a:contains('Customer')").length == 0) {
      frm.add_custom_button(__('Customer'), function() {
                  frappe.call({
                          "method": "hungerstation.hungerstation.tools.make_customer",
                          args: {doc:frm.doc},
                      callback: function(data)
                      {
                          frm.set_value("status","Converted");
                          frm.set_value("converted_date",frappe.datetime.nowdate());
                          frm.save();
                          console.log("data.message = ",data.message);
                          frappe.route_options = {'lead_name': data.message}
                          frappe.set_route("List", "Customer");
                      }
                  });
          }, __("Make"));
        }
      }
});
