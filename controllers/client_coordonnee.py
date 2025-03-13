#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql_utilisateur = '''SELECT * FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql_utilisateur, (id_client,))
    utilisateur = mycursor.fetchone()

    # Récupérer les adresses associées à l'utilisateur
    sql_adresses = '''SELECT a.*, 
                                 (SELECT COUNT(*) FROM commande WHERE id_adresse_livraison = a.id_adresse) AS nbr_commandes
                          FROM adresse a 
                          WHERE id_utilisateur = %s'''
    mycursor.execute(sql_adresses, (id_client,))
    adresse = mycursor.fetchall()

    mycursor.close()

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresse=adresse
                         #  , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    mycursor.close()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql_check = '''SELECT * FROM utilisateur WHERE (email = %s OR login = %s) AND id_utilisateur != %s'''
    mycursor.execute(sql_check, (email, login, id_client))
    utilisateur_existant = mycursor.fetchone()

    if utilisateur_existant:
        flash(u"Cet Email ou ce Login existe déjà pour un autre utilisateur", "alert-warning")
        return render_template("client/coordonnee/edit_coordonnee.html",
                               utilisateur={"nom": nom, "login": login, "email": email})

    # Mise à jour des informations

    sql_update = '''UPDATE utilisateur SET nom = %s, login = %s, email = %s WHERE id_utilisateur = %s'''
    mycursor.execute(sql_update, (nom, login, email, id_client))

    get_db().commit()
    mycursor.close()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')
    print(id_adresse, '1')

    sql_delete = '''DELETE FROM adresse WHERE id_adresse = %s AND id_utilisateur = %s'''
    mycursor.execute(sql_delete, (id_adresse, id_client))

    get_db().commit()
    mycursor.close()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = "SELECT * FROM utilisateur WHERE id_utilisateur = %s"
    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()  # 🔹 Récupérer une seule ligne

    mycursor.close()
    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()

    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_client = session['id_user']

    sql = '''INSERT INTO adresse (nom, rue, code_postal, ville, date_utilisation, id_utilisateur)
    VALUES (%s, %s, %s, %s, current_date, %s)'''

    mycursor.execute(sql, (nom, rue, code_postal, ville, id_client))
    get_db().commit()
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT * FROM utilisateur WHERE id_utilisateur = %s'''

    mycursor.execute(sql, (id_client,))
    utilisateur = mycursor.fetchone()

    sql_adresse = '''SELECT * FROM adresse WHERE id_utilisateur = %s'''
    mycursor.execute(sql_adresse, (id_client,))
    adresse = mycursor.fetchone()

    mycursor.close()

    return render_template('/client/coordonnee/edit_adresse.html'
                            ,utilisateur=utilisateur
                            ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    # Récupération des données du formulaire
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql_update = '''UPDATE adresse 
                        SET nom = %s, rue = %s, code_postal = %s, ville = %s 
                        WHERE id_adresse = %s AND id_utilisateur = %s'''
    mycursor.execute(sql_update, (nom, rue, code_postal, ville, id_adresse, id_client))

    get_db().commit()
    mycursor.close()

    return redirect('/client/coordonnee/show')
