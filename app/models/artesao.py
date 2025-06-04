from bson import ObjectId
from app.models.database import get_db

class Artesao:
    @staticmethod
    def criar_artesao(nome, bio, imagem_perfil):
        db = get_db()
        artesao_data = {
            'nome': nome,
            'bio': bio,
            'imagem_perfil': imagem_perfil
        }
        return db.artesaos.insert_one(artesao_data).inserted_id
    
    @staticmethod
    def obter_artesao(artesao_id):
        db = get_db()
        return db.artesaos.find_one({'_id': ObjectId(artesao_id)})
    
    @staticmethod
    def listar_artesaos():
        db = get_db()
        return list(db.artesaos.find({}))