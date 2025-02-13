DROP TABLE IF EXISTS article_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS lunette;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;



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

CREATE TABLE etat(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
);

CREATE TABLE categorie(
   id_categorie INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie)
);

CREATE TABLE commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE lunette(
    id_lunette INT AUTO_INCREMENT,
    nom_lunette VARCHAR(50),
    sexe VARCHAR(50),
    indice_protection INT,
    longueur_branches INT,
    largeur_verres INT,
    largeur_pont INT,
    prix_lunette DECIMAL(10,2),
    marque VARCHAR(50),
    stock INT,
    image VARCHAR(255),
    id_couleur INT NOT NULL,
    id_categorie INT NOT NULL,
    PRIMARY KEY(id_lunette),
    FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
    FOREIGN KEY(id_categorie) REFERENCES categorie(id_categorie)
);

CREATE TABLE ligne_commande(
   id_commande INT,
   id_lunette INT,
   prix DECIMAL(10,2),
   quantite INT,
   PRIMARY KEY(id_commande, id_lunette),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette)
);

CREATE TABLE ligne_panier(
   id_utilisateur INT,
   id_lunette INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_utilisateur, id_lunette),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_lunette) REFERENCES lunette(id_lunette)
);

CREATE TABLE article_commande(
    id_lunette INT,
    id_commande INT,
    PRIMARY KEY (id_lunette,id_commande),
    FOREIGN KEY (id_lunette) REFERENCES lunette(id_lunette),
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE couleur_dispo(
    id_lunette INT,
    id_couleur INT,
    FOREIGN KEY (id_lunette) REFERENCES lunette(id_lunette),
    FOREIGN KEY (id_couleur) REFERENCES couleur(id_couleur)
);


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

INSERT INTO etat(id_etat, libelle_etat) VALUES
                                             (1,'Stockée'),
                                             (2,'Envoyée'),
                                             (3,'Livrée');

INSERT INTO couleur(id_couleur, libelle_couleur) VALUES
                                                     (1,'noir'),
                                                     (2,'bleu'),
                                                     (3,'rouge'),
                                                     (4,'blanc'),
                                                     (5,'rose');

INSERT INTO  categorie(id_categorie, libelle_categorie) VALUES
            (1,'Soleil'),
            (2,'Protection'),
            (3,'Vue');

INSERT INTO commande(id_commande, date_achat, id_etat, id_utilisateur) VALUES
            (1,'2024-08-24',1,1),
            (2,'2025-01-13',2,2);

INSERT INTO lunette(id_lunette, nom_lunette, sexe, indice_protection, longueur_branches,largeur_verres,largeur_pont, prix_lunette, marque, stock, image, id_couleur, id_categorie) VALUES
            (1,'Hedley','homme',NULL,145,53,18,74.99,'SmartBuy Collection',5,'lunette1',4,3),
            (2,'L6024S 662','homme',3,145,52,22,120.99,'Lacoste',2,'lunette2',5,1),
            (3,'Murf','femme',NULL,148,53,19,54.99,'SmartBuy Collection',3,'lunette3',1,3),
            (4,'RB2140 Original Wayfarer 901','homme',2,150,50,22,138.99,'Ray-Ban',6,'lunette4',1,1);

INSERT INTO article_commande(id_lunette, id_commande) VALUES
            (1,1),
            (3,1),
            (2,2),
            (4,2),
            (1,2);

INSERT iNTO couleur_dispo(id_lunette, id_couleur) VALUES
    (1,2),
    (1,3),
    (2,2),
    (2,1),
    (3,4),
    (3,1);