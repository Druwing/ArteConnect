from bson import ObjectId
from app.models.database import get_db
from datetime import datetime

class Carrinho:
    @staticmethod
    def obter_carrinho(cliente_id):
        db = get_db()
        carrinho = db.carrinhos.find_one({'cliente_id': ObjectId(cliente_id)})
        if not carrinho:
            carrinho_id = db.carrinhos.insert_one({
                'cliente_id': ObjectId(cliente_id),
                'produtos': [],
                'data_criacao': datetime.now()
            }).inserted_id
            carrinho = db.carrinhos.find_one({'_id': carrinho_id})
        return carrinho

    @staticmethod
    def adicionar_produto(cliente_id, produto_id, quantidade):
        db = get_db()
        db.carrinhos.update_one(
            {'cliente_id': ObjectId(cliente_id)},
            {'$push': {'produtos': {'produto_id': ObjectId(produto_id), 'quantidade': quantidade}}},
            upsert=True
        )

    @staticmethod
    def adicionar_produtos(cliente_id, produtos):
        db = get_db()
        carrinho = db.carrinhos.find_one({'cliente_id': ObjectId(cliente_id)})
        if not carrinho:
            # Cria o carrinho se não existir
            db.carrinhos.insert_one({
                'cliente_id': ObjectId(cliente_id),
                'produtos': [],
                'data_criacao': datetime.now()
            })
            carrinho = db.carrinhos.find_one({'cliente_id': ObjectId(cliente_id)})

        produtos_atualizados = carrinho.get('produtos', [])

        for item in produtos:
            produto_id = item.get('produto_id')
            quantidade = item.get('quantidade', 1)
            if not produto_id:
                continue
            # Verifica se o produto já está no carrinho
            encontrado = False
            for prod in produtos_atualizados:
                if str(prod['produto_id']) == str(produto_id):
                    prod['quantidade'] += quantidade
                    encontrado = True
                    break
            if not encontrado:
                produtos_atualizados.append({
                    'produto_id': ObjectId(produto_id),
                    'quantidade': quantidade
                })

        db.carrinhos.update_one(
            {'cliente_id': ObjectId(cliente_id)},
            {'$set': {'produtos': produtos_atualizados}}
        )

    @staticmethod
    def remover_produto(cliente_id, produto_id, quantidade=1):
        db = get_db()
        carrinho = db.carrinhos.find_one({'cliente_id': ObjectId(cliente_id)})
        if not carrinho or not carrinho.get('produtos'):
            return {'error': 'Carrinho vazio ou não encontrado'}

        produtos = carrinho['produtos']
        for prod in produtos:
            if str(prod['produto_id']) == str(produto_id):
                if quantidade > prod['quantidade']:
                    return {'error': 'Tentando remover quantidade maior do que a disponível no carrinho'}
                elif quantidade == prod['quantidade']:
                    produtos.remove(prod)
                else:
                    prod['quantidade'] -= quantidade
                db.carrinhos.update_one(
                    {'cliente_id': ObjectId(cliente_id)},
                    {'$set': {'produtos': produtos}}
                )
                return {'success': True}
        return {'error': 'Produto não encontrado no carrinho'}

    @staticmethod
    def limpar_carrinho(cliente_id):
        db = get_db()
        db.carrinhos.update_one(
            {'cliente_id': ObjectId(cliente_id)},
            {'$set': {'produtos': []}}
        )