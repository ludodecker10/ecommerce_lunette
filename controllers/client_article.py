#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT * FROM lunette'''
    mycursor.execute(sql)

    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3='''SELECT * FROM categorie'''

    lunette = mycursor.fetchall()


    # pour le filtre
    categorie = mycursor.fetchall()


    ligne_panier = mycursor.fetchall()

    if len(ligne_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , lunette=lunette
                           , ligne_panier=ligne_panier
                           #, prix_total=prix_total
                           , categorie=categorie
                           )
