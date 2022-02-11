const smiles = Vue.component('smiles', {
  template: `
  <div id="input-header" class="container">
  <form @submit.prevent="submit">
      <div class="form-group" id="smiles-input">
          <input type="text" v-model="name" class="form-control" id="name" placeholder="Enter a SMILES string, e.g. 'CC1=CC(=CC(=C1)O)C'">
          <a class="btn btn-success" data-toggle="modal" data-target="#jsmewindow" onclick="drawfromSmiles('name')"><span class="glyphicon glyphicon-pencil" style="margin-right:10px"></span>Draw</a>
          <button type="submit" class="btn btn-success">
              Submit
          </button>
      </div>
      </form>
    <br>
  </div>
`,
props: ['name'],
methods : {
   submit(){
     router.push('/result/' +  this.name);
   }
}

});
