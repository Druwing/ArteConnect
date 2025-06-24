from flask import Blueprint
from app.controllers.artesao_controller import obter_artesao, listar_artesaos
from app.controllers.auth_controller import login_required

bp = Blueprint('artesaos', __name__, url_prefix='/artesaos')

bp.route('/', methods=['GET'])(login_required(listar_artesaos))
bp.route('/<string:artesao_id>', methods=['GET'])(login_required(obter_artesao))