import unittest
import base64
from bson.binary import Binary
from app import create_app
from config import Config
from app.models.database import get_db

class TestArtesao(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Config)
        self.client = self.app.test_client()
        self.db = get_db()
        
        # Limpar coleções antes de cada teste
        self.db.artesaos.delete_many({})
        
        # Dados de teste
        self.artesao_data = {
            'nome': 'Teste Artesão',
            'bio': 'Bio de teste',
            'imagem_perfil': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
        }
    
    def test_cadastrar_artesao(self):
        response = self.client.post('/artesaos/', json=self.artesao_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('artesao_id', response.json)
    
    def test_obter_artesao(self):
        # Primeiro cadastra
        post_response = self.client.post('/artesaos/', json=self.artesao_data)
        artesao_id = post_response.json['artesao_id']
        
        # Depois busca
        get_response = self.client.get(f'/artesaos/{artesao_id}')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json['nome'], self.artesao_data['nome'])
    
    def tearDown(self):
        self.db.artesaos.delete_many({})

if __name__ == '__main__':
    unittest.main()