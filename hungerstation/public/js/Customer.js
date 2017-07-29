frappe.ui.form.on('Customer', {

            validate: function(frm) {
                console.log("on validate ");
                console.log("frm", frm.doc);
                copy_rows_to(frm,"rest_branches",frm.doc.vendor_comany);
                copy_rows_to(frm,"banks");
                copy_rows_to(frm,"attachment");
          //       frappe.run_serially([
          //   () => copy_rows_to(frm,"banks"),
          //   () => copy_rows_to(frm,"rest_branches",frm.doc.vendor_comany),
          //   () => copy_rows_to(frm,"attachment")
          // ]);
              }
            });

            function copy_rows_to(frm,table,parent) {
              // debugger;
              var docs = [];
              $.each(frm.doc[table], function(index, row) {
                  if (row.__unsaved) {
                    row.parenttype = "Task";
                    var restaurant_name ="";
                    delete row.name;
                    if (parent){
                      restaurant_name = parent;
                    }else{
                      restaurant_name = row.parent;
                  }
                    var row1 = jQuery.extend({}, row);
                    row1.parent = restaurant_name +" - Documents submission";
                    docs.push(row1);
                    var row2 = jQuery.extend({}, row);
                    row2.parent = restaurant_name +" - Data Entry";
                    docs.push(row2);
                    var row3 = jQuery.extend({}, row);
                    row3.parent = restaurant_name +" - QA";
                    docs.push(row3);
                    if (frm.doc.area == "AAA"){
                    var row4 = jQuery.extend({}, row);
                    row4.parent = restaurant_name +" - AAA Reviewer";
                    docs.push(row4);
                  }
                  //get Restaurant Opp to check if it has OD
                  frappe.call({
                    "method": "frappe.client.get_list",
                    args: {
                      doctype: "Restaurant Opp",
                      fields:"*",
                      filters: [
                        ["parent","=", frm.doc.opportunity]
                      ]
                    },
                    callback: function(data) {
                      console.log("data",data);
                      $.each(data.message,function(i,r){
                        if(r.type == "OD"){
                            var row5 = jQuery.extend({}, row);
                            row5.parent = restaurant_name +" - Delivery Approval";
                            docs.push(row5);
                        }
                      });
                    }
                  });
                    var row6 = jQuery.extend({}, row);
                    row6.parent = restaurant_name +" - Control";
                    docs.push(row6);
                    var row7 = jQuery.extend({}, row);
                    row7.parent = restaurant_name +" - Printer";
                    docs.push(row7);
                    var row8 = jQuery.extend({}, row);
                    row8.parent = restaurant_name +" - Finance";
                    docs.push(row8);
                  }
              });
              console.log("docs",docs);
              setTimeout(function(){
              frappe.call({
                      method: "frappe.client.insert_many",
                      args: {docs:JSON.stringify(docs)
                      },
                      callback: function(r) {
                        // console.log("r",r);
                      }
                  });
                }, 200);
            }
