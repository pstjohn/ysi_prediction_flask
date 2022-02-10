const result = Vue.component('result', {
  props: ['smiles'],
  template: `
<div v-if="named_smiles" class='container'>
  <h2>{{ named_smiles }}</h2>
  <div id='drawing' v-html="mol_svg"></div>

  <div v-if="exp_mean" id='ysi_reg'>
  	<div class="alert alert-success">
    	<p>
    	Measured YSI:
    	<em>{{ exp_mean }} &plusmn; {{ exp_std }} </em>
    	</p>
    </div>
  </div>

  <div id='ysi_reg'>
  	<p>
  	Estimated YSI:
  	<em>{{ mean }} &plusmn; {{ std }} </em>
  	<span v-if="outlier" class="badge badge-danger">Outlier</span>
  	<span v-else class="badge badge-success">Inlier</span>
  	</p>
  </div>

  <div v-if="outlier">
    <h3>Missing Fragments</h3>

    <div v-if="frag_missing_df.count" class='container'>
      <div id='frags' class="row">
      	<div v-for="key in Object.keys(frag_missing_df.count)" class="col-sm-6 col-md-6 media fragment border-1 rounded">
      		<div class='media-left' v-html="frag_missing_df.svg[key]"></div>
      		<div class="media-body">
      			<h4 class='media-heading'>{{ key }}</h4>
      			<p><strong>Count:</strong> {{ frag_missing_df.count[key] }}<br/>
      		</div>
      	</div>
      </div>
    </div>
  </div>

  <h3>Component Fragments</h3>

  <div v-if="frag_df.count" class='container'>
    <div id='frags' class="row">
    	<div v-for="key in Object.keys(frag_df.count)" class="col-sm-6 col-md-6 media fragment border-1 rounded">
    		<div class='media-left' v-html="frag_df.svg[key]"></div>
    		<div class="media-body">
    			<h4 class='media-heading'>{{ key }}</h4>
    			<p><strong>Count:</strong> {{ frag_df.count[key]}}<br/>
    			<strong>YSI:</strong> {{ frag_df.mean[key] }} &plusmn; {{ frag_df.std[key] }}<br/>
    			<strong>Training #:</strong> <router-link :to="{ name: 'frag', params: { frag_str: key}}">{{ frag_df.train_count[key] }}</router-link><br/>
    		</div>
    	</div>
    </div>
  </div>

  <div id='frags' class='container'>
  	<div class='col-6'>
  	</div>
  </div>
</div>
    `,
  data() {
    return {
      named_smiles: "",
      mol_svg: "",
      exp_mean: null,
      exp_std: null,
      mean: null,
      std: null,
      frag_missing_df: {},
      frag_df: {},
      outlier: false
      };
  },
  methods: {
    async get_data(){
      const urlpath = "/result/" + encodeURIComponent(this.$route.params.smiles);
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
