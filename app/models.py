from app import db, login_manager
from datetime import datetime, date
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_produit=db.Column(db.String(200))
    description=db.Column(db.String(200))
    cout_achat=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    prix_detaille=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    emballage=db.Column(db.Integer)
    nombre_contenu = db.Column(db.Integer)
    piece = db.Column(db.Integer)
    mesure=db.Column(db.String(200))
    perissable=db.Column(db.Boolean, default=False)
    statut=db.Column(db.Boolean, default=True)
    perissables = db.relationship('Perissable', backref='produit_perissable', lazy='dynamic')
    stocks = db.relationship('Stock', backref='produit_stock', lazy='dynamic')
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.nom_produit)
    
    
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_categorie=db.Column(db.String(200))
    statut=db.Column(db.Boolean, default=True)
    produits = db.relationship('Produit', backref='categorie_produit', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.nom_categorie)
    
class Perissable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite=db.Column(db.Integer)
    date_op=db.Column(db.Date, default=date.today())
    date_expiration=db.Column(db.Date)
    date_fabrication=db.Column(db.Date)
    boutique=db.Column(db.Boolean, default=True)
    depot=db.Column(db.Boolean, default=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.quantite)

    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite=db.Column(db.Integer)
    prix_unitaire=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    quantite_total=db.Column(db.Integer)
    valeur_total=db.Column(db.Integer)
    montant_total=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    date_op=db.Column(db.Date, default=date.today())
    vente=db.Column(db.Boolean, default=True)
    transfert=db.Column(db.Boolean, default=True)
    correction_plus=db.Column(db.Boolean, default=True)
    correction_moins=db.Column(db.Boolean, default=True)
    erreur=db.Column(db.Boolean, default=True)
    solde=db.Column(db.Boolean, default=True)
    boutique=db.Column(db.Boolean, default=True)
    depot=db.Column(db.Boolean, default=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.quantite)
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(200))
    post_nom=db.Column(db.String(200))
    prenom=db.Column(db.String(200))
    role=db.Column(db.String(200))
    username=db.Column(db.String(200))
    password=db.Column(db.String(200))
    statut=db.Column(db.Boolean, default=True)    
    perissables = db.relationship('Perissable', backref='user_perissable', lazy='dynamic')
    stocks = db.relationship('Stock', backref='user_stock', lazy='dynamic')
    factures = db.relationship('Facture', backref='user_facture', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.nom)

class ValeurStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite=db.Column(db.Integer)
    prix_unitaire=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    montant_total=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.quantite)

class Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_facture=db.Column(db.String(200))
    valeur=db.Column(db.String(200))
    date_op=db.Column(db.Date, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    valeur_stocks = db.relationship('ValeurStock', backref='facture_valeurStock', lazy='dynamic')
    ventes = db.relationship('Vente', backref='facture_vente', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.code_facture)
    

class Vente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite=db.Column(db.Integer)
    prix_unitaire=db.Column(db.DECIMAL(precision=10, scale=2, asdecimal=False))
    valeur=db.Column(db.String(200))
    facture_id = db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.prix_unitaire)
    


    