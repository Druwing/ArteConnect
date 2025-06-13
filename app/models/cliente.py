from bson import ObjectId
import bcrypt
from datetime import datetime
from app.models.database import get_db

class Cliente:
    @staticmethod
    def criar_cliente(nome, email, senha):
        db = get_db()
        
        if db.clientes.find_one({"email": email}):
            return None
        
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        cliente_data = {
            'nome': nome,
            'email': email,
            'senha': hashed,
            'tipo': 'cliente',
            'data_criacao': datetime.now()
        }
        
        result = db.clientes.insert_one(cliente_data)
        return str(result.inserted_id)

    @staticmethod
    def verificar_credenciais(email, senha):
        db = get_db()
        cliente = db.clientes.find_one({"email": email})
        
        if cliente and bcrypt.checkpw(senha.encode('utf-8'), cliente['senha']):
            return cliente
        return None