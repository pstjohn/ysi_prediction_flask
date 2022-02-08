const frag = Vue.component('frag', {
  props: ['frag_str'],
  template: `
<div class='container'>
  <h2>{{ frag_str }}</h2>

  <div id='drawing' v-html="frag_svg"></div>

  <div id='ysi_reg'>
  	<p>
  	Regressed YSI:
  	<em>{{ fragrow['mean'] }} &plusmn; {{ fragrow['std'] }} </em>
  	</p>
  </div>

  <h3>Containing Molecules</h3>

  <div class='container'>
  <div v-if="matches.svg" id='frags' class="row">
  	<div v-for="key in Object.keys(matches.svg)" class="col-sm-6 col-md-6 media fragment border-1 rounded">
  		<div class='media-left' v-html="matches.svg[key]"></div>
  		<div class="media-body">
  			<h4 class='media-heading'>{{ matches.Species[key] }}</h4>
  			<p><strong>SMILES:</strong> <router-link :to="{ name: 'result', params: { smiles: matches.SMILES[key]}}">{{ matches.SMILES[key] }}</router-link><br/>
  			<strong>YSI:</strong> {{ matches.YSI[key] }} &plusmn; {{ matches.YSI_err[key] }}<br/>
  		</div>
  	</div>
  </div>
  </div>
</div>
    `,
  data() {
    return {
      frag_str: "",
      frag_svg: "",
      fragrow: {},
      matches: {},
      status: ''
      };
  },
  methods: {
    async get_data(){
      const urlpath = "/frag/" + encodeURIComponent(this.$route.params.frag_str);
      var response;
      try {
        response = await call_api_server( urlpath );
      } catch (e) {
        $('#smiles-error').text(e.responseJSON['detail']);
        $('#smiles-error').show();
        return;
      }
      Object.assign(this, response);
    }
  },
  created() {
    this.get_data();
  },
  watch: {
    // call again the method if the route changes
    '$route': 'get_data'
  }

});
