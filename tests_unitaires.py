import unittest
from io import BytesIO
from PIL import Image
from flask import request , json
import datetime
from app import app 
from static.models import Annonce , User
from static.db import db_init , db
import requests




class TestAddAnnonce(unittest.TestCase):  #classe pour tester ajouter annonce
    def test_add_annonce_post(self):
        with app.test_client() as client:
        # Test avec un prix valide
            # Preparation des données de l'annonce 
            image = Image.new("RGB", (234, 115), "#7f00ff")  
            image_io = BytesIO()
            image.save(image_io, format="JPEG")
            image_io.seek(0)

            data = {
                'name': 'Test Annonce',
                'categorie': 'Vente',
                'type': 'Appartement',
                'surface': '300',
                'description': 'Test unitaire de ajouter annonce',
                'prix': '1004360',
                'contact': 'ki_boudjadi@esi.dz',
                'wilaya': 'Alger',
                'commune': 'oued semar',
                'adresse': 'Appartement N 1',
                'image': (image_io, 'test.jpeg')
            }

            # envoyer un post pour ajouter l'annonce à la base de donnees 
            response = client.post('/add_annonce', data=data, content_type='multipart/form-data')
            
            # verifier si la reponse est correcte
            self.assertEqual(response.status_code, 200)

            # verifier que l'annonce est stockée dans la base de données 
            annonce = Annonce.query.filter_by(name='Test Annonce').first()  #recuperer l'annonce en utilisant "name"
            self.assertIsNotNone(annonce)  #verifier qu'on a trouvé l'annonce

            #verifier l'égalité des autres attributs
            self.assertEqual(annonce.categorie, 'Vente')
            self.assertEqual(annonce.type, 'Appartement')
            self.assertEqual(annonce.surface, 300)
            self.assertEqual(annonce.description, 'Test unitaire de ajouter annonce')
            self.assertEqual(annonce.prix, 1004360)
            self.assertEqual(annonce.contact, 'ki_boudjadi@esi.dz')
            self.assertEqual(annonce.wilaya, 'Alger')
            self.assertEqual(annonce.commune, 'oued semar')
            self.assertEqual(annonce.adresse, 'Appartement N 1')
            self.assertEqual(annonce.date.date(), datetime.datetime.utcnow().date())
            self.assertEqual(annonce.image, 'test.jpeg') 

        # Test avec un prix trop petit
            # Preparation des données de l'annonce 
            image = Image.new("RGB", (234, 115), "#6f00ff")  
            image_io = BytesIO()
            image.save(image_io, format="JPEG")
            image_io.seek(0)

            data1 = {
                'name': 'Test Annonce15',
                'categorie': 'Vente',
                'type': 'Appartement',
                'surface': '300',
                'description': 'Test unitaire de ajouter annonce',
                'prix': '3000',
                'contact': 'ki_boudjadi@esi.dz',
                'wilaya': 'Alger',
                'commune': 'oued semar',
                'adresse': 'Appartement N 1',
                'image': (image_io, 'test1.jpeg')
            }

            response = client.post('/add_annonce', data=data1 , content_type='multipart/form-data')
            # verifier si la reponse est correcte                                       
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data['error'], 'prix must be more than 10000')
    
        # Test avec un prix trop grand
            # Preparation des données de l'annonce 
            image = Image.new("RGB", (234, 115), "#3f00ff")  
            image_io = BytesIO()
            image.save(image_io, format="JPEG")
            image_io.seek(0)

            data2 = {
                'name': 'Test Annonce15',
                'categorie': 'Vente',
                'type': 'Appartement',
                'surface': '300',
                'description': 'Test unitaire de ajouter annonce',
                'prix': '30000000000',
                'contact': 'ki_boudjadi@esi.dz',
                'wilaya': 'Alger',
                'commune': 'oued semar',
                'adresse': 'Appartement N 1',
                'image': (image_io, 'test2.jpeg')   
            }

            response = client.post('/add_annonce', data=data2 , content_type='multipart/form-data')
            # verifier si la reponse est correcte                                        
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data['error'], 'prix must be less than 1000000000')


class TestAutho(unittest.TestCase):    #classe pour tester l'authentification
    
    def test_autho(self):
        with app.test_client() as client:
            #preparation des données de l'authentification
            data = {
                 'NAME': 'imene boudjadi',
                 'EMAIL': 'ki_boudjadi@esi.dz',
                 'googleid': '1111111'
            }
            # envoyer un post pour ajouter User à la base de données
            response = client.post('/autho', json=data)

            # verifier si la réponse est correcte
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'result': True})

            # verifier que User est stockée dans la base de données 
            user = User.query.filter_by(EMAIL='ki_boudjadi@esi.dz').first()  #recuperer l'annonce en utilisant "EMAIL"
            self.assertIsNotNone(user)  #verifier qu'on a trouvé User

            #verifier l'égalité des autres attributs.
            self.assertEqual(user.NAME, 'imene boudjadi')
            self.assertEqual(user.googleid, 1111111)   


class DeleteAnnonceTestCase(unittest.TestCase):    #classe pour tester la suppression de l'annonce
    def test_delete_annonce(self):
    # envoyer une requête DELETE à l'URL avec l'identifiant d'une annonce qui existe 
        response = requests.delete('http://localhost:5000/deleteAnnonce/13/')
        # vérifier si la réponse est correcte
        self.assertEqual(response.json(), {'result': True})
    # envoyer une requête DELETE à l'URL avec un identifiant d'annonce qui n'existe pas
        response = requests.delete('http://localhost:5000/deleteAnnonce/10000/')
        # vérifier si la réponse est correcte
        self.assertEqual(response.json(), {'result': False})


################### Lancement des tests unitaires #################

if __name__ == '__main__':
    unittest.main()