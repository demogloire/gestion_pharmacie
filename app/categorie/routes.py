from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Categorie, Produit 
from app.categorie.forms import CategorieForm, CategorieEditerForm
#from app.categorie.autorisation  import autorisation_gerant
from flask_login import login_user, current_user, logout_user, login_required

from . import categorie

@categorie.route('/ajouter_categorie', methods=['GET','POST'])
#@login_required
#@autorisation_gerant
def ajouter_categorie():
    #Les catagories de livre
    title="Ajouter une catégorie"

    form=CategorieForm()

    if form.validate_on_submit():
        categorie_ajout=Categorie(nom_categorie=form.nom.data.capitalize())
        db.session.add(categorie_ajout)
        db.session.commit()
        flash('Ajout de la catégorie ({}) avec succès'.format(form.nom.data.capitalize()),'success')
        return redirect(url_for('categorie.index'))

    return render_template('categorie/ajouterc.html', title=title, form=form)



@categorie.route('/')
#@login_required
#@autorisation_gerant
def index():
    #Les catagories des articles
    title="Liste | Catégorie"
    #Requete de listage des catégories des articles
    list_cate=Categorie.query.all()

    return render_template('categorie/index.html', title=title, listes=list_cate)


@categorie.route('/<int:cat_id>/categorie', methods=['GET','POST'])
#@login_required
#@autorisation_gerant
def editer_categorie(cat_id):
    #formulaire
    form=CategorieEditerForm()
    #Verification de l'existence de la cetégorie
    cate_edit=Categorie.query.filter_by(id=cat_id).first_or_404()
    #Titre de la catégorie
    title=" {} | Modification "+cate_edit.nom_categorie
    #Verification des informations de l'ID
    if cate_edit is None:
        flash("Veuillez respecté la procedure",'danger')
        return redirect(url_for('categorie.index'))
    #Validation d'enregistrement
    if form.validate_on_submit():
        cate_edit.nom_categorie=form.nom.data.capitalize()
        db.session.commit()
        flash("Modification avec succès",'success')
        return redirect(url_for('categorie.index'))
    elif request.method =='GET':
        form.nom.data=cate_edit.nom_categorie

    return render_template('categorie/mod_cat.html', title=title, form=form)


@categorie.route('/<int:cat_id>/statut', methods=['GET','POST'])
#@login_required
#@autorisation_gerant
def statut_categorie(cat_id):
    #Verification de l'existence de la cetégorie
    cate_statut=Categorie.query.filter_by(id=cat_id).first_or_404()
    if cate_statut.statut is True:
        cate_statut.statut=False
        db.session.commit()
        flash('Catégorie desactivée', 'success')
        return redirect(url_for('categorie.index'))
    else:
        cate_statut.statut=True
        db.session.commit()
        flash('Catégorie activée', 'success')
        return redirect(url_for('categorie.index'))
        
    return render_template('categorie/mod_cat.html', title=title, form=form)





@categorie.route('/<int:cat_id>/association', methods=['GET','POST'])
#@login_required
#@autorisation_gerant
def association_categorie(cat_id):
    #Verification de l'existence de la cetégorie
    cate_association=Categorie.query.filter_by(id=cat_id).first_or_404()
    #Titre de la catégorie
    title=" {} | Association ".format(cate_association.nom_categorie)
    #Verification des informations de l'ID
    if cate_association is None:
        flash("Veuillez respecté la procedure",'danger')
        return redirect(url_for('categorie.index'))
    #Vérification des produit associé à la catégorie.
    produits=Produit.query.filter_by(categorie_id=cat_id).all()
    #Nom de la catégorie de l'association.
    nom_categorie_association=cate_association.nom_categorie
    
    return render_template('categorie/asso.html', nom_categorie_association=nom_categorie_association, title=title, produits=produits)


    