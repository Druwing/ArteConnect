import uuid

def test_criar_produto_nome_muito_longo(flask_client, artesao_token):
    nome_longo = "A" * 300  # 300 caracteres
    resp = flask_client.post('/produtos/', json={
        'nome': nome_longo,
        'descricao': 'Teste nome longo',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    # Espera-se 400 ou 422 se houver validação, ou 201 se não houver limite
    assert resp.status_code in (201, 400, 422)

def test_criar_produto_sem_descricao(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Sem Descrição',
        'preco': 10.0,
        'quantidade': 1,
        # 'descricao' omitido
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_sem_categoria(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Sem Categoria',
        'preco': 10.0,
        'quantidade': 1,
        'descricao': 'Sem categoria'
        # 'categoria' omitido
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_nome_minimo(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'A',
        'descricao': 'Nome mínimo',
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
    assert resp.status_code in (201, 400, 422)

def test_criar_produto_descricao_vazia(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Descrição Vazia',
        'descricao': '',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_categoria_vazia(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Categoria Vazia',
        'descricao': 'Categoria vazia',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': ''
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_nome_espacos(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': '   ',
        'descricao': 'Nome só espaços',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_nome_caracteres_especiais(flask_client, artesao_token):
    resp = flask_client.post('/produtos/', json={
        'nome': '@#$%&*!',
        'descricao': 'Nome com caracteres especiais',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201

def test_criar_produto_descricao_muito_longa(flask_client, artesao_token):
    descricao_longa = "B" * 1000  # 1000 caracteres
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Descrição Longa',
        'descricao': descricao_longa,
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code in (201, 400, 422)