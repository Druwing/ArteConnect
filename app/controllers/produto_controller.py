from flask import jsonify, request
from bson import ObjectId
from app.models.produto import Produto

def cadastrar_produto():
    data = request.json
    
    produto_id = Produto.criar_produto(
        nome=data['nome'],
        descricao=data['descricao'],
        preco=data['preco'],
        disponibilidade=data['disponibilidade'],
        artesao_id=data['artesao_id'],
        imagem_url=data['imagem_url']
    )
    
    return jsonify({
        'mensagem': 'Produto cadastrado com sucesso',
        'produto_id': str(produto_id)
    }), 201

def listar_produtos():
    filtros = {
        'categoria': request.args.get('categoria'),
        'preco_min': request.args.get('preco_min'),
        'preco_max': request.args.get('preco_max')
    }
    
    produtos = Produto.listar_produtos(filtros)
    for produto in produtos:
        produto['_id'] = str(produto['_id'])
        produto['artesao_id'] = str(produto['artesao_id'])
    
    return jsonify(produtos), 200

def adicionar_comentario(produto_id):
    data = request.json
    
    Produto.adicionar_comentario(
        produto_id=produto_id,
        cliente_id=data['cliente_id'],
        nota=data['nota'],
        texto=data['texto']
    )
    
    return jsonify({'mensagem': 'Comentário adicionado com sucesso'}), 201

def obter_comentarios(produto_id):
    comentarios = Produto.obter_comentarios(produto_id)
    for comentario in comentarios:
        comentario['cliente_id'] = str(comentario['cliente_id'])
        comentario['data'] = comentario['data'].isoformat()
    
    return jsonify(comentarios), 200