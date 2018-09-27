from flask import Flask, render_template, request, redirect, Markup, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

import urllib.parse

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

from ysipred.prediction import predict, return_fragment_matches
from fragdecomp.fragment_decomposition import draw_mol_svg, FragmentError, draw_fragment
from fragdecomp.chemical_conversions import canonicalize_smiles

class ReusableForm(Form):
    name = TextField('SMILES:', validators=[validators.required()])

def quote(x):
    return urllib.parse.quote(x, safe='')

@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    return render_template('index.html', form=form)


@app.route("/result", methods=['GET', 'POST'])
def result():
    form = ReusableForm(request.form)
    smiles = request.args['name']
    can_smiles = canonicalize_smiles(smiles)

    try:
        # Here's the real prediction step. We calculated the predicted mean +/-
        # std, draw the whole molecule, and return a dataframe of the component
        # fragments.

        mean, std, outlier, frag_df, exp_mean, exp_std, exp_name = predict(can_smiles)
        svg = Markup(draw_mol_svg(can_smiles, figsize=(150, 150),
                                  color_dict=dict(zip(frag_df.index, frag_df.color))))

        mean = round(mean, 1)
        std = round(std, 1)

        frag_df['frag_link'] = frag_df.index
        frag_df['frag_link'] = frag_df['frag_link'].apply(quote)

        if exp_name:
            smiles += ' ({})'.format(exp_name)

        return render_template(
            "result.html", form=form, smiles=smiles, mol_svg=svg, mean=mean,
            std=std, frag_df=frag_df[frag_df['train_count'] > 0], 
            outlier=outlier, exp_mean=exp_mean, exp_std=exp_std,
            frag_missing_df=frag_df[frag_df['train_count'] == 0])

    except FragmentError:
        # Most likely a poorly-formed SMILES string.

        flash('Error: "{}" SMILES string invalid. Please enter a valid SMILES '
              'without quotes.'.format(smiles))
        return render_template('index.html', form=form)


@app.route("/frag", methods=['GET', 'POST'])
def frag():

    form = ReusableForm(request.form)
    frag_str = request.args['name']

    color = (0.9677975592919913, 0.44127456009157356, 0.5358103155058701)
    frag_svg = Markup(draw_fragment(frag_str, color))

    # try:

    fragment_row, matches = return_fragment_matches(frag_str)
    matches['smiles_link'] = matches.SMILES.apply(quote)

    return render_template(
        "frag.html", form=form, frag_str=frag_str, frag_svg=frag_svg,
        fragrow=fragment_row, matches=matches)

    # except KeyError:
        # flash('Error: "{}" fragment invalid.'.format(frag_str))
        # return render_template('index.html', form=form)


