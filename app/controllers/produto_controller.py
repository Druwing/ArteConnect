from flask import jsonify, request
from bson import ObjectId
from app.models.database import get_db
from app.controllers.auth_controller import login_required, artesao_required
from datetime import datetime


@login_required
@artesao_required
def criar_produto():
    db = get_db()
    data = request.json
    artesao_id = request.usuario['id']
    
    if not data or 'nome' not in data or 'preco' not in data:
        return jsonify({'message': 'Dados incompletos'}), 400
    
    produto_data = {
        'nome': data['nome'],
        'descricao': data.get('descricao', ''),
        'preco': float(data['preco']),
        'disponibilidade': data.get('disponibilidade', True),
        'artesao_id': ObjectId(artesao_id),
        'imagem_url': data.get('imagem_url', ''),
        'data_criacao': datetime.datetime.utcnow()
    }
    
    result = db.produtos.insert_one(produto_data)
    return jsonify({
        'message': 'Produto criado com sucesso',
        'produto_id': str(result.inserted_id)
    }), 201

def listar_produtos():
    db = get_db()
    produtos = list(db.produtos.find({}))
    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        produto['artesao_id'] = str(produto['artesao_id'])
    return jsonify(produtos), 200