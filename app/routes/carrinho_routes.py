from flask import Blueprint
from app.controllers.carrinho_controller import (
    ver_carrinho, adicionar_ao_carrinho, remover_do_carrinho, limpar_carrinho, checkout
)
from app.controllers.auth_controller import login_required

bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

bp.route('/', methods=['GET'])(login_required(ver_carrinho))
bp.route('/adicionar', methods=['POST'])(login_required(adicionar_ao_carrinho))
bp.route('/remover', methods=['POST'])(login_required(remover_do_carrinho))
bp.route('/limpar', methods=['POST'])(login_required(limpar_carrinho))
bp.route('/checkout', methods=['POST'])(login_required(checkout))