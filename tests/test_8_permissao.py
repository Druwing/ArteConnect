import uuid

def test_cliente_nao_pode_criar_produto(flask_client):
    # Cria e loga um cliente
    email = f"cliente_perm_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Permissão',
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 201

    resp = flask_client.post('/auth/login', json={
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 200
    token_cliente = resp.json['token']

    # Tenta criar produto como cliente
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Inválido',
        'descricao': 'Tentativa de cliente',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {token_cliente}"})
    assert resp.status_code == 403  # Acesso restrito a artesãos

def test_sem_token_nao_acessa_rotas_protegidas(flask_client):
    # Tenta acessar rota protegida sem token
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto',
        'descricao': 'Sem token',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    })
    assert resp.status_code == 401

def test_token_invalido(flask_client):
    # Tenta acessar rota protegida com token inválido
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto',
        'descricao': 'Token inválido',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": "Bearer token_invalido"})
    assert resp.status_code == 401

def test_cliente_nao_pode_remover_produto(flask_client):
    # Cria e loga um cliente
    email = f"cliente_remover_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Remover',
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 201

    resp = flask_client.post('/auth/login', json={
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 200
    token_cliente = resp.json['token']

    # Tenta remover produto como cliente
    resp = flask_client.post('/produtos/remover', json={
        'produto_id': 'id_invalido'
    }, headers={"Authorization": f"Bearer {token_cliente}"})
    assert resp.status_code == 403  # Acesso restrito a artesãos

def test_cliente_nao_pode_atualizar_quantidade_produto(flask_client):
    # Cria e loga um cliente
    email = f"cliente_atualiza_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Atualiza',
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 201

    resp = flask_client.post('/auth/login', json={
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 200
    token_cliente = resp.json['token']

    # Tenta atualizar quantidade como cliente
    resp = flask_client.post('/produtos/atualizar_quantidade', json={
        'produto_id': 'id_invalido',
        'quantidade': 2
    }, headers={"Authorization": f"Bearer {token_cliente}"})
    assert resp.status_code == 403  # Acesso restrito a artesãos