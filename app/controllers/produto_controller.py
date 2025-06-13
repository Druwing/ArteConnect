from flask import jsonify, request
from bson import ObjectId
import datetime
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
        'quantidade': int(data['quantidade']),
        'artesao_id': ObjectId(artesao_id),
        'imagem_url': data.get('imagem_url', ''),
        'data_criacao': datetime.utcnow()
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

@login_required
@artesao_required
def remover_produto():
    db = get_db()
    data = request.json
    produto_id = data.get('produto_id')
    if not produto_id:
        return jsonify({'message': 'ID do produto não informado'}), 400

    produto = db.produtos.find_one({'_id': ObjectId(produto_id)})
    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    # Garante que o artesão só pode remover seus próprios produtos
    artesao_id = request.usuario['id']
    if str(produto['artesao_id']) != str(artesao_id):
        return jsonify({'message': 'Você não tem permissão para remover este produto'}), 403

    db.produtos.delete_one({'_id': ObjectId(produto_id)})
    return jsonify({'message': 'Produto removido com sucesso'}), 200

@login_required
@artesao_required
def remover_todos_produtos():
    db = get_db()
    artesao_id = request.usuario['id']
    result = db.produtos.delete_many({'artesao_id': ObjectId(artesao_id)})
    return jsonify({'message': f'{result.deleted_count} produtos removidos com sucesso'}), 200

@login_required
@artesao_required
def atualizar_quantidade_produto():
    db = get_db()
    data = request.json
    produto_id = data.get('produto_id')
    nova_quantidade = int(data.get('quantidade'))

    if nova_quantidade == 0:
        return remover_produto()
    
    if nova_quantidade < 0:
        return jsonify({'message': 'Não se pode deixar a contagem de produtos em negativa.'}), 403
    
    if not produto_id or nova_quantidade is None:
        return jsonify({'message': 'ID do produto e nova quantidade são obrigatórios'}), 400

    produto = db.produtos.find_one({'_id': ObjectId(produto_id)})
    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    # Garante que o artesão só pode atualizar seus próprios produtos
    artesao_id = request.usuario['id']
    if str(produto['artesao_id']) != str(artesao_id):
        return jsonify({'message': 'Você não tem permissão para atualizar este produto'}), 401

    db.produtos.update_one(
        {'_id': ObjectId(produto_id)},
        {'$set': {'quantidade': int(nova_quantidade)}}
    )
    return jsonify({'message': 'Quantidade do produto atualizada com sucesso'}), 200

