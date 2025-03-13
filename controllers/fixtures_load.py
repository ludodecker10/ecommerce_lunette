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
    sql = '''DROP TABLE IF EXISTS declinaison_lunette;'''
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
    sql = '''DROP TABLE IF EXISTS adresse;'''
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
        est_actif TINYINT(1),
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

    sql = '''CREATE TABLE adresse(
    id_adresse INT AUTO_INCREMENT,
    nom VARCHAR(50),
    rue VARCHAR(50),
    code_postal INT,
    ville VARCHAR(50),
    date_utilisation DATE,
    id_utilisateur INT,
    PRIMARY KEY (id_adresse),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);'''
    mycursor.execute(sql)

    sql = ''' INSERT INTO adresse(id_adresse, nom, rue, code_postal, ville, date_utilisation,id_utilisateur) VALUES
                (1,'client', 'rue diago', 90000, 'Belfort', '2024-04-24',2),
                (2,'client', 'rue loin', 22000, 'Saint-Brieuc', '2024-12-12',2),
                (3,'client2', 'avenue maréchal', 25000, 'Besançon', '2025-01-03',3),
                (4,'client2', 'rue du tournant',59000 , 'Lille', '2024-11-28', 3)'''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE etat(
           id_etat INT AUTO_INCREMENT,
           libelle_etat VARCHAR(50),
           PRIMARY KEY(id_etat)
        );
        '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO etat(id_etat, libelle_etat) VALUES
                                                 (1,'Stockée'),
                                                 (2,'Envoyée'),
                                                 (3,'Livrée');
         '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE couleur(
           id_couleur INT AUTO_INCREMENT,
           libelle_couleur VARCHAR(50),
           PRIMARY KEY(id_couleur)
        );
        '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO couleur(id_couleur, libelle_couleur) VALUES
                                                         (1,'noir'),
                                                         (2,'bleu'),
                                                         (3,'rouge'),
                                                         (4,'blanc'),
                                                         (5,'rose'),
                                                         (6,'dorée');
        '''
    mycursor.execute(sql)

    sql='''
    CREATE TABLE categorie(
       id_categorie INT AUTO_INCREMENT,
       libelle_categorie VARCHAR(50),
       PRIMARY KEY(id_categorie)
    );
    '''
    mycursor.execute(sql)
    sql='''
    INSERT INTO  categorie(id_categorie, libelle_categorie) VALUES
                                                             (1,'Soleil'),
                                                             (2,'Protection'),
                                                             (3,'Vue');
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE commande(
       id_commande INT AUTO_INCREMENT,
       date_achat DATE,
       etat_id INT,
       utilisateur_id INT,
        id_adresse_livraison INT,
        id_adresse_facturation INT,
       PRIMARY KEY(id_commande),
       FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
       FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (id_adresse_facturation) REFERENCES adresse(id_adresse),
        FOREIGN KEY (id_adresse_livraison) REFERENCES adresse(id_adresse)
    );
         '''
    mycursor.execute(sql)
    sql = '''
        INSERT INTO commande(id_commande, date_achat, etat_id, utilisateur_id, id_adresse_livraison, id_adresse_facturation) VALUES
                (1,'2024-08-24',1,1,1,1),
                (2,'2025-01-13',2,2,3,3),
                (3, '2025-03-10',1,2,4,4),
                (4, '2024-12-25',2,1,2,2),
                (5, '2025-02-28',3,2,3,4),
                (6, '2025-01-29',1,1,1,2),
                (7,'2024-10-19',2,1,2,1),
                (8, '2025-02-21',1,2,4,3),
                (9,'2025-03-08',1,2,1,1),
                (10,'2025-03-09',1,2,1,1),
                (11,'2025-03-09',1,2,1,1);
                     '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE lunette(
    id_lunette INT AUTO_INCREMENT,
    nom_lunette VARCHAR(100),
    indice_protection INT,
    prix_lunette DECIMAL(10,2),
    marque VARCHAR(50),
    image VARCHAR(255),
    description VARCHAR(255),
    id_categorie INT,
    PRIMARY KEY(id_lunette),
    FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie)
);
     '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO lunette(id_lunette, nom_lunette, indice_protection, prix_lunette, marque, image, id_categorie) VALUES
            (1,'Hedley',0, 74.99,'SmartBuy Collection','lunette1.png',3),
            (2,'L6024S 662',3,120.99,'Lacoste','lunette2.png',1),
            (3,'Murf',0,54.99,'SmartBuy Collection','lunette3.png',3),
            (4,'RB2140 Original Wayfarer 901',2,138.99,'Ray-Ban','lunette4.png',1),
            (5,'Nike 7170 425',0,135.00, 'Nike',  'lunette5.png', 3 ),
            (6, 'Anna-Karin Karlsson CLAW OPTICAL OCTAGONAL - DIAMOND Gold Diamond', 0, 6227.00, 'Anna-Karin Karlsson', 'lunette6.png', 3),
            (7, 'Police VK129 BEYOND JR 2 2GHM', 0, 60.00, 'Police', 'lunette7.png',3),
            (8, 'Ray Ban Kids Ray-Ban Kids RJ9069S 100/71',3, 73.00, 'Ray-Ban Kids', 'lunette8.png', 1),
            (9, 'Montana Eyewear MS47 MS47',1, 13.00, 'Montana Eyewear', 'lunette9.png', 1),
            (10, ' Prada PR 17ZV 15J1O1',0, 189.00, 'Prada', 'lunette10.png', 3 ),
            (11, 'SmartBuy Collection Halia 3362 C2',0, 32.00, 'SmartBuy Collection', 'lunette11.png', 3 ),
            (12, 'Tom Ford FT5958-B Blue-Light Block 001',0, 283.00, 'Tom Ford', 'lunette12.png', 3),
            (13, 'Celine CL41390/F Clara Asian Fit BMP',0, 108.00, 'Celine', 'lunette13.png', 3 ),
            (14, 'BOSS Boss 1479/F Asian Fit PJP',0, 105.00, 'BOSS', 'lunette14.png', 3),
            (15, 'Oakley OX8076 CROSSLINK ZERO 807603',0, 104.00, 'Oakley', 'lunette15.png', 3);
'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE declinaison_lunette(
    id_declinaison_lunette INT AUTO_INCREMENT,
    stock INT,
    prix_declinaison DECIMAL(10,2),
    image VARCHAR(50),
    id_lunette INT,
    id_couleur INT,
    PRIMARY KEY (id_declinaison_lunette),
    FOREIGN KEY (id_lunette) REFERENCES lunette(id_lunette),
    FOREIGN KEY (id_couleur) REFERENCES couleur(id_couleur)
);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO declinaison_lunette(id_declinaison_lunette, stock, prix_declinaison, image, id_lunette, id_couleur) VALUES
            (1,10,74.99,'image1',1,1),
            (2,10,80.00,'image1.1',1,2),
            (3,10,120.99,'image2',2,1),
            (4,10,130.00,'image2.1',2,2),
            (5,10,54.99,'image3',3,1),
            (6,10,60.00,'image3.1',3,2),
            (7,10,138.99,'image4',4,1),
            (8,10,150.00,'image4.1',4,2),
            (9,10,135.00,'image5',5,1),
            (10,10,145.00,'image5.1',5,2),
            (11,10,6227.00,'image6',6,6),
            (12,10,7000.00,'image6.1',6,2),
            (13,10,60.00,'image7',7,1),
            (14,10,70.00,'image7.1',7,2),
            (15,10,73.00,'image8',8,1),
            (16,10,74.99,'image8.1',8,2),
            (17,10,13.00,'image9.0',9,2),
            (18,10,15.00,'image9.1',9,1),
            (19,10,189.00,'image10',10,2),
            (20,10,199.99,'image10.1',10,1),
            (21,10,32.00,'image11',11,2),
            (22,10,39.99,'image11.1',11,1),
            (23,10,183.00,'image12',12,2),
            (24,10,190.00,'image12.1',12,1),
            (25,10,109.00,'image13',13,2),
            (26,10,100.00,'image13.1',13,6),
            (27,10,105.00,'image14',14,2),
            (29,10,125.00,'image14.1',14,1),
            (30,10,104.00,'image15',15,1),
            (31,10,130.00,'image15.1',15,2)
'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_commande(
       id_commande INT,
       id_declinaison_lunette INT,
       prix DECIMAL(10,2),
       quantite INT,
       PRIMARY KEY(id_commande, id_declinaison_lunette),
       FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
       FOREIGN KEY(id_declinaison_lunette) REFERENCES declinaison_lunette(id_declinaison_lunette)
    );
         '''
    mycursor.execute(sql)

    sql = ''' INSERT INTO ligne_commande (id_commande, id_declinaison_lunette, prix, quantite) VALUES
                (1,5,59.99,3),
                (2,7,138.99,1),
                (3,10,145.00,2),
                (4,11,6227.00,1),
                (4,12,7000.00,1),
                (5,14,70.00,3),
                (5,13,60.00,2),
                (6,18,145.00,4),
                (7,1,74.99,5),
                (7,3,120.99,1),
                (8,8,150.00,8),
                (8,4,130.00,1),
                (9,12,7000.0,1),
                (10,2,80.00,4),
                (10,5,54.99,1),
                (11,8,150.00,4),
                (11,10,145.00,4)'''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE ligne_panier(
       id_utilisateur INT,
       id_declinaison_lunette INT,
       quantite INT,
       date_ajout DATE,
       PRIMARY KEY(id_utilisateur, id_declinaison_lunette),
       FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
       FOREIGN KEY(id_declinaison_lunette) REFERENCES declinaison_lunette(id_declinaison_lunette)
    );

         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
