from flask import Blueprint
from app.controllers.produto_controller import (
    criar_produto, listar_produtos
)
from app.controllers.auth_controller import login_required, artesao_required

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

bp.route('/', methods=['POST'])(login_required(artesao_required(criar_produto)))
bp.route('/', methods=['GET'])(listar_produtos)