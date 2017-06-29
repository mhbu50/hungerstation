frappe.ui.form.on('Lead', {
// 	onload: function(frm) {
//     console.log("onload");
//     $("div>ul>li:nth-child(1)>a").remove();
//     $("a.ct-active").remove();
// },refresh: function(frm) {
//   console.log("refresh");
//   $("div>ul>li:nth-child(1)>a").remove();
//   $("a.ct-active").remove();
// },
onload_post_render: function(frm) {
  $("div.form-links").remove();
  $("div>ul>li:nth-child(1)>a").remove();
  $("div>ul>li:nth-child(3)>a").remove();
}
});
