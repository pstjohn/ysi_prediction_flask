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
