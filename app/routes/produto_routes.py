from flask import Blueprint
from app.controllers.produto_controller import (
    cadastrar_produto, listar_produtos, adicionar_comentario, obter_comentarios
)

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

bp.route('/', methods=['POST'])(cadastrar_produto)
bp.route('/', methods=['GET'])(listar_produtos)
bp.route('/<string:produto_id>/comentarios', methods=['POST'])(adicionar_comentario)
bp.route('/<string:produto_id>/comentarios', methods=['GET'])(obter_comentarios)