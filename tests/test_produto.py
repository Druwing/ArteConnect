import unittest
from bson import ObjectId
from app import create_app
from config import Config
from app.models.database import get_db

class TestProduto(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()
        self.db = get_db()
        
        # Limpar coleções antes de cada teste
        self.db.produtos.delete_many({})
        self.db.artesaos.delete_many({})
        
        # Criar artesão de teste
        self.artesao_id = self.db.artesaos.insert_one({
            'nome': 'Artesão Teste',
            'bio': 'Bio de teste'
        }).inserted_id
        
        # Dados de teste
        self.produto_data = {
            'nome': 'Produto Teste',
            'descricao': 'Descrição de teste',
            'preco': 100.50,
            'disponibilidade': True,
            'artesao_id': str(self.artesao_id),
            'imagem_url': 'http://exemplo.com/imagem.jpg'
        }
    
    def test_cadastrar_produto(self):
        response = self.client.post('/produtos/', json=self.produto_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('produto_id', response.json)
    
    def test_listar_produtos(self):
        # Primeiro cadastra
        self.client.post('/produtos/', json=self.produto_data)
        
        # Depois busca
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
    
    def tearDown(self):
        self.db.produtos.delete_many({})
        self.db.artesaos.delete_many({})

if __name__ == '__main__':
    unittest.main()