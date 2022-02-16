// Vue app
const api_server = "http://localhost:8889";

// Components loaded in prior scripts
const routes = [
  { path: '/', component: home },
  { path: '/result/:smiles', component: result, props: true, name: 'result' },
  { path: '/frag/:frag_str', component: frag, props: true, name: 'frag' }
];
// Router
const router = new VueRouter({
  routes // short for `routes: routes`
});
// Vue
const app = new Vue({
  router
}).$mount('#app');

// Need a global jsmeApplet
function jsmeOnLoad() {
  jsmeApplet = new JSApplet.JSME("jsme_container", "768px", "400px");
}
// Window resizing needs to trigger applet resizing
$('#jsmewindow').on('shown.bs.modal', function (e) {
  jsmeApplet.setWidth($("#jsme_container").width() + "px");
});
window.onresize = e => { jsmeApplet.setWidth($("#jsme_container").width() + "px") };

// Calls to api server with standard error handling
// function call_api_server( urlpath ) {
//   $('#smiles-error').hide();
//   return $.ajax({
//     url: api_server + urlpath,
//     statusCode: {
//       0: function(responseObject, textStatus, jqXHR) {
//         $('#smiles-error').text("No response from api server " + api_server);
//         $('#smiles-error').show();
//       },
//       404: function(responseObject, textStatus, jqXHR) {
//         $('#smiles-error').text("API server not found at " + api_server);
//         $('#smiles-error').show();
//       }
//     }
//   });
// }
//
// SMILES text entry
// $('#name').on("input", function (){
//   if ($(this).val().trim() != ""){
//     $('#smiles-button').removeAttr("disabled");
//   } else {
//     $('#smiles-button').attr("disabled", "disabled");
//   }
// });
//
// // SMILES submit button
// $('#smiles-button').on('click', function () {
//     const smiles = encodeURIComponent($('#name').val().trim());
//     router.push({ path: '/result/'+smiles });
// });
//
// $(document).ready( function(){
//   $('#smiles-error').hide();
// });
