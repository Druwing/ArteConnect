# ===========================================
# ========== TESTES DE AUTENTICAÇÃO =========
# ===========================================

import pytest
import uuid

# =====================================
# ======= TESTES BEM-SUCEDIDOS ========
# =====================================

# -------- /auth/artesaos --------

def test_cadastrar_artesao_route(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': "artesao@teste.com",
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
    })
    assert response.status_code == 201 or response.status_code == 409  # 409 if email already exists

# -------- /auth/clientes --------

def test_cadastrar_cliente_route(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': "cliente@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 201 or response.status_code == 409  # 409 if email already exists

def test_cadastrar_cliente_duplicate_route(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': "cliente@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 201 or response.status_code == 409

# -------- /auth/login --------

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

# =====================================
# =========== TESTES FALHOS ===========
# =====================================

# -------- /auth/artesaos --------

def test_cadastrar_artesao_missing_email(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_artesao_invalid_email(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Teste',
        'email': "artesao_fail_teste.com",
        'senha': '1234'
    })
    assert response.status_code == 400 
    
def test_cadastrar_artesao_duplicate_email(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Outro Artesão',
        'email': 'artesao@teste.com',
        'senha': 'outra_senha',
        'bio': 'Outra bio',
        'imagem_perfil': 'data:image/png;base64,BBBB'
    })
    assert response.status_code == 409
    assert 'Email já cadastrado' in response.json['message']

def test_cadastrar_artesao_missing_password(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': "artesao_fail@teste.com",
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']

def test_cadastrar_artesao_empty_password(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': "artesao_fail@teste.com",
        'senha': '',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400

def test_cadastrar_artesao_missing_nome(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'email': "artesao_fail@teste.com",
        'senha': '1234',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'O nome não pode estar vazio' in response.json['message']
    
def test_cadastrar_artesao_empty_nome(flask_client):
    response = flask_client.post('/auth/artesaos', json={
        'email': "artesao_fail@teste.com",
        'senha': '1234',
        'nome': '',
        'bio': 'Bio de teste',
        'imagem_perfil': 'data:image/png;base64,AAAA'
    })
    assert response.status_code == 400
    assert 'O nome não pode estar vazio' in response.json['message']

def test_cadastrar_artesao_no_json(flask_client):
    response = flask_client.post('/auth/artesaos')
    assert response.status_code == 400

# -------- /auth/clientes --------

def test_cadastrar_cliente_missing_email(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'senha': '1234'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']
    
def test_cadastrar_cliente_invalid_email(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'clientes_fail_teste.com',
        'senha': '1234'
    })
    assert response.status_code == 400
    
def test_cadastrar_cliente_duplicate_email(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Outro Cliente',
        'email': 'cliente@teste.com',
        'senha': 'outra'
    })
    assert response.status_code == 409
    assert 'Email já cadastrado' in response.json['message']

def test_cadastrar_cliente_missing_password(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'cliente_fail@teste.com'
    })
    assert response.status_code == 400
    assert 'Dados incompletos' in response.json['message']
    
def test_cadastrar_cliente_empty_password(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'cliente_fail@teste.com',
        'senha': ''
    })
    assert response.status_code == 400
    
def test_cadastrar_cliente_missing_nome(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'email': 'cliente_fail@teste.com',
        'senha': '123'
    })
    assert response.status_code == 400
    assert 'O nome não pode estar vazio' in response.json['message']
    
def test_cadastrar_cliente_empty_nome(flask_client):
    response = flask_client.post('/auth/clientes', json={
        'email': 'cliente_fail@teste.com',
        'senha': '123',
        'nome': ''
    })
    assert response.status_code == 400
    assert 'O nome não pode estar vazio' in response.json['message']

def test_cadastrar_cliente_no_json(flask_client):
    response = flask_client.post('/auth/clientes')
    assert response.status_code == 400

# -------- /auth/login --------

def test_login_invalid_credentials(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': 'login_fail@teste.com',
        'senha': 'senhaerrada'
    })
    assert response.status_code == 401
    assert 'token' not in response.json
    
def test_login_no_email(flask_client):
    response = flask_client.post('/auth/login',json={
        'senha':'senhaerrada'
    })
    assert response.status_code == 400
    
def test_login_empty_email(flask_client):
    response = flask_client.post('/auth/login',json={
        'email': '',
        'senha':'senhaerrada'
    })
    assert response.status_code == 400
    
def test_login_no_password(flask_client):
    response = flask_client.post('/auth/login',json={
        'email': 'client@test.com'
    })
    assert response.status_code == 400
    
def test_login_empty_password(flask_client):
    response = flask_client.post('/auth/login',json={
        'email': 'client@test.com',
        'senha':''
    })
    assert response.status_code == 400