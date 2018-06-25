import os
import pandas as pd
import numpy as np
from flask import Markup

from fragdecomp.fragment_decomposition import get_fragments, draw_fragment, FragmentError
from fragdecomp.nullspace_outlier import NullspaceClassifier
from fragdecomp.chemical_conversions import canonicalize_smiles
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model.base import _rescale_data

from ysipred.colors import husl_palette


currdir = os.path.dirname(os.path.abspath(__file__))

# Load YSI data
ysi = pd.read_csv(currdir + '/YSIs_for_prediction/ysi.csv')

# Parse ysi fragments
frags = ysi.SMILES.apply(get_fragments).fillna(0).astype(int)

# Fit YSI model
nullspace = NullspaceClassifier()
nullspace.fit(frags)

bridge = BayesianRidge()

X, y = _rescale_data(frags, ysi.YSI, 1/ysi.YSI_err)  # Until sklearn 0.20
bridge.fit(X, y)

frag_means, frag_stds = bridge.predict(np.eye(frags.shape[1]), return_std=True)
beta = pd.DataFrame(np.vstack([frag_means, frag_stds]).T,
                       index=frags.columns, columns=['mean', 'std'])
beta = beta.round(1)
beta['train_count'] = frags.sum(0)

ysi = ysi.set_index('SMILES')

def predict(smiles):

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
    mean, std = bridge.predict(reindexed_frags.values.reshape(1, -1),
                               return_std=True)

    # process fragments for display
    colors = husl_palette(n_colors=len(fragments))
    frag_df = pd.DataFrame(fragments, columns=['count'])
    frag_df['color'] = colors
    frag_df['svg'] = frag_df.apply(
        lambda x: Markup(draw_fragment(x.name, x.color)), 1)
    frag_df = frag_df.join(beta, how='left').fillna(0)

    return mean[0], std[0], isoutlier, frag_df, exp_mean, exp_std


def predict_apply(smiles):
    """ function optimized for pandas series of SMILES strings """

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
    mean, std = bridge.predict(reindexed_frags.values.reshape(1, -1),
                               return_std=True)

    prediction_type = 'prediction' if not isoutlier else 'outlier'
    if exp_mean:
        prediction_type = 'experiment'

    return pd.Series({
        'YSI': exp_mean if exp_mean else mean[0],
        'YSI_err': exp_std if exp_mean else std[0],
        'pred_type': prediction_type}, name=smiles)
