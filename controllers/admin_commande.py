#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = ''' SELECT u.login, c.id_commande, c.date_achat, sum(lc.quantite) AS nbr_articles, e.libelle_etat, c.etat_id,  SUM(lc.prix* lc.quantite) AS prix_total
                FROM commande c
                JOIN utilisateur u ON u.id_utilisateur = c.utilisateur_id
                JOIN ligne_commande lc ON lc.id_commande = c.id_commande
                JOIN etat e ON e.id_etat = c.etat_id
                GROUP BY c.id_commande '''
    mycursor.execute(sql)
    commandes=mycursor.fetchall()

    article_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = '''  SELECT lc.id_declinaison_lunette, lc.prix, lc.quantite, l.nom_lunette, SUM(lc.prix* lc.quantite) AS prix_ligne, c.etat_id
            FROM ligne_commande lc
            JOIN declinaison_lunette dl ON lc.id_declinaison_lunette = dl.id_declinaison_lunette
            JOIN lunette l ON dl.id_lunette = l.id_lunette
            JOIN commande c ON c.id_commande = lc.id_commande
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
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , article_commande=article_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id =  etat_id + 1 WHERE id_commande = %s'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
