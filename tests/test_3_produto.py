import pytest

# =====================================
# ======= TESTES BEM-SUCEDIDOS ========
# =====================================

def test_criar_produto_success(flask_client, artesao_token):
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 201
    data = response.json
    assert 'produto_id' in data
    global produto_id
    produto_id = data['produto_id']
    
def test_criar_produto_nome_caracteres_especiais(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': '@#$%&*!',
        'descricao': 'Nome com caracteres especiais',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201
    
def test_criar_produto_quantidade_zero(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Zero',
        'descricao': 'Quantidade zero',
        'preco': 10.0,
        'quantidade': 0,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_listar_produtos(flask_client, artesao_token):
    response = flask_client.get('/produtos/', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_atualizar_quantidade_produto_success(flask_client, artesao_token):
    global produto_id
    response = flask_client.post('/produtos/atualizar_quantidade', json={
        'produto_id': produto_id,
        'quantidade': 50
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 200
    assert 'Quantidade do produto atualizada com sucesso' in response.json['message']
    
# =====================================
# =========== TESTES FALHOS ===========
# =====================================

# -------- no auth --------

def test_criar_produto_fail_no_auth(flask_client):
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5
    })
    assert response.status_code == 401

def test_atualizar_quantidade_produto_fail_no_auth(flask_client):
    global produto_id
    response = flask_client.post('/produtos/atualizar_quantidade', json={
        'produto_id': produto_id,
        'quantidade': 2
    })
    assert response.status_code == 401

def test_remover_produto_fail_no_auth(flask_client):
    global produto_id
    response = flask_client.post('/produtos/remover', json={
        'produto_id': produto_id
    })
    assert response.status_code == 401

def test_remover_todos_produtos_fail_no_auth(flask_client):
    response = flask_client.post('/produtos/remover_todos')
    assert response.status_code == 401
    
# -------- client auth --------
def test_criar_produto_fail_client_auth(flask_client, cliente_token):
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5
    }, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 403

def test_atualizar_quantidade_produto_fail_client_auth(flask_client, cliente_token):
    global produto_id
    response = flask_client.post('/produtos/atualizar_quantidade', json={
        'produto_id': produto_id,
        'quantidade': 2
    }, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 403

def test_remover_produto_fail_client_auth(flask_client, cliente_token):
    global produto_id
    response = flask_client.post('/produtos/remover', json={
        'produto_id': produto_id
    }, headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 403

def test_remover_todos_produtos_fail_client_auth(flask_client, cliente_token):
    response = flask_client.post('/produtos/remover_todos',
                                 headers={"Authorization": f"Bearer {cliente_token}"})
    assert response.status_code == 403
    
# -------- Different artesao --------
def test_artesao_nao_pode_remover_produto_de_outro(flask_client, artesao_token):
    # Cria e loga o artesão 2
    resp = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão B',
        'email': "artesao_2@teste.com",
        'senha': '123',
        'bio': 'Bio B',
        'imagem_perfil': ''
    })
    assert resp.status_code in (201,409)
    resp = flask_client.post('/auth/login', json={'email': 'artesao_2@teste.com', 'senha': '123'})
    token_b = resp.json['token']

    # Busca o produto criado por A
    produtos = flask_client.get('/produtos/',headers={"Authorization": f"Bearer {artesao_token}"}).json
    produto_id = produtos[0]['_id']

    # Artesão B tenta remover o produto de A
    resp = flask_client.post('/produtos/remover', json={
        'produto_id': produto_id,
        'quantidade': 1
    }, headers={"Authorization": f"Bearer {token_b}"})
    assert resp.status_code == 403
    assert 'permissão' in resp.json['message'].lower()


# -------- Bad formatting/data --------

# Nome
def test_criar_produto_no_nome(flask_client, artesao_token):
    response = flask_client.post('/produtos/', json={
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']
    
def test_criar_produto_empty_nome(flask_client, artesao_token):
    response = flask_client.post('/produtos/', json={
        'nome': '',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']
   
# Preco 
def test_criar_produto_no_preco(flask_client, artesao_token):
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto gratis',
        'descricao': 'Descrição do produto',
        'quantidade': 5,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']
    
# Quantidade
def test_criar_produto_no_quantidade(flask_client, artesao_token):
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto gratis',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']