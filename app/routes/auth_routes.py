from flask import Blueprint
from app.controllers.auth_controller import (
    cadastrar_artesao, cadastrar_cliente, login,
    login_required, artesao_required
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.route('/artesaos', methods=['POST'])(cadastrar_artesao)
bp.route('/clientes', methods=['POST'])(cadastrar_cliente)
bp.route('/login', methods=['POST'])(login)