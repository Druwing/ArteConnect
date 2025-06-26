from flask import jsonify, request
import jwt
from datetime import datetime,timedelta
from functools import wraps
from config import Config
from app.models.artesao import Artesao
from app.models.cliente import Cliente
import re

def gerar_token(usuario):
    payload = {
        'id': str(usuario['_id']),
        'email': usuario['email'],
        'tipo': usuario['tipo'],
        'exp': int((datetime.now() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)).timestamp())
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token de acesso ausente'}), 401
        
        try:
            token = token.split(' ')[1] 
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            request.usuario = data
        except:
            return jsonify({'message': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated

def artesao_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.usuario.get('tipo') != 'artesao':
            return jsonify({'message': 'Acesso restrito a artesãos'}), 403
        return f(*args, **kwargs)
    return decorated

def email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def cadastrar_artesao():
    data = request.json
    if not data or 'email' not in data or 'senha' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400

    if not email_valido(data['email']):
        return jsonify({'message': 'Email inválido'}), 400
    
    if data['senha'] == '':
        return jsonify({'message':'Senha Inválida'}), 400
    
    artesao_id = Artesao.criar_artesao(
        nome=data.get('nome'),
        email=data['email'],
        senha=data['senha'],
        bio=data.get('bio', ''),
        imagem_perfil=data.get('imagem_perfil', '')
    )
    
    if not artesao_id:
        return jsonify({'message': 'Email já cadastrado'}), 409
    
    return jsonify({'message': 'Artesão cadastrado com sucesso'}), 201

def cadastrar_cliente():
    data = request.json
    if not data or 'email' not in data or 'senha' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400

    if not email_valido(data['email']):
        return jsonify({'message': 'Email inválido'}), 400
    
    if data['senha'] == '':
        return jsonify({'message':'Senha Inválida'}), 400
    
    cliente_id = Cliente.criar_cliente(
        nome=data.get('nome'),
        email=data['email'],
        senha=data['senha']
    )
    
    if not cliente_id:
        return jsonify({'message': 'Email já cadastrado'}), 409
    
    return jsonify({'message': 'Cliente cadastrado com sucesso'}), 201

def login():
    data = request.json
    if not data or 'email' not in data or 'senha' not in data:
        return jsonify({'message': 'Credenciais ausentes'}), 400
    
    usuario = Artesao.verificar_credenciais(data['email'], data['senha'])
    if not usuario:
        usuario = Cliente.verificar_credenciais(data['email'], data['senha'])
    
    if not usuario:
        return jsonify({'message': 'Email ou senha incorretos'}), 401
    
    token = gerar_token(usuario)
    return jsonify({
        'token': token,
        'tipo': usuario['tipo'],
        'id': str(usuario['_id'])
    }), 200
