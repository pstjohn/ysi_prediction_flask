const home = Vue.component('home', {
  template: `
<div class="container">
  <h3>Group-contribution predictions of Yield Sooting Index (YSI)</h3>
  <p>This tool predicts the Yield Sooting Index of a compound as a function of its carbon types. To use, enter a SMILES string above (or use the drawing tool) and press submit. Experimental measurements, when available, are also displayed.</p>

  <div id='affiliation'>
  	<p> For more info, see our publication:<br/>
  	Das, D. D., St. John, P. C., McEnally, C. S., Kim, S., &amp; Pfefferle, L. D. (2018). Measuring and predicting sooting tendencies of oxygenates, alkanes, alkenes, cycloalkanes, and aromatics on a unified scale. <em>Combustion and Flame</em>, 190, 349–364. <a href="https://doi.org/10.1016/j.combustflame.2017.12.005">10.1016/j.combustflame.2017.12.005</a></p>
  	<video autoplay="" loop="" controls class="" style="max-width: 100%; min-height: 410px;"><source type="video/mp4" src="//i.imgur.com/csXBEtP.mp4"/></video>
  	<p> Website by <em><a href="https://www.nrel.gov/research/peter-stjohn.html" >Peter St. John</a>, <a href="https://www.nrel.gov/research/michael-bartlett.html">Michael Bartlett</a>, and <a href="https://www.nrel.gov/research/seonah-kim.html" >Seonah Kim</a></em></p>
	</div>
</div>
`
});
