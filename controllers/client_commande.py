#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime


from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT lp.id_declinaison_lunette, lp.quantite,
           dl.prix_declinaison AS prix,
          l.nom_lunette, c.libelle_couleur, lp.quantite*dl.prix_declinaison as sous_total
    FROM ligne_panier lp
     JOIN declinaison_lunette dl ON lp.id_declinaison_lunette = dl.id_declinaison_lunette
     JOIN lunette l ON dl.id_lunette = l.id_lunette
     JOIN couleur c ON dl.id_couleur = c.id_couleur
     WHERE lp.id_utilisateur = %s;'''
    mycursor.execute(sql, id_client)

    ligne_panier = mycursor.fetchall()

    if len(ligne_panier) >= 1:
        sql = ''' SELECT sum(lp.quantite*dl.prix_declinaison) AS montantcommande
    FROM ligne_panier lp
     JOIN declinaison_lunette dl ON lp.id_declinaison_lunette = dl.id_declinaison_lunette
     WHERE lp.id_utilisateur = %s'''
        mycursor.execute(sql, (id_client,))
        ressql = mycursor.fetchone()

        prix_total = ressql['montantcommande']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    sql = '''SELECT * FROM adresse WHERE id_utilisateur = %s'''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , ligne_panier=ligne_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    id_adresse_livraison = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')
    sql = ''' SELECT *
            FROM ligne_panier lp
            JOIN declinaison_lunette dl ON lp.id_declinaison_lunette = dl.id_declinaison_lunette
            WHERE id_utilisateur = %s '''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
         return redirect('/client/article/show')
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/


    sql = ''' INSERT INTO commande (date_achat, etat_id, utilisateur_id, id_adresse_livraison, id_adresse_facturation)
            VALUES (current_date, %s, %s, %s, %s)'''
    mycursor.execute(sql,( 1, id_client, id_adresse_livraison, id_adresse_facturation,))


    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    reqsql = mycursor.fetchone()

    idcommande = reqsql['last_insert_id']



    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur = %s AND id_declinaison_lunette = %s'''
        mycursor.execute(sql, (id_client,item['id_declinaison_lunette'],))

        sql = ''' INSERT INTO ligne_commande (id_commande, id_declinaison_lunette, prix, quantite)
                VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql, (idcommande,item['id_declinaison_lunette'],item['prix_declinaison'],item['quantite']))


    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = ''' SELECT c.id_commande, c.date_achat,sum(lc.quantite) as nbr_articles, SUM(lc.prix* lc.quantite) AS prix, e.libelle_etat
            FROM commande c
            JOIN ligne_commande lc ON c.id_commande = lc.id_commande
            JOIN etat e ON c.etat_id = e.id_etat
            WHERE utilisateur_id = %s
            GROUP BY c.id_commande'''
    mycursor.execute(sql, (id_client,))
    commande = mycursor.fetchall()

    article_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        sql = ''' SELECT lc.id_declinaison_lunette, lc.prix, lc.quantite, l.nom_lunette, SUM(lc.prix* lc.quantite) AS prix_ligne
            FROM ligne_commande lc
            JOIN declinaison_lunette dl ON lc.id_declinaison_lunette = dl.id_declinaison_lunette
            JOIN lunette l ON dl.id_lunette = l.id_lunette
            WHERE lc.id_commande = %s
            GROUP BY lc.id_declinaison_lunette'''
        mycursor.execute(sql, (id_commande,))
        article_commande = mycursor.fetchall()

        sql = '''   SELECT a1.nom AS nom_livraison, a2.nom AS nom_facturation
                    FROM commande c
                    LEFT JOIN adresse a1 ON c.id_adresse_livraison = a1.id_adresse
                    LEFT JOIN adresse a2 ON c.id_adresse_facturation = a2.id_adresse
                    WHERE c.id_commande = %s
                    '''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchone()



    return render_template('client/commandes/show.html'
                           , commande=commande
                           , article_commande=article_commande
                           , commande_adresses=commande_adresses
                           )

