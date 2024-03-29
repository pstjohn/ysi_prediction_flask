import re
from collections import Counter

import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from ysi_flask.fragdecomp.chemical_conversions import canonicalize_smiles

# from IPython.display import SVG


class FragmentError(Exception):
    pass


def get_fragments(smiles):
    """Return a pandas series indicating the carbon types in the given SMILES
    string

    smiles: string
        A representation of the desired molecule. I.e, 'CCCC'

    """
    try:
        mol = Chem.MolFromSmiles(canonicalize_smiles(smiles, isomeric=False))
        mol = Chem.AddHs(mol)  # This seems important to get just the next C
        return pd.Series(
            Counter(
                (get_environment_smarts(carbon, mol) for carbon in iter_carbons(mol))
            )
        )

    except Exception:
        # Deal with wierd rdkit errors
        raise FragmentError


def iter_carbons(mol):
    """Iterates over the carbon atoms in the given molecule

    mol: an rdkit.Chem.Mol object

    """
    for a in mol.GetAtoms():
        if a.GetSymbol() == "C":
            yield a

        # elif a.GetSymbol() is 'O':
        #     neighbors = [ai for ai in a.GetNeighbors()
        #                  if ai.GetSymbol() is not 'H']
        #     if len(neighbors) > 1:
        #         yield a


def get_environment_smarts(carbon, mol):
    """For a given carbon atom and molecule, return a SMARTS representation of
    the atom environment.

    carbon: rdkit.Chem.Atom
        The desired carbon atom
    mol: rdkit.Chem.Mol
        The molecule the atom is present in

    """
    bond_list = list(
        Chem.FindAtomEnvironmentOfRadiusN(mol, 1, carbon.GetIdx(), useHs=True)
    )

    bond_smarts = bond_list_to_smarts(mol, bond_list)

    if carbon.IsInRing():
        return bond_smarts + " | (Ring)"
    else:
        return bond_smarts


def bond_list_to_smarts(mol, bond_list):
    """For a given molecule and list of bond indices, return a SMARTS string.

    mol: rdkit.Chem.Mol
        The molecule the atom is present in
    bond_list: list
        A list of bond indicies

    """
    atoms = set()
    for bidx in bond_list:
        atoms.add(mol.GetBondWithIdx(bidx).GetBeginAtomIdx())
        atoms.add(mol.GetBondWithIdx(bidx).GetEndAtomIdx())
    return Chem.MolFragmentToSmiles(
        mol, atoms, canonical=True, allBondsExplicit=True, allHsExplicit=True
    )


def label_fragments(smiles):
    """For a given smiles string, return the carbon fragments and atom indices
    corresponding to those fragments

    smiles: string

    """
    mol = Chem.MolFromSmiles(canonicalize_smiles(smiles, isomeric=False))
    mol = Chem.AddHs(mol)
    out = {}
    for carbon in iter_carbons(mol):
        out[carbon.GetIdx()] = get_environment_smarts(carbon, mol)

    return pd.Series(out)


def draw_mol_svg(mol_str, color_dict=None, figsize=(300, 300), smiles=True):
    """Return an SVG image of the molecule, with atoms highlighted to reveal
    the sootiest fragments.

    (Note: This is currently not very quantitative...)

    mol_str: string
    fragment_soot: dict-like
        A dictionary matching fragment SMILES to color
    figsize: tuple
        Figure size (in pixels) to pass to rdkit.

    """
    if smiles:
        mol = Chem.MolFromSmiles(mol_str)
    else:
        mol = Chem.MolFromSmarts(mol_str)

    mc = Chem.Mol(mol.ToBinary())
    if True:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())

    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)

    drawer = rdMolDraw2D.MolDraw2DSVG(*figsize)

    if color_dict is not None:
        matches = label_fragments(mol_str)

        highlight_colors_dict = pd.DataFrame(matches).merge(
            pd.DataFrame(pd.Series(color_dict)), left_on=0, right_index=True
        )["0_y"]

        drawer.DrawMolecule(
            mc,
            highlightAtoms=tuple(highlight_colors_dict.index),
            highlightAtomColors=highlight_colors_dict.to_dict(),
            highlightBonds=False,
        )

    else:
        drawer.DrawMolecule(mc)

    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()

    svg = svg.replace("svg:", "").replace(":svg", "")
    return svg


def flatten(l, ltypes=(list, tuple)):
    """Utility function to iterate over a flattened list"""
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i : i + 1] = l[i]
        i += 1
    return ltype(l)


def draw_fragment(fragment_name, color):
    mol = Chem.MolFromSmarts(re.sub(" \|.*$", "", fragment_name))
    mc = Chem.Mol(mol.ToBinary())
    rdDepictor.Compute2DCoords(mc)

    drawer = rdMolDraw2D.MolDraw2DSVG(80, 80)

    center = int(
        pd.Series(
            {atom.GetIdx(): len(atom.GetNeighbors()) for atom in mol.GetAtoms()}
        ).idxmax()
    )

    to_highlight = [center]
    radius_dict = {center: 0.5}
    color_dict = {center: color}

    drawer.DrawMolecule(
        mc,
        highlightAtoms=to_highlight,
        highlightAtomColors=color_dict,
        highlightAtomRadii=radius_dict,
        highlightBonds=False,
    )

    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()

    return svg.replace("svg:", "").replace(":svg", "")
