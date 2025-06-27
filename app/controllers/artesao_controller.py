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
        imagem_perfil=imagem_binaria,
        email=data['email'],
        senha=data['senha']
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
    imagem = artesao.get('imagem_perfil')
    if imagem:
        if isinstance(imagem, str):
            # Already a string, just use it
            artesao['imagem_perfil'] = imagem
        elif hasattr(imagem, 'tobytes'):
            imagem_bytes = imagem.tobytes()
            artesao['imagem_perfil'] = (
                "data:image/png;base64," +
                base64.b64encode(imagem_bytes).decode('utf-8')
            )
        else:
            imagem_bytes = bytes(imagem)
            artesao['imagem_perfil'] = (
                "data:image/png;base64," +
                base64.b64encode(imagem_bytes).decode('utf-8')
            )
    else:
        artesao['imagem_perfil'] = None
    if 'senha' in artesao:
        del artesao['senha']

    return jsonify(artesao), 200

def listar_artesaos():
    artesaos = Artesao.listar_artesaos()
    for artesao in artesaos:
        artesao['_id'] = str(artesao['_id'])
        # Remove password and other sensitive fields if present
        if 'senha' in artesao:
            del artesao['senha']
    return jsonify(artesaos), 200