const smiles = Vue.component('smiles', {
  template: `
  <div id="input-header" class="container">
      <div class="form-group" id="smiles-input">
        <input type="text" class="form-control" id="name" name="name" placeholder="Enter a SMILES string, e.g. 'CC1=CC(=CC(=C1)O)C'">
        <a class="btn btn-success" data-toggle="modal" data-target="#jsmewindow" onclick="drawfromSmiles('name')"><span class="glyphicon glyphicon-pencil" style="margin-right:10px"></span>Draw</a>
        <button id="smiles-button" class="btn btn-success" disabled="disabled">Submit</button>
      </div>
    <br>
    <div class="alert alert-warning" id="smiles-error">
    </div>
  </div>
`
});
