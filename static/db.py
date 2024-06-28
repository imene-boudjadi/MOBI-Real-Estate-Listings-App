from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  


# Fonction qui initialise la base de données et cree les tables 
def db_init(app):
    db.init_app(app)

    # Création des tables si la base de données n'existe pas encore. 
    with app.app_context():
        db.create_all()

