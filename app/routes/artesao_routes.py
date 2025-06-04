from flask import Blueprint
from app.controllers.artesao_controller import cadastrar_artesao, obter_artesao, listar_artesaos

bp = Blueprint('artesaos', __name__, url_prefix='/artesaos')

bp.route('/', methods=['POST'])(cadastrar_artesao)
bp.route('/', methods=['GET'])(listar_artesaos)
bp.route('/<string:artesao_id>', methods=['GET'])(obter_artesao)