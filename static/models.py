# Ce fichier cintient les classes 
from static.db import db
import datetime # pour stocker la date de l'annonce

#################  Classe Annonce  #################
# classe annonce qui a comme attributs : identifiant , titre de l'annonce , categorie , type , surface , description , prix , cidentifiant de l'utilisateur qui a ajouté l'annonce , wilaya , commune , adresse  , image et la date de publication
class Annonce(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    categorie =  db.Column(db.Text, nullable=False)
    type =  db.Column(db.Text, nullable=False)
    surface = db.Column(db.Float,  nullable=False)
    description = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Float,  nullable=False)
    contact = db.Column(db.Text, nullable=False)
    # utilisateur_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # localisation : wilaya , commune , adresse
    wilaya = db.Column(db.Text, nullable=False)
    commune = db.Column(db.Text, nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow) # pour la date de publication on utilise la bibliothèque "datetime" qui permet de manipuler des dates, des heures et des intervalles de temps.

    
    def __init__(self , name , categorie , type , surface , description , prix , contact , wilaya , commune , adresse ,  image , date ):  # initialisation
        self.name=name
        self.categorie = categorie
        self.type = type
        self.surface = surface
        self.description = description
        self.prix = prix
        self.contact = contact
        self.wilaya = wilaya
        self.commune = commune
        self.adresse = adresse
        self.image = image
        self.date = date 

    def to_json(self):  # pour retourner les attributs de l'annonce
        return {
            'id': self.id ,
            'name': self.name ,
            'categorie': self.categorie ,
            'type': self.type ,
            'surface': self.surface ,
            'description': self.description ,
            'prix': self.prix ,
            'contact': self.contact ,
            'wilaya' : self.wilaya ,
            'commune' : self.commune ,
            'adresse' : self.adresse,
            'date' : self.date,
        }


####################################
####################################
#####################################

# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)

#     def __init__(self,id , name,email) :
#         self.id = id
#         self.name= name
#         self.email=email 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    EMAIL= db.Column(db.String(100), nullable=False)
    googleid = db.Column(db.Integer , nullable=False) 

    def __init__(self,NAME,EMAIL,googleid):
        self.NAME=NAME
        self.EMAIL=EMAIL
        self.googleid=googleid 

    # def __repr__(self):
    #     return '<User %r>' % self.EMAIL