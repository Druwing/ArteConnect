# Teste do fluxo de integração
import uuid

def test_fluxo_completo_cliente(flask_client):
    # 0. Cadastro e login de artesão para criar produto
    email_artesao = f"artesao_{uuid.uuid4().hex}@teste.com"
    senha_artesao = "1234"
    resp = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Integração',
        'email': email_artesao,
        'senha': senha_artesao,
        'bio': 'Bio teste',
        'imagem_perfil': ''
    })
    assert resp.status_code == 201

    resp = flask_client.post('/auth/login', json={
        'email': email_artesao,
        'senha': senha_artesao
    })
    assert resp.status_code == 200
    token_artesao = resp.json['token']

    # 0.1 Cadastrar produto
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Integração',
        'descricao': 'Produto para teste de integração',
        'preco': 10.0,
        'quantidade': 5,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {token_artesao}"})
    assert resp.status_code == 201

    # 1. Cadastro de cliente
    email = f"cliente_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Integração',
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 201

    # 2. Login do cliente
    resp = flask_client.post('/auth/login', json={
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 200
    token = resp.json['token']

    # 3. Listar produtos
    resp = flask_client.get('/produtos/')
    assert resp.status_code == 200
    produtos = resp.json
    assert produtos, "Nenhum produto cadastrado para testar o fluxo"
    produto_id = produtos[0]['_id']

    # 4. Adicionar produto ao carrinho
    resp = flask_client.post('/carrinho/adicionar', json={
        "produtos": [{"produto_id": produto_id, "quantidade": 1}]
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    # 5. Checkout
    resp = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    # 6. Verificar carrinho limpo
    resp = flask_client.get('/carrinho/', headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json['produtos'] == []