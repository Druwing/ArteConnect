import pytest

# =====================================
# ======= TESTES BEM-SUCEDIDOS ========
# =====================================

def test_ver_carrinho_success(flask_client, cliente_token):
    response = flask_client.get('/carrinho/', headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200

def test_adicionar_ao_carrinho_success(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produtos": [
            {"produto_id": produto['_id'], "quantidade": 5} for produto in produtos_artesao
        ]
    }
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200

def test_reduzir_do_carrinho_success(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produto_id": produtos_artesao[0]['_id'],
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200
    
def test_remover_do_carrinho_success(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produto_id": produtos_artesao[0]['_id'],
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200

def test_limpar_carrinho_success(flask_client, cliente_token):    
    # Then, it removes all items from carrinho
    response = flask_client.post('/carrinho/limpar', headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200
    
    # Adds productos back in carrinho so other tests can be performed
    test_adicionar_ao_carrinho_success(flask_client,cliente_token)
    
def test_checkout_success(flask_client, cliente_token):
    # Ensure carrinho contains no incorrect items 
    flask_client.post('/carrinho/limpar', headers={"Authorization": f"Bearer {cliente_token}"})
    
    # Ensures carrinho contains correct items
    produtos_artesao = flask_client.get('/produtos/').json
    produto = produtos_artesao[0]
    payload = {
        "produtos": [
            {'produto_id': produto['_id'], 'quantidade':1}
        ]
    }
    flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    
    # Checkout carrinho
    response = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 200
    
    # Adds productos back in carrinho so other tests can be performed
    test_adicionar_ao_carrinho_success(flask_client,cliente_token)
# =====================================
# =========== TESTES FALHOS ===========
# =====================================

# -------- ver_carrinho --------

def test_ver_carrinho_no_auth(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.get('/carrinho/')
    assert response.status_code == 401


# -------- adicionar_ao_carrinho --------

def test_adicionar_ao_carrinho_no_auth(flask_client):
    # Not authenticated, should fail (401)
    payload = {
        "produtos": [
            {"produto_id": "dummyid1", "quantidade": 2},
            {"produto_id": "dummyid2", "quantidade": 1}
        ]
    }
    response = flask_client.post('/carrinho/adicionar', json=payload)
    assert response.status_code == 401
    
def test_adicionar_ao_carrinho_no_produto(flask_client, cliente_token):
    payload = {}
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    
def test_adicionar_ao_carrinho_empty_produto(flask_client, cliente_token):
    payload = {
        "produtos": []
    }
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    
def test_adicionar_ao_carrinho_produto_not_list(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produtos": {"produto_id": produto['_id'], "quantidade": produto['quantidade']} for produto in produtos_artesao
    }
    response = flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400

# -------- remover do carrinho --------

def test_remover_do_carrinho_no_auth(flask_client):
    # Not authenticated, should fail (401)
    payload = {
        "produto_id": "dummyid1",
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload)
    assert response.status_code == 401

def test_remover_do_carrinho_no_produto(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    assert 'Produto não informado' in response.json['message']
    
def test_remover_do_carrinho_invalid_produto(flask_client, cliente_token):
    payload = {
        "produto_id": 'Fake id',
        "quantidade": 1
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    assert 'Produto não encontrado no carrinho' in response.json['message']
    
def test_remover_do_carrinho_high_quantidade(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produto_id": produtos_artesao[0]['_id'],
        "quantidade": 1_000
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    assert 'Tentando remover quantidade maior do que a disponível no carrinho' in response.json['message']
    
def test_remover_do_carrinho_negative_quantidade(flask_client, cliente_token):
    produtos_artesao = flask_client.get('/produtos/').json
    payload = {
        "produto_id": produtos_artesao[0]['_id'],
        "quantidade": -1
    }
    response = flask_client.post('/carrinho/remover', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    assert 'Essa quantidade não é válida' in response.json['message']
    
# -------- limpar_carrinho --------
def test_limpar_carrinho_no_auth(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.post('/carrinho/limpar')
    assert response.status_code == 401

# -------- checkout --------
def test_checkout_no_auth(flask_client):
    # Not authenticated, should fail (401)
    response = flask_client.post('/carrinho/checkout')
    assert response.status_code == 401
    
def test_checkout_empty_carrinho(flask_client, cliente_token):
    # First, ensure carrinho is empty
    flask_client.post('/carrinho/limpar', headers={"Authorization": f"Bearer {cliente_token}"})
    
    # Checkout for empty carrinho
    response = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 400
    
def test_checkout_bad_carrinho(flask_client, cliente_token):  
    # Empties carrinho just for better control of products inside it
    flask_client.post('/carrinho/limpar', headers={"Authorization": f"Bearer {cliente_token}"})
    fake_id = '685e9e05184a02829e7b1e31'
    # Adds incorrect product in carrinho
    payload = {
        "produtos": [
            {"produto_id": fake_id, "quantidade": 1}
        ]
    }
    flask_client.post('/carrinho/adicionar', json=payload, headers={"Authorization": f"Bearer {cliente_token}"})
    
    # Checkout carrinho with bad product
    response = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 404
    assert f'Produto {fake_id} não encontrado' in response.json['message']
    
    # Clears carrinho and adds produtos back in carrinho so other tests can be performed
    test_limpar_carrinho_success(flask_client,cliente_token)
    test_adicionar_ao_carrinho_success(flask_client,cliente_token)