import pytest
from app import create_app
from config import Config

@pytest.fixture(scope="module")
def flask_app():
    app = create_app(Config)
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope="module")
def flask_client(flask_app):
    return flask_app.test_client()

# ----------- FAIL CASES -----------

def test_ver_carrinho_route_fail(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.get('/carrinho/')
    assert response.status_code == 401

def test_adicionar_ao_carrinho_route_fail(flask_client):
    # Not authenticated, should fail (401)
    payload = {
        "produtos": [
            {"produto_id": "dummyid1", "quantidade": 2},
            {"produto_id": "dummyid2", "quantidade": 1}
        ]
    }
    response = flask_client.post('/carrinho/adicionar', json=payload)
    assert response.status_code == 401

def test_remover_do_carrinho_route_fail(flask_client):
    # Not authenticated, should fail (401)
    payload = {
        "produto_id": "dummyid1",
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload)
    assert response.status_code == 401

def test_limpar_carrinho_route_fail(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.post('/carrinho/limpar')
    assert response.status_code == 401

def test_checkout_route_fail(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.post('/carrinho/checkout')
    assert response.status_code == 401

# ----------- SUCCESS CASES (Authenticated) -----------
def test_ver_carrinho_route_success(flask_client, artesao_token):
    # You would need to login and set the auth header here
    response = flask_client.get('/carrinho/', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code in (200, 400)  # 400 if cart is empty

def test_adicionar_ao_carrinho_route_success(flask_client, artesao_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produtos": [
            {"produto_id": produto['_id'], "quantidade": produto['quantidade']} for produto in produtos_artesao
        ]
    }
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code in (200, 400)

def test_remover_do_carrinho_route_success(flask_client, artesao_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produto_id": produtos_artesao[0]['_id'],
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code in (200, 400)

def test_checkout_route_success(flask_client, artesao_token):
    response = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code in (200, 400)  # 400 if cart is empty

def test_limpar_carrinho_route_success(flask_client, artesao_token):
    # First, it adds items in carrinho
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produtos": [
            {"produto_id": produto['_id'], "quantidade": produto['quantidade']} for produto in produtos_artesao
        ]
    }
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {artesao_token}"})
    
    # Then, it removes all items from carrinho
    response = flask_client.post('/carrinho/limpar', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code in (200, 400)