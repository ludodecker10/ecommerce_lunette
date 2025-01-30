#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *

from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql = '''DROP TABLE IF EXISTS ligne_panier;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS ligne_commande;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS lunette;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS commande;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS categorie;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS couleur;'''
    mycursor.execute(sql)
    sql = '''DROP TABLE IF EXISTS etat;'''
    mycursor.execute(sql)
    sql = ''' DROP TABLE IF EXISTS utilisateur;'''
    mycursor.execute(sql)

    sql='''
    CREATE TABLE utilisateur(
       id_utilisateur INT AUTO_INCREMENT,
       login VARCHAR(50),
       email VARCHAR(50),
       nom VARCHAR(50),
       password VARCHAR(255),
       role VARCHAR(50),
       est_actif VARCHAR(255),
       PRIMARY KEY(id_utilisateur)
    );
    '''
    mycursor.execute(sql)
    sql='''
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
    (1,'admin','admin@admin.fr',
        'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
        'ROLE_admin','admin','1'),
    (2,'client','client@client.fr',
        'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
        'ROLE_client','client','1'),
    (3,'client2','client2@client2.fr',
        'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
        'ROLE_client','client2','1');
    '''
    mycursor.execute(sql)

    sql='''
    CREATE TABLE categorie(
       id_categorie INT,
       libelle_categorie VARCHAR(50),
       PRIMARY KEY(id_categorie)
    );
    '''
    mycursor.execute(sql)
    sql='''
    INSERT INTO type_article
    '''
    mycursor.execute(sql)


    sql='''
    CREATE TABLE etat(
       id_etat INT,
       libelle_etat VARCHAR(50),
       PRIMARY KEY(id_etat)
    );
    '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO etat
     '''
    mycursor.execute(sql)


    sql='''
    CREATE TABLE couleur(
       id_couleur INT,
       libelle_couleur TEXT,
       PRIMARY KEY(id_couleur)
    );
    '''
    mycursor.execute(sql)
    sql='''
    INSERT INTO couleur
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE lunette(
       id_lunette INT,
       nom_lunette VARCHAR(50),
       sexe VARCHAR(50),
       indice_protection INT,
       taille_monture VARCHAR(50),
       prix_lunette INT,
       fournisseur VARCHAR(50),
       marque VARCHAR(50),
       id_couleur INT NOT NULL,
       id_categorie INT NOT NULL,
       PRIMARY KEY(id_lunette),
       FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
       FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie)
    );
     '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO article (

         '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE commande(
       id_commande INT,
       date_achat DATE,
       id_etat INT NOT NULL,
       id_utilisateur INT NOT NULL,
       PRIMARY KEY(id_commande),
       FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
    ); 
     '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande(
       id_commande INT,
       id_lunette INT,
       prix INT,
       quantite INT,
       PRIMARY KEY(id_commande, id_lunette),
       FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
       FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette)
    );
         '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO ligne_commande 
         '''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE ligne_panier(
       id_utilisateur INT,
       id_lunette INT,
       quantite INT,
       date_ajout DATE,
       PRIMARY KEY(id_utilisateur, id_lunette),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
       FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette)
    );
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
