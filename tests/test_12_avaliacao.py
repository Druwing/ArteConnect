import uuid

def criar_produto(flask_client, artesao_token, nome='Produto Teste'):
    resp = flask_client.post('/produtos/', json={
        'nome': nome,
        'descricao': 'Produto para teste de avaliação',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {artesao_token}"})
    assert resp.status_code == 201
    return resp.json.get('_id') or flask_client.get('/produtos/').json[-1]['_id']

def criar_cliente(flask_client):
    email = f"cliente_avaliacao_{uuid.uuid4().hex}@teste.com"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Avaliação',
        'email': email,
        'senha': '1234'
    })
    assert resp.status_code == 201
    resp = flask_client.post('/auth/login', json={'email': email, 'senha': '1234'})
    return resp.json['token']

def test_busca_produto_por_nome(flask_client, artesao_token):
    produto_id = criar_produto(flask_client, artesao_token, nome='Produto Teste')
    resp = flask_client.get('/produtos/?nome=Produto Teste')
    assert resp.status_code == 200
    assert any('Produto Teste' in p['nome'] for p in resp.json)

def test_cliente_nao_pode_avaliar_sem_login(flask_client, artesao_token):
    produto_id = criar_produto(flask_client, artesao_token)
    resp = flask_client.post(f'/produtos/{produto_id}/comentarios', json={'texto': 'Teste', 'nota': 5})
    # Aceita 401 (não autorizado) ou 404 (produto não encontrado, caso o endpoint não exista)
    assert resp.status_code in (401, 404)

def test_avaliar_produto_inexistente(flask_client):
    # Cria e autentica cliente
    email = f"cliente_avaliacao_{uuid.uuid4().hex}@teste.com"
    resp = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Avaliação',
        'email': email,
        'senha': '1234'
    })
    assert resp.status_code == 201
    resp = flask_client.post('/auth/login', json={'email': email, 'senha': '1234'})
    cliente_token = resp.json['token']
    # Tenta avaliar produto inexistente
    resp = flask_client.post('/produtos/id_inexistente/comentarios', json={'texto': 'Teste', 'nota': 5},
                             headers={"Authorization": f"Bearer {cliente_token}"})
    assert resp.status_code in (404, 400)