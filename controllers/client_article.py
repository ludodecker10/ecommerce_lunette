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


    filtrenomlunette = session['filter_word']

    sql = '''SELECT * 
            FROM lunette l
            JOIN declinaison_lunette dl ON l.id_lunette = dl.id_lunette
            JOIN couleur c ON c.id_couleur = dl.id_couleur
            WHERE nom_lunette like %s '''
    mycursor.execute(sql, '%'+filtrenomlunette+'%')
    lunette = mycursor.fetchall()


    # utilisation du filtre
    sql3='''SELECT * FROM categorie'''
    mycursor.execute(sql3)
    categorie = mycursor.fetchall()

    # pour le filtre


    slq = '''SELECT lp.id_declinaison_lunette, lp.quantite,
           dl.prix_declinaison AS prix,
          l.nom_lunette, c.libelle_couleur, lp.quantite*dl.prix_declinaison as sous_total
    FROM ligne_panier lp
     JOIN declinaison_lunette dl ON lp.id_declinaison_lunette = dl.id_declinaison_lunette
     JOIN lunette l ON dl.id_lunette = l.id_lunette
     JOIN couleur c ON dl.id_couleur = c.id_couleur
     WHERE lp.id_utilisateur = %s;'''
    mycursor.execute(slq, id_client)
    ligne_panier = mycursor.fetchall()

  #  if len(ligne_panier) >= 1:
  #      sql = ''' calcul du prix total du panier '''
  #      prix_total = None
  #  else:
  #      prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , lunette=lunette
                           , ligne_panier=ligne_panier
                           #, prix_total=prix_total
                           , categorie=categorie
                           )
