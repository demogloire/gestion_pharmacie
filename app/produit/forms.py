from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField,IntegerField, DecimalField
from wtforms.validators import DataRequired, Length,Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Categorie


def rech_cate():
    return Categorie.query.filter_by(statut=True).all()

class ProduitAForm(FlaskForm):
    nom_produit=StringField('Nom', validators=[DataRequired("Completer nom"),  Length(min=4, max=60, 
                    message="Veuillez respecter la longeur de 2 à 60")])
    description=TextAreaField('Contenu', validators=[DataRequired("Description du produit")])
    cout_achat = DecimalField('Prix pièce e n gros', validators=[DataRequired("Le prix de pièce de gors en decimal")])
    prix_detaille = DecimalField('Prix pièce detaille', validators=[DataRequired("Le prix de pièce détaille en decimal")])
    prix_gros = DecimalField('Prix produit en gors', validators=[DataRequired("Le prix du produit gros en decimal")])
    emballage= SelectField('Emballage',choices=[('Box', 'Box'), ('Carton', 'Carton'), ('Sac', 'Sac'), ('Vrac', 'Vrac'), ('Sachet', 'Sachet')])
    nombre_contenu=IntegerField('Nombre de contenu')
    mesure_em=StringField('Contenu emballage', validators=[DataRequired("Completer nom"),  Length(min=4, max=60, 
                    message="Veuillez respecter la longeur de 2 à 60")])
    emballage_contenu=StringField('Contenu emballae', validators=[DataRequired("Completer nom"),  Length(min=4, max=60, 
                    message="Veuillez respecter la longeur de 2 à 60")])
    nombre_contenu_emballage=IntegerField('Nombre de contenu')
    mesure_em_con=StringField('Contenu emballage', validators=[DataRequired("Completer nom"),  Length(min=4, max=60, 
                    message="Veuillez respecter la longeur de 2 à 60")])
    avatar = FileField("Image",validators=[FileAllowed(['jpg','png'],'Seul jpg et png sont autorisés')])
    categorie= QuerySelectField(query_factory=rech_cate, get_label='nom_categorie', allow_blank=False)

    submit= SubmitField('Enregister')

