#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''SELECT l.*, SUM(dl.stock) AS stock, COUNT(dl.id_declinaison_lunette) AS nb_declinaisons
    FROM lunette l
    JOIN declinaison_lunette dl ON l.id_lunette = dl.id_lunette
    GROUP BY l.id_lunette
    '''
    mycursor.execute(sql)
    lunette = mycursor.fetchall()
    return render_template('admin/article/show_article.html', lunette=lunette)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    sql_categories = '''SELECT * FROM categorie'''
    mycursor.execute(sql_categories)
    categorie = mycursor.fetchall()

    # Récupérer les couleurs disponibles
    sql_couleurs = '''SELECT * FROM couleur'''
    mycursor.execute(sql_couleurs)
    couleur = mycursor.fetchall()

    return render_template('admin/article/add_article.html'
                           , categorie=categorie, couleur=couleur
                            )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    stock = request.form.get('stock', '')
    indice_protection = request.form.get('indice_protection', '')
    prix = request.form.get('prix', '')
    marque = request.form.get('marque', '')
    image = request.files.get('image', '')
    description = request.form.get('description', '')
    id_categorie = request.form.get('id_categorie', '')
    image = request.files.get('image', '')

    filename = None
    if image:
        filename = 'img_upload'+ str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', secure_filename(filename)))


    sql = '''INSERT INTO lunette (nom_lunette, stock, indice_protection, prix_lunette, marque, image,description, id_categorie)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

    tuple_add = (nom, stock, indice_protection, prix, marque, filename, description, id_categorie)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', id_categorie, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + id_categorie + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_lunette = request.args.get('id_lunette')
    mycursor = get_db().cursor()

    sql = ''' SELECT COUNT(*) AS nb_declinaison FROM declinaison_lunette WHERE id_lunette = %s '''
    mycursor.execute(sql, id_lunette)
    nb_declinaison = mycursor.fetchone()

    if nb_declinaison['nb_declinaison'] > 0:
        message= u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' SELECT image FROM lunette WHERE id_lunette = %s '''
        mycursor.execute(sql, id_lunette)
        lunette = mycursor.fetchone()
        image = lunette['image']

        sql = ''' DELETE FROM lunette WHERE id_lunette = %s  '''
        mycursor.execute(sql, id_lunette)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_lunette)
        message = u'un article supprimé, id : ' + id_lunette
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_lunette = request.args.get('id_lunette')
    mycursor = get_db().cursor()
    sql = '''
    SELECT l.*, SUM(dl.stock) AS stock
    FROM lunette l
    JOIN declinaison_lunette dl ON l.id_lunette = dl.id_lunette
    WHERE l.id_lunette = %s
    GROUP BY l.id_lunette
    '''
    mycursor.execute(sql, id_lunette)
    lunette = mycursor.fetchone()
    print(lunette)

    sql = '''
    SELECT * FROM categorie
    '''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()

    sql = ''' SELECT * 
            FROM declinaison_lunette dl
            JOIN couleur c ON c.id_couleur = dl.id_couleur
            WHERE id_lunette = %s '''
    mycursor.execute(sql, id_lunette)
    declinaisons_lunette = mycursor.fetchall()


    return render_template('admin/article/edit_article.html'
                           ,lunette=lunette
                           ,categorie=categorie
                           ,declinaisons_lunette=declinaisons_lunette
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id_lunette = request.form.get('id_lunette', '')
    nom_lunette = request.form.get('nom', '')
    id_categorie = request.form.get('id_categorie', '')
    prix_lunette = request.form.get('prix', '')
    marque = request.form.get('marque', '')
    indice_protection = request.form.get('indice_protection', '')
    stock = request.form.get('stock', '')
    description = request.form.get('description', '')
    image = request.files.get('image')

    sql = '''SELECT image FROM lunette WHERE id_lunette = %s'''
    mycursor.execute(sql, (id_lunette,))
    lunette = mycursor.fetchone()
    image_nom = lunette['image'] if lunette else None

    if image and image.filename != '':
        if image_nom:
            filepath = os.path.join('static/images/', image_nom)
            if os.path.exists(filepath):
                os.remove(filepath)

        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        filepath = os.path.join('static/images/', secure_filename(filename))
        image.save(filepath)
        image_nom = filename

    sql = '''UPDATE lunette 
                 SET nom_lunette = %s, indice_protection = %s, prix_lunette = %s, 
                     marque = %s, image = %s, description = %s, id_categorie = %s
                 WHERE id_lunette = %s'''
    mycursor.execute(sql, (nom_lunette, indice_protection, prix_lunette, marque, image_nom, description, id_categorie, id_lunette))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = f"Lunette '{nom_lunette}' modifiée avec succès"
    flash(message, 'alert-success')
    return redirect('/admin/article/show')







@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article=[]
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
