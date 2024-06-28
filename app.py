from flask import Flask 
from flask import abort
import os
import sqlite3  #la base de données utilisées est SQLite
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy une bibliothèque qui permet de faire la liaison entre la base de données relationnelle (SQLite) et les objets python
from flask_marshmallow import Marshmallow
from flask import jsonify , render_template , redirect
from flask import Flask, request, Response # pour envoyer des requetes 
from werkzeug.utils import secure_filename
from PIL import Image
import io
import datetime #pour stocker la date de l'annonce 
import base64
from flask import make_response
from flask import json
from static.models import Annonce , User
from static.db import db_init , db
from flask import Flask, redirect, url_for, request , session
from flask_cors import CORS

######################################

app = Flask(__name__)
CORS(app)

######################################

app.config['SECRET'] = "secret12345" #secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tpigl.sqlite"
app.config['UPLOAD_FOLDER'] = 'static/images'

######################################
# initialiser la base de données 
db_init(app)


@app.route('/')
def home():
    return render_template('index2.html')



####################### Authentification #######################
@app.route('/autho', methods=['GET','POST'])
def Autho():
    """
    Autho permet d'authentifier en utilisant Single Sign-On (SSO) via Google , la méthode utilisée est POST.

    :return: true 
    :rtype: JSON
    """

    with app.app_context():
        if request.method=='POST':
                db.create_all()
                user = User (NAME = request.json['NAME'],  # Creer une instance user avec les informations recupéré
                        EMAIL=request.json['EMAIL'],
                        googleid=request.json['googleid'])
                users = User.query.all()   
                results = []
                #il faut verifier que cet User n'est pas encore ajouté à la base de donnees (existe déja)
                for userr in users:
                    if userr.EMAIL == request.json['EMAIL']: 
                        results.append(userr)
                    
                if not results:
                    db.session.add(user)  # on ajoute ce User a la base de données 
                    db.session.commit()    
                
                return jsonify({'result': True}) # retourne vrai
        return render_template('formulaire.html')
  
###################  Ajouter une annonce  #####################
@app.route('/add_annonce', methods=['GET', 'POST']) 
def add_annonce():
    """
    Ajouter annonce permet d'ajouter une annonce dans la base de données en récupérant les informations nécessaires à partir du formulaire. 

    :return: une annonce ajoutée en format JSON si les informations entrées sont valide sinon un message d'erreur 
    :rtype: JSON
    """    
    with app.app_context():
        if request.method == 'POST':  #la methode est POST
            db.create_all() # creation de la BDD si non deja crée

            image = Image.open(request.files['image'])
            image_io = io.BytesIO()
            if image.format =='PNG':
                image.save(image_io , format='PNG')
            elif image.format == 'JPEG':
                image.save(image_io , format='JPEG')     
            image_io.seek(0)
            
            annonce = Annonce(name=request.form['name'],  #creer l'annonce avec les attributs récupérés du formulaire
                            categorie = request.form['categorie'],
                            type = request.form['type'],
                            surface = request.form['surface'],
                            description = request.form['description'],
                            prix = request.form['prix'],
                            contact = request.form['contact'],
                            wilaya = request.form['wilaya'],
                            commune = request.form['commune'],
                            adresse = request.form['adresse'],
                            image=image_io.read(),
                            date=datetime.datetime.utcnow())
            prix = int(annonce.prix)
            if (prix < 10000):
                return jsonify({'error':'prix must be more than 10000'})
            if (prix > 1000000000):
                return jsonify({'error':'prix must be less than 1000000000'})
    
            db.session.add(annonce)   #ajouter l'annonce à la BDD
            db.session.commit()
  
            return jsonify(annonce.to_json()) # retourne l'annonce ajoutée en format JSON

        return render_template('add_annonce.html')

####################  Supprimer annonce  ####################
@app.route("/deleteAnnonce/<id>/",methods=['DELETE'])  # la méthode est DELETE
def delete(id):  #récuperer l’identifiant  de l'annonce
    """
    Supprimer annonce supprime une annonce de la base de données par l'utilisateur qui la créé.

    :param id: l'identifiant de l'annonce à supprimer
    :return: si  l'annonce que l'utilisateur veut supprimer existe , elle sera supprimer et la methode retourne "True" sinon "Faux"
    :rtype: JSON
    """
    myData = Annonce.query.get(id)  # chercher l'annonce qui a cet identifiant
    if myData is None:    #si non trouvé c'est a dire cette annonce n'existe pas 
       return jsonify({'result': False})  #retourne faux 
    db.session.delete(myData)  #si cette annonce est trouvée , on la supprime de la base de données
    db.session.commit()
    return jsonify({'result': True}) # retourne vrai   


########################### Delete User ############################
# permet de supprimer un utilisateur de la BDD en spécifiant son identifiant (id) 
@app.route("/deleteUser/<id>/",methods=['DELETE'])    # la méthode est DELETE
def deleteUser(id):   

    myData = User.query.get(id)   #récuperer l’identifiant  du User qu'on veut supprimer 
    if myData is None:      #si l'utilisateur n'existe pas 
       return jsonify({'result': False})  # retourne faux 
    db.session.delete(myData)  # sinon on le supprime de la BDD
    db.session.commit()
    return jsonify({'result': True})  # retourne vrai 
####################  Afficher les annonces  ####################
#permet d'afficher toutes les annonces en commençant par les plus récentes
@app.route("/affichAnnonces",methods=['GET'])  # la méthode est GET
def get_annonces():
    """
    get_annonces affiche toutes les annonces ajoutées par les différents utilisateurs.

    :return: toutes annonces qui se trouvent dans la base de données
    :rtype: JSON
    """
    annonces = Annonce.query.all() #on recupere toutes les annonces de la BDD
    sorted_annonces = sorted(annonces, key=lambda x: x.date, reverse=True)  # On les trie en commençant par les plus récentes.
    result = []
    for annonce in sorted_annonces: #on parcourt la liste des anonces
        test = annonce
        test.image = base64.b64encode(test.image)
        if str(test.image)[-3:] == "=":
            testd = {'id':test.id ,
            'name': test.name ,
            'categorie': test.categorie ,
            'type': test.type ,
            'surface': test.surface ,
            'description': test.description ,
            'prix': test.prix ,
            'contact': test.contact ,
            'wilaya' : test.wilaya ,
            'commune' : test.commune ,
            'adresse' : test.adresse,
            'image' : str(test.image)[2:-3],
            'date' : test.date,}
        else:
            testd = {'id':test.id ,
            'name': test.name ,
            'categorie': test.categorie ,
            'type': test.type ,
            'surface': test.surface ,
            'description': test.description ,
            'prix': test.prix ,
            'contact': test.contact ,
            'wilaya' : test.wilaya ,
            'commune' : test.commune ,
            'adresse' : test.adresse,
            'image' : str(test.image)[2:-2],
            'date' : test.date,}
        result.append(testd)
    return jsonify([Annonce for Annonce in result])

####################  Afficher les details de l'annonce  ####################
# cette route permet d'afficher les détails d'une annonce c'est à dire toutes ses informations 
@app.route("/detailAnnonce/<id>/",methods=['GET']) #la méthode est GET
def detail(id): 
    """
    afficher les détails d'une annonce spécifique.

    :param id: l'identifiant de l'annonce qu'on veut afficher ses details
    :return: toutes les informations de l'annoce
    :rtype: JSON
    """
    Annoncee = Annonce.query.get(id)  #on cherche l'annonce en utilisant l'id
    if Annoncee is None: #si elle n'existe pas 
        return jsonify({'result': False})  #on retourne faux 
    return jsonify(Annoncee.to_json())  #sinon on retourne toutes ses informations en format JSON


###################### Afficher l'image d'une annonce ########################
@app.route('/img/<int:annonce_id>/', methods=['GET']) # la methode utilisee et GET
def annonce_photo(annonce_id):
    annonce = Annonce.query.get(annonce_id)  # on cherche l'annonce par son id  
    if annonce is None:
        return jsonify({'result': False}) #si on trouvé retourne faux
    #sinon
    response = make_response(annonce.image) #on recupere l'image de l'annonce de la BDD
    response.headers.set('Content-Type', 'image/jpeg')
    return response  #on retourne l'image
    

################# Recherche ########################
#permet de rechercher, dans le titre et la description, toutes les AI contenant un ou plusieurs mots spécifiés par l’utilisateur.
@app.route("/search", methods=["GET"]) #la methode est GET
def search():
    """
    Rechercher, dans le titre et la description, toutes les annonces immobilières contenant un ou plusieurs mots spécifiés par l'utilisateur.

    :return: les annonces trouvées apres la recherche
    :rtype: JSON
    """
    keywords = request.args.get("keywords")  #on recupére les mots clés
    keywords = keywords.split() # on les sépare pour vérifier chaque clé 
    if not keywords:  
        return "Please provide a search query", 400

    results = []  #on initialise la liste des résultats à vide
    annonces = Annonce.query.all() # on recupere toutes les annonces de la BDD
    for annonce in annonces:  # boucle pour verifier toutes les annonces
        if all(keyword in annonce.name or keyword in annonce.description for keyword in keywords):  # pour tout les mots clés , si on trouve un mot dans le titre ou la description de l'AI
            results.append(annonce)  # on ajoute cette annonce à la liste des resultats
    if not results:
        return "No matching ads found", 404
    else :
        sorted_annonces = sorted(results, key=lambda x: x.date, reverse=True) # on trie les resultats pour les afficher en commençant par les plus récentes  
        result = []
        for annonce in sorted_annonces: #on parcourt la liste des anonces
                test = annonce
                test.image = base64.b64encode(test.image)
                if str(test.image)[-3:] == "=":
                    testd = {'id':test.id ,
                    'name': test.name ,
                    'categorie': test.categorie ,
                    'type': test.type ,
                    'surface': test.surface ,
                    'description': test.description ,
                    'prix': test.prix ,
                    'contact': test.contact ,
                    'wilaya' : test.wilaya ,
                    'commune' : test.commune ,
                    'adresse' : test.adresse,
                    'image' : str(test.image)[2:-3],
                    'date' : test.date,}
                else:
                    testd = {'id':test.id ,
                    'name': test.name ,
                    'categorie': test.categorie ,
                    'type': test.type ,
                    'surface': test.surface ,
                    'description': test.description ,
                    'prix': test.prix ,
                    'contact': test.contact ,
                    'wilaya' : test.wilaya ,
                    'commune' : test.commune ,
                    'adresse' : test.adresse,
                    'image' : str(test.image)[2:-2],
                    'date' : test.date,}
                result.append(testd)
        return jsonify([Annonce for Annonce in result]) # on les retourne en format JSON

############# filtrage entre deux dates ############
# permet d'afficher les anoonces ajoutées entre deux dates de publication
@app.route('/annonces/<startDate>/<endDate>')
def filtered_annonces(startDate, endDate):
    """
    filtrer les annonces immobilières selon la période entre deux dates de publication

    :param startDate: la date de début de la période
    :param endDate: la date de fin de la période
    :return: les annonces trouvées apres le filtrage
    :rtype: JSON
    """
    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').date()  #on recupere la date de debut 
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d').date() #et la date de fin  
    annonces = Annonce.query.filter(Annonce.date.between(startDate, endDate)).all() #on filtre les annonces afin de trouver les annonces ajoutees entre la date de debut et de fin 
    result = []

    annonces =  sorted(annonces, key=lambda x: x.date, reverse=True) # en les trie en commençant par les plus récentes  
    for annonce in annonces:
        test = annonce
        test.image = base64.b64encode(test.image)
        testd = {'id':test.id ,
            'name': test.name ,
            'categorie': test.categorie ,
            'type': test.type ,
            'surface': test.surface ,
            'description': test.description ,
            'prix': test.prix ,
            'contact': test.contact ,
            'wilaya' : test.wilaya ,
            'commune' : test.commune ,
            'adresse' : test.adresse,
            'image' : str(test.image)[2:-2],
            'date' : test.date,}
        result.append(testd)
    return jsonify([Annonce for Annonce in result]) # on les retourne en format JSON


####################### Afficher mes annonces #######################
# Permet a un utilisateur d'afficher ou de visualiser ses annonces seulement 
@app.route("/MesAnnonces/<email>", methods=["GET"])
def afficher_annonces_utilisateur(email):  
    """
    Afficher les annonces immobilières ajoutées par un utilisateur (l'utilisateur veut afficher ses annonces)

    :param email: l'email de ce utilisateur
    :return: les annonces de l'utilisateur
    :rtype: JSON
    """
    annonces= Annonce.query.all() # on recupere les annonces de la BDD
    annonces =  sorted(annonces, key=lambda x: x.date, reverse=True) # en les trie en commençant par les plus récentes  
    annonces_utilisateur = []  # on initialise la liste "annonces_utilisateur" à vide 
    for annonce in annonces :  # on parcourt les annonces 
        if annonce.contact ==email:    # si l'utilisateur qui a crée l'annonce est le meme que l'utilisateur courant 
            test = annonce
            test.image = base64.b64encode(test.image)
            if str(test.image)[-3:] == "=":
                testd = {'id':test.id ,
                'name': test.name ,
                'categorie': test.categorie ,
                'type': test.type ,
                'surface': test.surface ,
                'description': test.description ,
                'prix': test.prix ,
                'contact': test.contact ,
                'wilaya' : test.wilaya ,
                'commune' : test.commune ,
                'adresse' : test.adresse,
                'image' : str(test.image)[2:-3],
                'date' : test.date,}
            else:
                testd = {'id':test.id ,
                'name': test.name ,
                'categorie': test.categorie ,
                'type': test.type ,
                'surface': test.surface ,
                'description': test.description ,
                'prix': test.prix ,
                'contact': test.contact ,
                'wilaya' : test.wilaya ,
                'commune' : test.commune ,
                'adresse' : test.adresse,
                'image' : str(test.image)[2:-2],
                'date' : test.date,}
            annonces_utilisateur.append(testd)   # on ajoute cette annonce à "annonces_utilisateur"
    return jsonify([Annonce for Annonce in annonces_utilisateur])  # retourne les annonces du resultat en format JSON   
############## filtrage de l'annonce ###############
# cette route filtre les annonces selon le type , la wilaya ou la commune
@app.route("/filtreAd", methods=["GET"])  #la methode est GET
def filtrer(): 
    """
    filtrer les annonces immobilières selon le type , la wilaya ou la commune 
   
    :return: les annonces trouvées apres le filtrage 
    :rtype: JSON   
    """
    filtre = request.args.get("filtre") # on recupere le critère de filtrage (type , wilaya ou commune)
    info = request.args.get("info")  # on récupere l'information supplémentaire 
    filtered_annonces = Annonce.query.all() # on recupere les annonces de la BDD
    filtered_annonces =  sorted(filtered_annonces, key=lambda x: x.date, reverse=True) # n les trie en commençant par les plus récentes  
    if filtre == "type" : # si le critère est le type , 
        result = []
        for annonce in filtered_annonces: # on parcourt la liste des anonces
            if annonce.type == info :   # si le type de l'annonce est le meme que le type entré 
                test = annonce
                test.image = base64.b64encode(test.image)
                testd = {'id':test.id ,
                    'name': test.name ,
                    'categorie': test.categorie ,
                    'type': test.type ,
                    'surface': test.surface ,
                    'description': test.description ,
                    'prix': test.prix ,
                    'contact': test.contact ,
                    'wilaya' : test.wilaya ,
                    'commune' : test.commune ,
                    'adresse' : test.adresse,
                    'image' : str(test.image)[2:-2],
                    'date' : test.date,}
                result.append(testd)  

        return jsonify([Annonce for Annonce in result]) # on les retourne en format JSON

    elif filtre == "wilaya" : # si le critère est la wilaya
        result = []
        for annonce in filtered_annonces: #on parcourt la liste des anonces
            if annonce.wilaya == info :  # si la wilaya de l'annonce est la meme que la wilaya entrée
                test = annonce
                test.image = base64.b64encode(test.image)
                testd = {'id':test.id ,
                    'name': test.name ,
                    'categorie': test.categorie ,
                    'type': test.type ,
                    'surface': test.surface ,
                    'description': test.description ,
                    'prix': test.prix ,
                    'contact': test.contact ,
                    'wilaya' : test.wilaya ,
                    'commune' : test.commune ,
                    'adresse' : test.adresse,
                    'image' : str(test.image)[2:-2],
                    'date' : test.date,}
                result.append(testd)
                
        return jsonify([Annonce for Annonce in result]) # on les retourne en format JSON

    elif filtre == "commune" : # si le critère est la commune
        result = []
        for annonce in filtered_annonces: #on parcourt la liste des anonces
            if annonce.commune== info :  # si la commune de l'annonce est la meme que la commune entrée
                test = annonce
                test.image = base64.b64encode(test.image)
                testd = {'id':test.id ,
                    'name': test.name ,
                    'categorie': test.categorie ,
                    'type': test.type ,
                    'surface': test.surface ,
                    'description': test.description ,
                    'prix': test.prix ,
                    'contact': test.contact ,
                    'wilaya' : test.wilaya ,
                    'commune' : test.commune ,
                    'adresse' : test.adresse,
                    'image' : str(test.image)[2:-2],
                    'date' : test.date,}
                result.append(testd)
                
        return jsonify([Annonce for Annonce in result]) # on les retourne en format JSON


############  Lancement de l'appliction  ###########

if __name__ == '__main__' :
    app.run(debug=True)

#################################################### 
