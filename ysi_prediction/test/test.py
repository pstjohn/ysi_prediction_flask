import pytest
from ysi_flask import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert b'Yield Sooting Index (YSI)' in rv.data

def test_result(client):
    rv = client.get('/result?name=c1ccccc1')
    assert b'Component Fragments' in rv.data

def test_neighbors(client):
    rv = client.get('frag?name=%5BH%5D-%5BC%5D%28-%5BH%5D%29%28-%5BH%5D%29-%5BC%5D')
    assert b'Containing Molecules' in rv.data

def test_out_of_scope(client):
    rv = client.get('/result?name=BrC1CCCC1')
    assert b'Missing Fragments' in rv.data

def test_invalid(client):
    rv = client.get('/result?name=')
    assert b'Please enter a valid SMILES without quotes' in rv.data


def test_api(client):
    data = client.get('/api/CCO').get_json()
    assert data['status'] == 'ok'

    data = client.get('/api?smiles=C%2FC%3DC%2FC').get_json()
    assert data['status'] == 'ok'

    data = client.get('/api/CB').get_json()
    assert data['outlier'] == True

    data = client.get('/api/X').get_json()
    assert data['status'] == 'invalid smiles'