import numpy as np
import pandas as pd
from sklearn.linear_model import BayesianRidge

from ysi_flask.colors import husl_palette
from ysi_flask.fragdecomp.chemical_conversions import canonicalize_smiles
from ysi_flask.fragdecomp.fragment_decomposition import (
    FragmentError,
    draw_fragment,
    draw_mol_svg,
    get_fragments,
)
from ysi_flask.fragdecomp.nullspace_outlier import NullspaceClassifier

try:
    from flask import Markup

    flask = True
except ImportError:
    flask = False

# Grab the most recent YSI data from github
ysi = pd.read_csv(
    "https://raw.githubusercontent.com/pstjohn/YSIs_for_prediction/master/ysi.csv"
)

# we use this for weighting, so provide a 5% relative error if none given
ysi.YSI_err = ysi.YSI_err.fillna(np.abs(ysi.YSI * 0.05))

# Parse ysi fragments
frags = ysi.SMILES.apply(get_fragments).fillna(0).astype(int)

# Fit YSI model
nullspace = NullspaceClassifier()
nullspace.fit(frags)

bridge = BayesianRidge(fit_intercept=False)

bridge.fit(frags, ysi.YSI, sample_weight=1 / ysi.YSI_err)

frag_means, frag_stds = bridge.predict(np.eye(frags.shape[1]), return_std=True)
beta = pd.DataFrame(
    np.vstack([frag_means, frag_stds]).T, index=frags.columns, columns=["mean", "std"]
)
beta = beta.round(1)
beta["train_count"] = frags.sum(0)

ysi = ysi.set_index("SMILES")


def predict(smiles):
    try:
        assert smiles is not None
        fragments = get_fragments(smiles)
    except Exception:
        raise FragmentError

    isoutlier = False

    # See if an experimental value exists
    try:
        ysi_exp = ysi.loc[canonicalize_smiles(smiles)]
        exp_mean = round(ysi_exp.YSI, 1)
        exp_std = round(ysi_exp.YSI_err, 1)
        exp_name = ysi_exp.Species

    except KeyError:
        exp_mean = None
        exp_std = None
        exp_name = None

    # Make sure all the fragments are found in the database
    if not fragments.index.isin(frags.columns).all():
        isoutlier = True

    # Put the fragments in the correct order
    reindexed_frags = fragments.reindex(frags.columns).fillna(0).astype(int)

    # Make sure the fragments are not present in nonlinear combinations of database
    if nullspace.predict(reindexed_frags):
        isoutlier = True

    # Predict based off previous regression
    mean, std = bridge.predict(reindexed_frags.values.reshape(1, -1), return_std=True)

    # process fragments for display
    colors = husl_palette(n_colors=len(fragments))
    frag_df = pd.DataFrame(fragments, columns=["count"])
    frag_df["color"] = colors
    if flask:
        frag_df["svg"] = frag_df.apply(
            lambda x: Markup(draw_fragment(x.name, x.color)), 1
        )
    frag_df = frag_df.join(beta, how="left").fillna(0)

    return mean[0], std[0], isoutlier, frag_df, exp_mean, exp_std, exp_name


def return_fragment_matches(frag_str):
    """return a database of molecules matching the input fragment"""

    matches = ysi[(frags[frag_str] != 0).values].reset_index()
    color = (0.9677975592919913, 0.44127456009157356, 0.5358103155058701)

    if len(matches) > 20:
        matches = matches.sample(20)

    matches["svg"] = matches.SMILES.apply(
        lambda x: Markup(
            draw_mol_svg(x, figsize=(80, 80), color_dict={frag_str: color})
        )
    )

    return beta.loc[frag_str], matches.round(1)


def predict_apply(smiles):
    """function optimized for pandas series of SMILES strings"""

    try:
        fragments = get_fragments(smiles)
    except Exception:
        raise FragmentError

    isoutlier = False

    # See if an experimental value exists
    try:
        ysi_exp = ysi.loc[canonicalize_smiles(smiles)]
        exp_mean = ysi_exp.YSI
        exp_std = ysi_exp.YSI_err

    except KeyError:
        exp_mean = None
        exp_std = None

    # Make sure all the fragments are found in the database
    if not fragments.index.isin(frags.columns).all():
        isoutlier = True

    # Put the fragments in the correct order
    reindexed_frags = fragments.reindex(frags.columns).fillna(0).astype(int)

    # Make sure the fragments are not present in nonlinear combinations of database
    if nullspace.predict(reindexed_frags):
        isoutlier = True

    # Predict based off previous regression
    mean, std = bridge.predict(reindexed_frags.values.reshape(1, -1), return_std=True)

    prediction_type = "prediction" if not isoutlier else "outlier"
    if exp_mean:
        prediction_type = "experiment"

    return pd.Series(
        {
            "YSI": exp_mean if exp_mean else mean[0],
            "YSI_err": exp_std if exp_mean else std[0],
            "pred_type": prediction_type,
        },
        name=smiles,
    )
