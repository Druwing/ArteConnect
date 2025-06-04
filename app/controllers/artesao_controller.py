from flask import jsonify, request
from bson import ObjectId
from bson.binary import Binary
from app.models.artesao import Artesao
import base64

def cadastrar_artesao():
    data = request.json
    imagem_binaria = Binary(base64.b64decode(data['imagem_perfil'].split(',')[1]))
    
    artesao_id = Artesao.criar_artesao(
        nome=data['nome'],
        bio=data['bio'],
        imagem_perfil=imagem_binaria
    )
    
    return jsonify({
        'mensagem': 'Artesão cadastrado com sucesso',
        'artesao_id': str(artesao_id)
    }), 201

def obter_artesao(artesao_id):
    artesao = Artesao.obter_artesao(artesao_id)
    if not artesao:
        return jsonify({'mensagem': 'Artesão não encontrado'}), 404
    
    artesao['_id'] = str(artesao['_id'])
    if 'imagem_perfil' in artesao:
        artesao['imagem_perfil'] = base64.b64encode(artesao['imagem_perfil']).decode('utf-8')
    
    return jsonify(artesao), 200

def listar_artesaos():
    artesaos = Artesao.listar_artesaos()
    for artesao in artesaos:
        artesao['_id'] = str(artesao['_id'])
        if 'imagem_perfil' in artesao:
            artesao['imagem_perfil'] = base64.b64encode(artesao['imagem_perfil']).decode('utf-8')
    
    return jsonify(artesaos), 200