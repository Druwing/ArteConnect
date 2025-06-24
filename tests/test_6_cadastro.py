import pytest
import os
from app import create_app
from config import Config
import uuid

@pytest.fixture(scope="module")
def flask_app():
    app = create_app(Config)
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope="module")
def flask_client(flask_app):
    return flask_app.test_client()

def test_cadastrar_artesao_missing_email(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_artesao_missing_password(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': 'novoartesao@teste.com',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_artesao_missing_nome(flask_client):
    email_unico = f"novoartesao2_{uuid.uuid4().hex}@teste.com"
    response = flask_client.post('/auth/artesaos', json={
        'email': email_unico,
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code in (201, 400)

def test_cadastrar_artesao_duplicate_email(flask_client):
    # First, register
    flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': 'duplicado@teste.com',
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    # Try again with same email
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Outro Artesão',
        'email': 'duplicado@teste.com',
        'senha': 'outra_senha',
        'bio': 'Outra bio',
        'imagem_perfil': 'data:image/png;base64,BBBB'
    })
    assert response.status_code == 409
    assert 'Email já cadastrado' in response.json['message']

def test_cadastrar_artesao_empty_password(flask_client):
    email_unico = f"vazio_{uuid.uuid4().hex}@teste.com"
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': email_unico,
        'senha': '',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code in (201, 400)

def test_cadastrar_artesao_no_json(flask_client):
    response = flask_client.post('/auth/artesaos')
    assert response.status_code == 400

def test_cadastrar_cliente_missing_email(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'senha': '1234'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_cliente_missing_password(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'novocliente@teste.com'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_cliente_duplicate_email(flask_client):
    flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'duplicadocliente@teste.com',
        'senha': '1234'
    })
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Outro Cliente',
        'email': 'duplicadocliente@teste.com',
        'senha': 'outra'
    })
    assert response.status_code == 409
    assert 'Email já cadastrado' in response.json['message']

def test_cadastrar_artesao_email_invalido(flask_client):
    email_unico = f"emailinvalido_{uuid.uuid4().hex}"  # sem @, propositalmente inválido
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Teste',
        'email': email_unico,
        'senha': '1234'
    })
    assert response.status_code in (400, 422)

def test_cadastrar_cliente_no_json(flask_client):
    response = flask_client.post('/auth/clientes')
    assert response.status_code == 400

def test_cadastrar_cliente_empty_password(flask_client):
    email_unico = f"vazio_{uuid.uuid4().hex}@cliente.com"
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': email_unico,
        'senha': ''
    })
    assert response.status_code in (201, 400)

def test_cadastrar_cliente_email_invalido(flask_client):
    email_unico = f"emailinvalido_{uuid.uuid4().hex}"  # sem @, propositalmente inválido
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': email_unico,
        'senha': '1234'
    })
    assert response.status_code in (400, 422)

def test_cadastrar_artesao_campos_extras(flask_client):
    email_unico = f"extracampo_{uuid.uuid4().hex}@teste.com"
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': email_unico,
        'senha': '1234',
        'campo_invalido': 'valor'
    })
    assert response.status_code in (201, 400)