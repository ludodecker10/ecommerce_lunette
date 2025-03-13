#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''   SELECT categorie.id_categorie, categorie.libelle_categorie, COUNT(lunette.id_lunette) AS nbr_lunette
        FROM categorie
        LEFT JOIN lunette ON categorie.id_categorie = lunette.id_categorie
        GROUP BY categorie.id_categorie, categorie.libelle_categorie
        ORDER BY categorie.id_categorie    '''
    mycursor.execute(sql)
    categorie = mycursor.fetchall()

    return render_template('admin/type_article/show_type_article.html', categorie=categorie)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    libelle = request.form.get('libelle', '')
    mycursor = get_db().cursor()
    sql = '''    INSERT INTO categorie (libelle_categorie)
                VALUES (%s)'''
    mycursor.execute(sql, (libelle,))
    get_db().commit()
    message = u'type ajouté , libellé :'+libelle
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show') #url_for('show_type_article')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_categorie = request.args.get('id_categorie', '')
    mycursor = get_db().cursor()

    sql = '''DELETE FROM categorie
            WHERE id_categorie = %s'''
    mycursor.execute(sql, (id_categorie,))
    get_db().commit()

    flash(u'suppression type article , id : ' + id_categorie, 'alert-success')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_categorie = request.args.get('id_categorie', '')
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM categorie WHERE id_categorie = %s  '''
    mycursor.execute(sql, (id_categorie,))
    categorie = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', categorie=categorie)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle_categorie']
    id_categorie = request.form.get('id_categorie', '')
    mycursor = get_db().cursor()
    sql = '''  UPDATE categorie
                SET libelle_categorie = %s  
                WHERE id_categorie = %s'''
    tuple_update = (libelle, id_categorie)
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_categorie + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')








