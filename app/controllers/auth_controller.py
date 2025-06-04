from flask import jsonify, request
from bson import ObjectId
from app.models.database import get_db

def cadastrar_cliente():
    data = request.json
    db = get_db()
    
    cliente_id = db.clientes.insert_one({
        'email': data['email'],
        'nome': data['nome']
    }).inserted_id
    
    return jsonify({
        'mensagem': 'Cliente cadastrado com sucesso',
        'cliente_id': str(cliente_id)
    }), 201

def obter_cliente(cliente_id):
    db = get_db()
    cliente = db.clientes.find_one({'_id': ObjectId(cliente_id)})
    
    if not cliente:
        return jsonify({'mensagem': 'Cliente não encontrado'}), 404
    
    cliente['_id'] = str(cliente['_id'])
    return jsonify(cliente), 200