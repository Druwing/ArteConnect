import pytest
from app import create_app
from config import Config

@pytest.fixture(scope="module")
def flask_app():
    app = create_app(Config)
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope="module")
def flask_client(flask_app):
    return flask_app.test_client()


@pytest.fixture(scope="module")
def artesao_token(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': "artesao@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 200
    return response.json['token']

@pytest.fixture(scope="module")
def cliente_token(flask_client):
    response = flask_client.post('/auth/login', json={
        'email': "cliente@teste.com",
        'senha': '1234'
    })
    assert response.status_code == 200
    return response.json['token']