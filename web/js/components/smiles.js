const smiles = Vue.component('smiles', {
  template: `
<div class="container">
  <div id="input-header" class="container">
  <form @submit.prevent="submit">
      <div class="form-group" id="smiles-input">
          <input type="text" v-model="name" class="form-control" id="name" placeholder="Enter a SMILES string, e.g. 'CC1=CC(=CC(=C1)O)C'">
          <a class="btn btn-success" data-toggle="modal" data-target="#jsmewindow" @click="drawfromSmiles()"><span class="glyphicon glyphicon-pencil" style="margin-right:10px"></span>Draw</a>
          <button type="submit" class="btn btn-success">
              Submit
          </button>
      </div>
      </form>
    <br>
  </div>
  <!-- jsmewindow connected to the draw link by data-target -->
  <div class="modal fade" id="jsmewindow">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div id="jsme_container" class="modal-body" style="height:430px;">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
          <button type="button" class="btn btn-primary" data-dismiss="modal" @click="saveSmiles()">OK</button>
        </div>
      </div>
    </div>
  </div>
</div>`,
data() {
  return {
    name: ""
  }
},
methods : {
  drawfromSmiles() {
    if (this.name) {
      jsmeApplet.readGenericMolecularInput(this.name);
    } else {
      jsmeApplet.reset();
    }
  },
  saveSmiles() {
    this.name =  jsmeApplet.smiles();
  },
  submit(){
   router.push('/result/' +  this.name);
  }
}

});
