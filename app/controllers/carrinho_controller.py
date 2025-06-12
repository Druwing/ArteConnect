from flask import request, jsonify
from app.models.carrinho import Carrinho
from app.models.produto import Produto
from app.controllers.auth_controller import login_required
from app.controllers.produto_controller import atualizar_quantidade_produto
from app.models.database import get_db
from bson import ObjectId

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

@login_required
def checkout():
    cliente_id = request.usuario['id']
    carrinho = Carrinho.obter_carrinho(cliente_id)
    produtos_no_carrinho = carrinho.get('produtos', [])

    if not produtos_no_carrinho:
        return jsonify({'message': 'Carrinho vazio'}), 400

    db = get_db()

    # 1. Verifica disponibilidade de todos os produtos
    produtos_para_atualizar = []
    for item in produtos_no_carrinho:
        produto = Produto.obter_produto(item['produto_id'])
        if not produto:
            return jsonify({'message': f"Produto {item['produto_id']} não encontrado"}), 404
        estoque = produto.get('quantidade', 0)
        if estoque < item['quantidade']:
            return jsonify({'message': f"Estoque insuficiente para o produto {produto.get('nome', str(item['produto_id']))}"}), 400
        produtos_para_atualizar.append({
            'produto_id': str(produto['_id']),
            'nova_quantidade': estoque - item['quantidade'],
            'artesao_id': str(produto['artesao_id'])
        })

    # 2. Atualiza o estoque de todos os produtos usando atualizar_quantidade_produto
    for produto_info in produtos_para_atualizar:
        # Monta um request-like objeto para atualizar_quantidade_produto
        with request.app.test_request_context(
            json={
                'produto_id': produto_info['produto_id'],
                'quantidade': produto_info['nova_quantidade']
            }
        ):
            # Força o usuário autenticado como o artesão do produto
            request.usuario = {'id': produto_info['artesao_id']}
            resp = atualizar_quantidade_produto()
            if resp[1] != 200:
                return resp

    # 3. Limpa o carrinho
    Carrinho.limpar_carrinho(cliente_id)

    return jsonify({'message': 'Checkout realizado com sucesso!'}), 200