from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy.orm import backref


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_categorie = db.Column(db.String(128))
    produits = db.relationship('Produit', backref='produit_categorie', lazy='dynamic')
    articles_associ=db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return ' {} '.format(self.nom_categorie)
    
def Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_produit = db.Column(db.String(128))
    nom_produit = db.Column(db.String(128))
    description = db.Column(db.Text)
    vt_gros_piece = db.Column(db.DECIMAL(precision=30, scale=16))
    vt_detaille_piece = db.Column(db.DECIMAL(precision=30, scale=16))
    vt_gros_entier = db.Column(db.DECIMAL(precision=30, scale=16))
    cout_d_achat = db.Column(db.DECIMAL(precision=30, scale=16))
    avatar = db.Column(db.String(128), default="avatar.jpg")
    emballage = db.Column(db.String(128))
    nombre_contenu=db.Column(db.Integer, default=1)
    stock_de_securite = db.Column(db.Integer)
    perissable=db.Column(db.Boolean, default=False) 
    unite_mesure = db.Column(db.String(128))
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    perrisables = db.relationship('Perrisable', backref='produit_perrisable', lazy='dynamic')
    valeurs=db.relationship('Valeurstock', backref='produit_valeur', lazy='dynamic')
    ventes = db.relationship('Vente', backref='produit_vente', lazy='dynamic')
    stocks = db.relationship('Stock', backref='produit_stock', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.code_produit)

def Perrisable(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    qte=db.Column(db.Integer)
    date_op= db.Column(db.Date)
    date_expiration=db.Column(db.Date)
    produit_id =db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    depot=db.Column(db.Boolean, default=False)
    boutique=db.Column(db.Boolean, default=False)
    date_fabrication=db.Column(db.Date)
    
    def __repr__(self):
        return ' {} '.format(self.qte)

def Stock(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    qte=db.Column(db.Integer)
    prix_unit=db.Column(db.DECIMAL(precision=30, scale=16))
    qte_total=db.Column(db.DECIMAL(precision=30, scale=16))
    valeur_total=db.Column(db.DECIMAL(precision=30, scale=16))
    date_op=db.Column(db.Date)
    transfert=db.Column(db.Boolean, default=False)
    correction_plus=db.Column(db.Boolean, default=False)
    correction_moins=db.Column(db.Boolean, default=False)
    erreur=db.Column(db.Boolean, default=False)
    solde=db.Column(db.Boolean, default=False)
    produit_id=db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    boutique=db.Column(db.Boolean, default=False)
    depot=db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return ' {} '.format(self.qte)

def User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    post_nom = db.Column(db.String(128))
    prenom= db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    password_onhash = db.Column(db.String(128))
    statut=db.Column(db.Boolean, default=False)
    avatar=db.Column(db.String(128), default='user.png')
    role = db.Column(db.String(128))
    boutique = db.Column(db.Boolean, default=False)
    depot = db.Column(db.Boolean, default=False)
    stocks = db.relationship('Stock', backref='user_stock', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.nom)

def Valeurstock(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    qte=db.Column(db.Integer)
    montant=db.Column(db.DECIMAL(precision=30, scale=16))
    prix_unit=db.Column(db.DECIMAL(precision=30, scale=16))
    montant_total=db.Column(db.DECIMAL(precision=30, scale=16))
    facture_id=db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    produit_id=db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    vente_id=db.Column(db.Integer, db.ForeignKey('vente.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.qte)

def Facture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_facture = db.Column(db.String(128))
    montant = db.Column(db.DECIMAL(precision=30, scale=16), default=0)
    valeur_vendue = db.Column(db.DECIMAL(precision=30, scale=16), default=0)
    cash = db.Column(db.Boolean, default=False)
    dette = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date)
    valeurstocks = db.relationship('Valeurstock', backref='facture_valeur', lazy='dynamic')
    ventes = db.relationship('Vente', backref='facture_vente', lazy='dynamic')
    
    def __repr__(self):
        return ' {} '.format(self.montant)

def Vente(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    qte=db.Column(db.Integer)
    montant=db.Column(db.DECIMAL(precision=30, scale=16))
    prix_unit=db.Column(db.DECIMAL(precision=30, scale=16))
    montant_total=db.Column(db.DECIMAL(precision=30, scale=16))
    facture_id=db.Column(db.Integer, db.ForeignKey('facture.id'), nullable=False)
    produit_id=db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    
    def __repr__(self):
        return ' {} '.format(self.qte)
