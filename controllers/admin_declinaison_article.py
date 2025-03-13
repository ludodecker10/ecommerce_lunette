#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_lunette=request.args.get('id_lunette')
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM lunette WHERE id_lunette=%s '''
    mycursor.execute(sql, (id_lunette,))
    lunette=mycursor.fetchone()

    sql = ''' SELECT * FROM couleur '''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()

    d_couleur_uniq=None
    return render_template('admin/article/add_declinaison_article.html'
                           , lunette=lunette
                           , couleurs=couleurs
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()

    id_lunette = request.form.get('id_lunette')
    stock = request.form.get('stock')
    prix_declinaison = request.form.get('prix_declinaison')
    id_couleur = request.form.get('id_couleur')
    # attention au doublon
    sql = ''' SELECT id_couleur FROM declinaison_lunette WHERE id_lunette=%s '''
    mycursor.execute(sql, (id_lunette,))
    lunette=mycursor.fetchall()
    for i in range(len(lunette)):
        if int(id_couleur) == lunette[i]['id_couleur']:
            flash(u'le déclinaison existe déjà ', 'alert-success')
            return redirect('/admin/article/edit?id_lunette=' + str(id_lunette))

    sql = ''' INSERT INTO declinaison_lunette (stock, prix_declinaison, id_lunette, id_couleur)
                VALUES (%s, %s, %s, %s)'''
    mycursor.execute(sql, (stock,prix_declinaison,id_lunette,id_couleur))

    get_db().commit()
    return redirect('/admin/article/edit?id_lunette=' + str(id_lunette))


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison_lunette = request.args.get('id_declinaison_lunette')
    mycursor = get_db().cursor()

    sql = ''' SELECT l.nom_lunette, l.image, dl.id_declinaison_lunette, dl.stock, dl.id_couleur, l.id_lunette
            FROM declinaison_lunette dl
            JOIN lunette l ON l.id_lunette = dl.id_lunette
            WHERE id_declinaison_lunette = %s '''
    mycursor.execute(sql, id_declinaison_lunette)
    declinaison_lunette=mycursor.fetchone()

    sql = ''' SELECT * FROM couleur '''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()
    d_couleur_uniq=None
    return render_template('admin/article/edit_declinaison_article.html'
                           , couleurs=couleurs
                           , declinaison_lunette=declinaison_lunette
                           , d_couleur_uniq=d_couleur_uniq
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_lunette = request.form.get('id_declinaison_lunette','')
    id_lunette = request.form.get('id_lunette','')
    stock = request.form.get('stock','')
    id_couleur = request.form.get('id_couleur','')
    mycursor = get_db().cursor()

    sql = ''' SELECT id_couleur FROM declinaison_lunette WHERE id_lunette=%s '''
    mycursor.execute(sql, (id_lunette,))
    lunette=mycursor.fetchall()

    for i in range (len(lunette)):
        if int(id_couleur) == lunette[i]['id_couleur']:
            flash(u'le déclinaison existe déjà ', 'alert-success')
            return redirect('/admin/article/edit?id_lunette=' + str(id_lunette))

    sql = ''' UPDATE declinaison_lunette SET stock = %s , id_couleur = %s WHERE id_declinaison_lunette = %s '''
    mycursor.execute(sql, (stock, id_couleur, id_declinaison_lunette))
    get_db().commit()

    message = u'declinaison_article modifié , id:' + str(id_declinaison_lunette) + '- stock :' + str(stock) + ' - couleur_id:' + str(id_couleur)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?id_lunette=' + str(id_lunette))


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_lunette = request.args.get('id_declinaison_lunette','')
    id_lunette = request.args.get('id_lunette','')
    mycursor = get_db().cursor()

    sql = ''' DELETE FROM declinaison_lunette WHERE id_declinaison_lunette = %s '''
    mycursor.execute(sql, id_declinaison_lunette)
    get_db().commit()

    flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_lunette),  'alert-success')
    return redirect('/admin/article/edit?id_lunette=' + str(id_lunette))
