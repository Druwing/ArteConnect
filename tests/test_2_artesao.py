import pytest

artesao_base = None

def test_listar_artesaos_route(flask_client, artesao_token):
    response = flask_client.get('/artesaos/', headers={
        "Authorization": f"Bearer {artesao_token}"
    })
    assert response.status_code == 200
    assert isinstance(response.json, list)
    global artesao_base; artesao_base = response.json[0]

def test_obter_artesao_route(flask_client, artesao_token):
    id_artesao = artesao_base['_id']
    nome_artesao = artesao_base['nome']
    email_artesao = artesao_base['email']
    get_resp = flask_client.get(f'/artesaos/{id_artesao}', headers={
        "Authorization": f"Bearer {artesao_token}"
    })
    assert get_resp.status_code == 200
    data = get_resp.json
    assert data['nome'] == nome_artesao
    assert data['email'] == email_artesao
    assert 'imagem_perfil' in data
    
def test_artesao_listagem_nao_expoe_senha(flask_client, cliente_token):
    resp = flask_client.get('/artesaos/', headers={"Authorization": f"Bearer {cliente_token}"})
    assert resp.status_code == 200
    for artesao in resp.json:
        assert 'senha' not in artesao