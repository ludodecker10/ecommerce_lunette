#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')

@client_panier.route('/client/article/show')
def afficher_panier():
    id_client = session.get('id_user')

    mycursor = get_db().cursor(dictionary=True)  # 🔹 Assure que les résultats sont des dictionnaires
    sql = """
    SELECT lp.id_declinaison_lunette, lp.quantite
  
    FROM ligne_panier lp

    """
    mycursor.execute(sql, (id_client,))
    ligne_panier = mycursor.fetchall()

    print(f"🔍 Contenu du panier récupéré : {ligne_panier}")  # Vérifier la sortie en console Flask

    return render_template('panier.html', ligne_panier=ligne_panier)

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    id_client = session.get('id_user')
    id_declinaison_lunette = request.form.get('id_declinaison_lunette')
    quantite = int(request.form.get('quantite', 1))

    if not id_client or not id_declinaison_lunette or quantite <= 0:
        return {"error": "Données invalides"}, 400

    mycursor = get_db().cursor()

    # Vérifier si la déclinaison existe et le stock disponible
    sql = "SELECT stock FROM declinaison_lunette WHERE id_declinaison_lunette = %s"
    mycursor.execute(sql, (id_declinaison_lunette,))
    declinaison_lunette = mycursor.fetchone()

    if not declinaison_lunette:
        return {"error": "Cette déclinaison de lunette n'existe pas"}, 400

    stock_disponible = declinaison_lunette['stock']

    # Vérifier si l'article est déjà dans le panier
    sql = """SELECT quantite FROM ligne_panier 
         WHERE id_declinaison_lunette = %s AND id_utilisateur = %s"""
    mycursor.execute(sql, (id_declinaison_lunette, id_client))
    article_panier = mycursor.fetchone()

    if article_panier:  # Mise à jour de la quantité si déjà présent
        nouvelle_quantite = article_panier['quantite'] + quantite
        if quantite > stock_disponible:
            return {"error": "Quantité demandée supérieure au stock disponible"}, 400

        sql = """UPDATE ligne_panier 
                 SET quantite = %s 
                 WHERE id_utilisateur = %s AND id_declinaison_lunette = %s"""
        mycursor.execute(sql, (nouvelle_quantite, id_client, id_declinaison_lunette))
    else:  # Ajout d'un nouvel article
        if quantite > stock_disponible:
            return {"error": "Quantité demandée supérieure au stock disponible"}, 400

        sql = """INSERT INTO ligne_panier(id_utilisateur, id_declinaison_lunette, quantite, date_ajout) 
                 VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"""
        mycursor.execute(sql, (id_client, id_declinaison_lunette, quantite))

    sql = ''' UPDATE declinaison_lunette SET stock = stock - %s WHERE id_declinaison_lunette = %s'''
    mycursor.execute(sql, (quantite, id_declinaison_lunette))

    get_db().commit()
    mycursor.close()
    print("✅ Article ajouté au panier avec succès")
    return redirect('/client/article/show')



@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_lunette = request.form.get('id_declinaison_lunette','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = ''' SELECT * FROM ligne_panier WHERE id_declinaison_lunette = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_declinaison_lunette,id_client))
    article_panier = mycursor.fetchone()

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = ''' UPDATE ligne_panier SET quantite = quantite-1 WHERE id_declinaison_lunette = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_declinaison_lunette, id_client))
    else:
        sql = '''  DELETE FROM ligne_panier WHERE id_declinaison_lunette = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (id_declinaison_lunette, id_client))

    # mise à jour du stock de l'article disponible

    sql = ''' UPDATE declinaison_lunette SET stock = stock+1 WHERE id_declinaison_lunette = %s '''
    mycursor.execute(sql, (id_declinaison_lunette))

    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT * FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = '''DELETE FROM ligne_panier WHERE id_declinaison_lunette = %s AND id_utilisateur = %s'''
        mycursor.execute(sql, (item['id_declinaison_lunette'], id_client))

        sql = ''' UPDATE declinaison_lunette SET stock = stock+%s WHERE id_declinaison_lunette = %s '''
        mycursor.execute(sql, (item['quantite'],item['id_declinaison_lunette']))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_lunette = request.form.get('id_declinaison_lunette')

    sql = '''SELECT quantite FROM ligne_panier WHERE id_declinaison_lunette = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_declinaison_lunette,id_client))
    quantite = mycursor.fetchone()

    sql = ''' DELETE FROM ligne_panier WHERE id_declinaison_lunette = %s AND id_utilisateur = %s '''
    mycursor.execute(sql, (id_declinaison_lunette, id_client))

    sql2=''' UPDATE declinaison_lunette SET stock = stock+%s WHERE id_declinaison_lunette = %s '''
    mycursor.execute(sql2, (quantite['quantite'], id_declinaison_lunette))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables

    session['filter_word']=filter_word

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session['filter_word'] = ''
    print("suppr filtre")
    return redirect('/client/article/show')
