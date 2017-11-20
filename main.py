from flask import Flask, render_template, request, redirect, Markup, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

from frag_prediction.prediction import predict
from frag_prediction.fragment_decomposition import draw_mol_svg

class ReusableForm(Form):
    name = TextField('SMILES:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    return render_template('index.html', form=form)


@app.route("/result", methods=['GET', 'POST'])
def result():
    form = ReusableForm(request.form)
    smiles = request.args['name']

    try:
        mean, std, outlier, frag_df = predict(smiles)
        svg = Markup(draw_mol_svg(smiles, figsize=(150, 150),
                                  color_dict=dict(zip(frag_df.index, frag_df.color))))

        mean = round(mean, 1)
        std = round(std, 1)

    except Exception:
        flash('Error: "{}" SMILES string invalid. Please enter a valid SMILES without quotes.'.format(smiles))
        return render_template('index.html', form=form)

    return render_template(
        "result.html", form=form, smiles=smiles, mol_svg=svg, mean=mean,
        std=std, frag_df=frag_df[frag_df['train_count'] > 0], 
        outlier=outlier, frag_missing_df=frag_df[frag_df['train_count'] == 0])



if __name__ == "__main__":
    app.run()
