from bson import ObjectId
import bcrypt
from datetime import datetime
from app.models.database import get_db

class Artesao:
    @staticmethod
    def criar_artesao(nome, email, senha, bio, imagem_perfil):
        db = get_db()
        
        if db.artesaos.find_one({"email": email}):
            return None
        
        hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        
        artesao_data = {
            'nome': nome,
            'email': email,
            'senha': hashed,
            'bio': bio,
            'imagem_perfil': imagem_perfil,
            'tipo': 'artesao',
            'data_criacao': datetime.utcnow()
        }
        
        result = db.artesaos.insert_one(artesao_data)
        return str(result.inserted_id)

    @staticmethod
    def verificar_credenciais(email, senha):
        db = get_db()
        artesao = db.artesaos.find_one({"email": email})
        
        if artesao and bcrypt.checkpw(senha.encode('utf-8'), artesao['senha']):
            return artesao
        return None

    @staticmethod
    def listar_artesaos():
        db = get_db()
        return list(db.artesaos.find({}))

    @staticmethod
    def obter_artesao(artesao_id):
        db = get_db()
        return db.artesaos.find_one({'_id': ObjectId(artesao_id)})