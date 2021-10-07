import re
import ssl
from urllib.request import urlopen

from rdkit.Chem import MolToSmiles, MolFromSmiles
from rdkit.Chem.inchi import MolFromInchi, MolToInchi

try:
    import pubchempy as pcp
except ImportError:
    pcp = False

inchi_search = re.compile(
    '[^Get](InChI=[0-9BCOHNSOPrIFla+\-\(\)\\\/,pqbtmsih]{6,})', re.IGNORECASE)
smiles_search = re.compile(
    '<h3>Smiles</h3>\s*(\S*)<br>\s*<button type="button" id="downloadSmiles">')

CAS_search = re.compile(
    '(?<=[CAS\ Regeistry\ Number])(\d{1,7}\-\d{2}\-\d{1})')


def get_smiles_from_name(name):
    if not pcp:
        raise RuntimeError('No Pubchempy')

    compounds = pcp.get_compounds(name, 'name')
    if len(compounds) == 1:
        return canonicalize_smiles(compounds[0].isomeric_smiles)
    elif len(compounds) == 0:
        return
    elif len(compounds) > 1:
        print(', '.join((c.iupac_name for c in compounds)))


def get_smiles_from_cas(cas, db='nih'):
    """ Webquery to find SMILES from CAS number.

    db: 'nih' or 'nist'
        The database that is used for the search. If 'nist', smiles is created
        via an inchi string.

    """

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

    try:
        if db == 'nih':
            smiles = urlopen(
                'http://cactus.nci.nih.gov/chemical/structure/{}/SMILES'
                    .format(cas), context=context).read().decode()

        elif db == 'nist':
            html = urlopen(
                'http://webbook.nist.gov/cgi/cbook.cgi?ID={}&Units=SI'
                    .format(cas), context=context).read().decode()
            smiles = smiles_from_inchi(inchi_search.findall(html)[0])

        elif db == 'chemid':
            html = urlopen(
                'http://chem.sis.nlm.nih.gov/chemidplus/rn/{}'
                    .format(cas), context=context).read().decode()
            smiles = re.sub('<wbr>', '', smiles_search.findall(html)[0])

        return canonicalize_smiles(smiles)

    except Exception as ex:
        print("error with CAS: {0}, \t {1}".format(cas, ex))


def smiles_from_inchi(inchi):
    mol = MolFromInchi(inchi)
    return MolToSmiles(mol, isomericSmiles=True)


def inchi_from_smiles(smiles):
    mol = MolFromSmiles(smiles)
    return MolToInchi(mol)


def canonicalize_smiles(smiles, isomeric=True):
    try:
        mol = MolFromSmiles(smiles)
        return MolToSmiles(mol, isomericSmiles=isomeric)
    except Exception:
        pass


def check_cas(cas):
    try:
        cas_sum = sum(list((int(num) * (i + 1) for i, num in
                            enumerate(cas[:-2].replace('-', '')[::-1])))) % 10
        return cas_sum == int(cas[-1])
    except Exception:
        return False


cas_search = re.compile('([0-9]{2,7}-[0-9]{2}-[0-9])')


def get_cas_from_inchi(inchi):
    try:
        html = urlopen(
            'http://webbook.nist.gov/cgi/cbook.cgi?InChI={}&Units=SI'
                .format(inchi)).read().decode()
        cas = CAS_search.findall(html)[0]
        if check_cas(cas):
            return cas

    except Exception:
        pass


def get_iupac_name_from_smiles(smiles):
    if not pcp:
        raise RuntimeError('No Pubchempy')

    try:
        cpd = pcp.get_compounds(smiles, 'smiles')
    except pcp.PubChemHTTPError:
        cpd = pcp.get_compounds(smiles, 'smiles')

    if len(cpd) != 1:
        return
    else:
        return cpd[0].iupac_name


def get_cas_from_name(name, db='webbook'):
    try:
        if db == 'webbook':
            html = urlopen(
                'http://webbook.nist.gov/cgi/cbook.cgi?Name={}&Units=SI&cTP=on'
                    .format(name.lower().replace(',', '%2C'))).read().decode()
            CAS = CAS_search.findall(html)[0]
            if check_cas(CAS):
                return CAS

        elif db == 'pubchem':
            smiles = get_smiles_from_name(name)
            inchi = inchi_from_smiles(smiles)
            CAS = get_cas_from_inchi(inchi)
            if check_cas(CAS):
                return CAS

    except Exception:
        pass
