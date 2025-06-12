import pytest
from app import create_app
from config import Config
import json
import bcrypt

@pytest.fixture
def client():
    app = create_app(Config)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_cadastro_artesao(client):
    response = client.post('/auth/artesaos', json={
        'nome': 'Artesão Teste',
        'email': 'artesao@teste.com',
        'senha': 'senha123',
        'bio': 'Bio de teste'
    })
    assert response.status_code == 201

def test_cadastro_cliente(client):
    response = client.post('/auth/clientes', json={
        'nome': 'Cliente Teste',
        'email': 'cliente@teste.com',
        'senha': 'senha123'
    })
    assert response.status_code == 201

def test_login_artesao(client):
    # Primeiro cadastra
    client.post('/auth/artesaos', json={
        'nome': 'Artesão Login',
        'email': 'artesao_login@teste.com',
        'senha': 'senha123',
        'bio': 'Bio de teste'
    })
    
    # Depois tenta login
    response = client.post('/auth/login', json={
        'email': 'artesao_login@teste.com',
        'senha': 'senha123'
    })
    assert response.status_code == 200
    assert 'token' in response.json

def test_criar_produto_autenticado(client):
    # Cadastra e loga artesão
    client.post('/auth/artesaos', json={
        'nome': 'Artesão Produto',
        'email': 'artesao_produto@teste.com',
        'senha': 'senha123'
    })
    login = client.post('/auth/login', json={
        'email': 'artesao_produto@teste.com',
        'senha': 'senha123'
    })
    token = login.json['token']
    
    # Tenta criar produto com token
    response = client.post('/produtos', 
        json={
            'nome': 'Produto Teste',
            'preco': 100.50
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201

def test_criar_produto_nao_autenticado(client):
    response = client.post('/produtos', json={
        'nome': 'Produto Teste',
        'preco': 100.50
    })
    assert response.status_code == 401