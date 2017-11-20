import os
import pandas as pd
import seaborn as sns
from flask import Markup

from .fragment_decomposition import get_fragments, draw_fragment

currdir = os.path.dirname(os.path.abspath(__file__))

beta_df = pd.read_csv(currdir + '/data/fragment_values.csv')
nullspace = pd.read_csv(currdir + '/data/nullspace.csv')
frag_counts = pd.read_csv(currdir + '/data/ysi_fragments.csv')

def predict(smiles):
    fragments = get_fragments(smiles)
    isoutlier = False

    # Make sure all the fragments are found in the database
    if not fragments.index.isin(beta_df.columns).all():
        isoutlier = True

    # Put the fragments in the correct order
    reindexed_frags = fragments.reindex(beta_df.columns).fillna(0).astype(int)
    reindexed_frags['intercept'] = 1
    
    # Make sure the fragments are not present in nonlinear combinations of database
    if (nullspace @ reindexed_frags.iloc[1:].values).sum() > 1E-10:
        isoutlier = True

    # Predict based off previous regression
    means = beta_df.dot(reindexed_frags)
    mean = means.mean()
    std = means.std()

    # process fragments for display
    colors = sns.color_palette(n_colors=len(fragments), palette='husl')
    frag_df = pd.DataFrame(fragments, columns=['count'])
    frag_df['color'] = colors
    frag_df['svg'] = frag_df.apply(
        lambda x: Markup(draw_fragment(x.name, x.color)), 1)

    beta_reindexed = beta_df.T.reindex(frag_df.index)
    frag_df['mean'] = beta_reindexed.mean(1).round(1)
    frag_df['std'] = beta_reindexed.std(1).round(1)
    frag_df['train_count'] = \
        frag_counts.astype(bool).sum(0).reindex(frag_df.index).fillna(0).astype(int)

    return mean, std, isoutlier, frag_df
