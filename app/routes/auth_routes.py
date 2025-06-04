from flask import Blueprint
from app.controllers.auth_controller import cadastrar_cliente, obter_cliente

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.route('/clientes', methods=['POST'])(cadastrar_cliente)
bp.route('/clientes/<string:cliente_id>', methods=['GET'])(obter_cliente)