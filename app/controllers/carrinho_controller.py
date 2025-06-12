from flask import request, jsonify
from app.models.carrinho import Carrinho
from app.controllers.auth_controller import login_required

@login_required
def ver_carrinho():
    cliente_id = request.usuario['id']
    carrinho = Carrinho.obter_carrinho(cliente_id)
    # Convert ObjectId to string for JSON
    for item in carrinho.get('produtos', []):
        item['produto_id'] = str(item['produto_id'])
    carrinho['_id'] = str(carrinho['_id'])
    carrinho['cliente_id'] = str(carrinho['cliente_id'])
    return jsonify(carrinho), 200

@login_required
def adicionar_ao_carrinho():
    cliente_id = request.usuario['id']
    data = request.json
    produtos = data.get('produtos')
    if not produtos or not isinstance(produtos, list):
        return jsonify({'message': 'Lista de produtos não informada'}), 400
    Carrinho.adicionar_produtos(cliente_id, produtos)
    return jsonify({'message': 'Produtos adicionados ao carrinho'}), 200

@login_required
def remover_do_carrinho():
    cliente_id = request.usuario['id']
    data = request.json
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade', 1)
    if not produto_id:
        return jsonify({'message': 'Produto não informado'}), 400
    resultado = Carrinho.remover_produto(cliente_id, produto_id, quantidade)
    if 'error' in resultado:
        return jsonify({'message': resultado['error']}), 400
    return jsonify({'message': 'Produto removido do carrinho'}), 200

@login_required
def limpar_carrinho():
    cliente_id = request.usuario['id']
    Carrinho.limpar_carrinho(cliente_id)
    return jsonify({'message': 'Carrinho limpo'}), 200