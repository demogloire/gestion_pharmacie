from flask import render_template, flash, url_for, redirect, request
from .. import db
from ..models import Categorie, Produit 
from app.produit.forms import ProduitAForm
from app.produit.autorisation  import save_image
from flask_login import login_user, current_user, logout_user, login_required

from . import produit

@produit.route('/ajouter_produit', methods=['GET','POST'])
#@login_required
#@autorisation_gerant
def ajouter_produit():
    #Les catagories de livre
    title="Ajouter une catégorie"

    form=ProduitAForm()

    if form.validate_on_submit():
        prix_d_achat=form.cout_achat.data
        prix_de_vente_detail=form.prix_detaille.data
        pix_de_vente_gros=form.prix_gros.data
        emballage=form.emballage.data
        
        #Vérification des prix
        if prix_d_achat > 0 or prix_de_vente_detail > 0 or pix_de_vente_gros > 0:
            if prix_d_achat > prix_de_vente_detail or prix_d_achat > pix_de_vente_gros:
                flash("Est une vente à perte","danger") 
            elif pix_de_vente_gros > prix_de_vente_detail:
                flash("Le prix grossite est supérieur au prix detaille","danger")
            elif emballage =='Vrac':
                if form.nombre_contenu.data>1 or form.nombre_contenu_emballage.data >1:
                    flash("Le contenu à Vrac est égal à 1")
        else:
            flash("Le prix doit-être superieur à 0")
        #Vérification des contenues des emballages
        if form.nombre_contenu.data<1 or form.nombre_contenu_emballage.data <1:
            flash(" Le nombre de contenu doit être superieur à 0")
        else:
            pro=None
            if form.avatar.data is not None:
                image=save_image(form.avatar.data)
                pro=Produit(nom_produit=form.nom_produit.data.capitalize(),
                            description=form.description.data,cout_achat=form.cout_achat.data,
                            prix_detaille=form.prix_detaille.data,prix_gros=form.prix_gros.data,
                            emballage=form.emballage.data,nombre_contenu=1, mesure_em=form.mesure_em.data, emballage_contenu=form.emballage_contenu.data,
                            nombre_contenu_emballage=form.nombre_contenu_emballage.data,
                            mesure=form.mesure_em_con.data,avatar=image,categorie_id=form.categorie.data.id)
            else:
                pro=Produit(nom_produit=form.nom_produit.data.capitalize(),
                            description=form.description.data,cout_achat=form.cout_achat.data,
                            prix_detaille=form.prix_detaille.data,prix_gros=form.prix_gros.data,
                            emballage=form.emballage.data,nombre_contenu=1, mesure_em=form.mesure_em.data, emballage_contenu=form.emballage_contenu.data,
                            nombre_contenu_emballage=form.nombre_contenu_emballage.data,
                            mesure=form.mesure_em_con.data,categorie_id=form.categorie.data.id)
                
            db.session.add(pro)
            db.session.commit()
            flash('Vous avez ajouter un produit', 'success')

    return render_template('produit/ajouter.html', title=title, form=form)



# @categorie.route('/')
# #@login_required
# #@autorisation_gerant
# def index():
#     #Les catagories des articles
#     title="Liste | Catégorie"
#     #Requete de listage des catégories des articles
#     list_cate=Categorie.query.all()

#     return render_template('categorie/index.html', title=title, listes=list_cate)


# @categorie.route('/<int:cat_id>/categorie', methods=['GET','POST'])
# #@login_required
# #@autorisation_gerant
# def editer_categorie(cat_id):
#     #formulaire
#     form=CategorieEditerForm()
#     #Verification de l'existence de la cetégorie
#     cate_edit=Categorie.query.filter_by(id=cat_id).first_or_404()
#     #Titre de la catégorie
#     title=" {} | Modification "+cate_edit.nom_categorie
#     #Verification des informations de l'ID
#     if cate_edit is None:
#         flash("Veuillez respecté la procedure",'danger')
#         return redirect(url_for('categorie.index'))
#     #Validation d'enregistrement
#     if form.validate_on_submit():
#         cate_edit.nom_categorie=form.nom.data.capitalize()
#         db.session.commit()
#         flash("Modification avec succès",'success')
#         return redirect(url_for('categorie.index'))
#     elif request.method =='GET':
#         form.nom.data=cate_edit.nom_categorie

#     return render_template('categorie/mod_cat.html', title=title, form=form)


# @categorie.route('/<int:cat_id>/statut', methods=['GET','POST'])
# #@login_required
# #@autorisation_gerant
# def statut_categorie(cat_id):
#     #Verification de l'existence de la cetégorie
#     cate_statut=Categorie.query.filter_by(id=cat_id).first_or_404()
#     if cate_statut.statut is True:
#         cate_statut.statut=False
#         db.session.commit()
#         flash('Catégorie desactivée', 'success')
#         return redirect(url_for('categorie.index'))
#     else:
#         cate_statut.statut=True
#         db.session.commit()
#         flash('Catégorie activée', 'success')
#         return redirect(url_for('categorie.index'))
        
#     return render_template('categorie/mod_cat.html', title=title, form=form)





# @categorie.route('/<int:cat_id>/association', methods=['GET','POST'])
# #@login_required
# #@autorisation_gerant
# def association_categorie(cat_id):
#     #Verification de l'existence de la cetégorie
#     cate_association=Categorie.query.filter_by(id=cat_id).first_or_404()
#     #Titre de la catégorie
#     title=" {} | Association ".format(cate_association.nom_categorie)
#     #Verification des informations de l'ID
#     if cate_association is None:
#         flash("Veuillez respecté la procedure",'danger')
#         return redirect(url_for('categorie.index'))
#     #Vérification des produit associé à la catégorie.
#     produits=Produit.query.filter_by(categorie_id=cat_id).all()
#     #Nom de la catégorie de l'association.
#     nom_categorie_association=cate_association.nom_categorie
    
#     return render_template('categorie/asso.html', nom_categorie_association=nom_categorie_association, title=title, produits=produits)


    