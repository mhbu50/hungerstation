frappe.ui.form.on('Opportunity', {
    refresh: function(frm) {
      $("div>ul>li>a:contains('Quotation')").remove();
      $("div.form-links").remove();

if (!frm.doc.__islocal && frm.doc.status !== "Lost") {
      frm.add_custom_button(__('Customer'), function() {
                  frappe.call({
                          "method": "hungerstation.hungerstation.tools.make_customer",
                          args: {doc:frm.doc},
                      callback: function(data)
                      {
                          frappe.route_options = {'lead_name': data.message}
                          frappe.set_route("List", "Customer");
                      }
                  });
          }, __("Make"));

        }

      }
});



//
// console.log("onload_post_render");
//
//
//     console.log("ccccccccccc");
//
//   }
