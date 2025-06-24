import uuid

def test_checkout_concorrente_nao_excede_estoque(flask_client):
    # Cria e loga um artesão
    email_artesao = f"artesao_conc_{uuid.uuid4().hex}@teste.com"
    senha = "1234"
    resp = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Concorrência',
        'email': email_artesao,
        'senha': senha,
        'bio': 'Bio teste',
        'imagem_perfil': ''
    })
    assert resp.status_code == 201
    resp = flask_client.post('/auth/login', json={'email': email_artesao, 'senha': senha})
    token_artesao = resp.json['token']

    # Artesão cria um produto com estoque 1
    resp = flask_client.post('/produtos/', json={
        'nome': 'Produto Concorrente',
        'descricao': 'Teste de concorrência',
        'preco': 10.0,
        'quantidade': 1,
        'categoria': 'Teste'
    }, headers={"Authorization": f"Bearer {token_artesao}"})
    assert resp.status_code == 201

    # Busca o produto criado
    produtos = flask_client.get('/produtos/').json
    produto_id = [p['_id'] for p in produtos if p['nome'] == 'Produto Concorrente'][0]

    # Cria e loga dois clientes
    clientes = []
    for i in range(2):
        email_cliente = f"cliente_conc_{i}_{uuid.uuid4().hex}@teste.com"
        resp = flask_client.post('/auth/clientes', json={
            'nome': f'Cliente Concorrente {i}',
            'email': email_cliente,
            'senha': '1234'
        })
        assert resp.status_code == 201
        resp = flask_client.post('/auth/login', json={'email': email_cliente, 'senha': '1234'})
        clientes.append(resp.json['token'])

    # Ambos adicionam o produto ao carrinho
    for token in clientes:
        resp = flask_client.post('/carrinho/adicionar', json={
            "produtos": [{"produto_id": produto_id, "quantidade": 1}]
        }, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200

    # Ambos tentam fazer checkout (um deve conseguir, o outro deve falhar por estoque)
    resultados = []
    for token in clientes:
        resp = flask_client.post('/carrinho/checkout', headers={"Authorization": f"Bearer {token}"})
        resultados.append(resp)

    status_codes = [r.status_code for r in resultados]
    assert 200 in status_codes
    assert any(code in [400, 404] for code in status_codes)
    mensagens = [r.json['message'] for r in resultados]
    assert any('Checkout realizado com sucesso' in m for m in mensagens)
    assert any(
        'Estoque insuficiente' in m or 'não encontrado' in m.lower()
        for m in mensagens
    )