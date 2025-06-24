import pytest
import uuid

def test_cadastrar_artesao_route(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': "artesao@teste.com",
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
    })
    assert response.status_code == 201 or response.status_code == 409  # 409 if email already exists

def test_cadastrar_cliente_route(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': "cliente@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 201 or response.status_code == 409  # 409 if email already exists

def test_login_artesao_route(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': "artesao@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert data['tipo'] == 'artesao'
    assert data['id']

def test_login_cliente_route(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': "cliente@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert data['tipo'] == 'cliente'
    assert data['id']

def test_login_invalid_credentials(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': 'naoexiste@teste.com',
        'senha': 'senhaerrada'
    })
    assert response.status_code == 401
    assert 'token' not in response.json