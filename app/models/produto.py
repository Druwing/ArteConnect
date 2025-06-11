from bson import ObjectId
from app.models.database import get_db

class Produto:
    @staticmethod
    def criar_produto(nome, descricao, preco, disponibilidade, artesao_id, imagem_url):
        db = get_db()
        produto_data = {
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'disponibilidade': disponibilidade,
            'artesao_id': ObjectId(artesao_id),
            'imagem_url': imagem_url
        }
        return db.produtos.insert_one(produto_data).inserted_id
    
    @staticmethod
    def obter_produto(produto_id):
        db = get_db()
        return db.produtos.find_one({'_id': ObjectId(produto_id)})
    
    @staticmethod
    def listar_produtos(filtros=None):
        db = get_db()
        query = {}
        
        if filtros:
            if 'categoria' in filtros:
                query['categoria'] = filtros['categoria']
            if 'preco_min' in filtros and 'preco_max' in filtros:
                query['preco'] = {'$gte': float(filtros['preco_min']), '$lte': float(filtros['preco_max'])}
        
        return list(db.produtos.find(query))
    
    @staticmethod
    def adicionar_comentario(produto_id, cliente_id, nota, texto):
        db = get_db()
        comentario = {
            'cliente_id': ObjectId(cliente_id),
            'nota': nota,
            'texto': texto,
            'data': datetime.datetime.utcnow()
        }
        return db.produtos.update_one(
            {'_id': ObjectId(produto_id)},
            {'$push': {'comentarios': comentario}}
        )
    
    @staticmethod
    def obter_comentarios(produto_id):
        db = get_db()
        produto = db.produtos.find_one(
            {'_id': ObjectId(produto_id)},
            {'comentarios': 1}
        )
        return produto.get('comentarios', []) if produto else []