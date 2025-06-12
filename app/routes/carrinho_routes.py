from flask import Blueprint
from app.controllers.carrinho_controller import (
    ver_carrinho, adicionar_ao_carrinho, remover_do_carrinho, limpar_carrinho
)

bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

bp.route('/', methods=['GET'])(ver_carrinho)
bp.route('/adicionar', methods=['POST'])(adicionar_ao_carrinho)
bp.route('/remover', methods=['POST'])(remover_do_carrinho)
bp.route('/limpar', methods=['POST'])(limpar_carrinho)