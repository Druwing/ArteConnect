from flask import Blueprint
from app.controllers.produto_controller import (
    criar_produto,
    listar_produtos,
    remover_produto,
    remover_todos_produtos,
    atualizar_quantidade_produto
)
from app.controllers.auth_controller import login_required, artesao_required

bp = Blueprint('produtos', __name__, url_prefix='/produtos')

bp.route('/', methods=['POST'])(login_required(artesao_required(criar_produto)))
bp.route('/', methods=['GET'])(listar_produtos)
bp.route('/remover', methods=['POST'])(login_required(artesao_required(remover_produto)))
bp.route('/remover_todos', methods=['POST'])(login_required(artesao_required(remover_todos_produtos)))
bp.route('/atualizar_quantidade', methods=['POST'])(login_required(artesao_required(atualizar_quantidade_produto)))