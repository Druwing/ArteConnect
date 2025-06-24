# import pytest 

def test_remover_produto_success(flask_client, artesao_token):
    produtos_artesao = flask_client.get('/produtos/').json
    
    response = flask_client.post('/produtos/remover', json={
        'produto_id': produtos_artesao[0]['_id']
    }, headers={"Authorization": f"Bearer {artesao_token}"})
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
    
    response = flask_client.post('/produtos/remover_todos', headers={"Authorization": f"Bearer {artesao_token}"})
    assert response.status_code == 200
    assert 'produtos removidos com sucesso' in response.json['message']