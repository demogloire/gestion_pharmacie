import os
import secrets
from flask import render_template, flash, url_for, redirect, request, session
from flask_login import login_user, current_user, login_required
from PIL import Image
from .. import create_app
from .. import db
from functools import wraps

from ..models import Produit


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


#Autorisation des vendeur
# def autorisation_gerant(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if current_user.role =='Gérant':
#             return f(*args, **kwargs)
#         else:
#             return redirect(url_for('main.index'))       
#     return wrap

#Enregistrement du fichier pdf
def save_image(document):
    if document is None:
        return None
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(document.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/file', picture_fn)
    document.save(picture_path)
    return picture_fn

#Enregistrement du fichier 
def save_image_mod(form_picture, ancien):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    #Suppression de l'ancien fichier
    if ancien is not None:
        chemin_offre=os.path.join(app.root_path, 'static/publication', ancien)
        if os.path.exists(chemin_offre):
            os.remove(chemin_offre)
        else:
            pass
    #Enregitrement du nouveau fichier
    picture_path = os.path.join(app.root_path, 'static/publication', picture_fn)
    form_picture.save(picture_path)
    return picture_fn