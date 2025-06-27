import uuid

def test_artesao_nao_pode_remover_produto_de_outro(flask_client):
    # Loga o artesão 1
    resp = flask_client.post('/auth/login', json={'email': "artesao@test.com", 'senha': '123'})
    token_a = resp.json['token']

    # Cria e loga o artesão 2
    resp = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão B',
        'email': "artesao_2@teste.com",
        'senha': '123',
        'bio': 'Bio B',
        'imagem_perfil': ''
    })
    assert resp.status_code == 201
    resp = flask_client.post('/auth/login', json={'email': 'artesao_2@teste.com', 'senha': '123'})
    token_b = resp.json['token']

    # Artesão A cria um produto
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Artesao A',
        'descricao': 'Produto de A',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {token_a}"})
    assert resp.status_code == 201

    # Busca o produto criado por A
    produtos = flask_client.get('/produtos/').json
    produto_id = [p['_id'] for p in produtos if p['nome'] == 'Produto Artesao A'][0]

    # Artesão B tenta remover o produto de A
    resp = flask_client.post('/produtos/remover', json={
        'produto_id': produto_id
    }, headers={"Authorization": f"Bearer {token_b}"})
    assert resp.status_code == 403
    assert 'permissão' in resp.json['message'].lower()

def test_artesao_listagem_nao_expoe_senha(flask_client, artesao_token):
    resp = flask_client.get('/artesaos/', headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 200
    for artesao in resp.json:
        assert 'senha' not in artesao