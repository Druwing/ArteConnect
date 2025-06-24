import uuid


def test_remover_produto_success(flask_client):
    # Cria e loga um artesão
    email = f"artesao_remover_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Remover',
        'email': email,
        'senha': senha,
        'bio': 'Bio teste',
        'imagem_perfil': ''
    })
    assert resp.status_code == 201

    resp = flask_client.post('/auth/login', json={
        'email': email,
        'senha': senha
    })
    assert resp.status_code == 200
    token = resp.json['token']

    # Cria um produto
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Remover',
        'descricao': 'Produto para remover',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201

    # Busca o produto criado
    produtos = flask_client.get('/produtos/').json
    produto_id = [p['_id']
                  for p in produtos if p['nome'] == 'Produto Remover'][0]

    # Remove o produto
    response = flask_client.post('/produtos/remover', json={
        'produto_id': produto_id
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert 'Produto removido com sucesso' in response.json['message']


def test_remover_todos_produtos_success(flask_client, artesao_token):
    # First we add a new item to check if the items are correctly being deleted
    response = flask_client.post('/produtos/', json={
        'nome': 'Produto Teste',
        'descricao': 'Descrição do produto',
        'preco': 100.50,
        'quantidade': 5,
        'imagem_url': 'http://exemplo.com/imagem.png'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 201

    response = flask_client.post(
        '/produtos/remover_todos', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 200
    assert 'produtos removidos com sucesso' in response.json['message']
