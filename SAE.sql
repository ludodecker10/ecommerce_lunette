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
   etat_id INT NOT NULL,
   utilisateur_id INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(etat_id) REFERENCES etat(id_etat),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE lunette(
    id_lunette INT AUTO_INCREMENT,
    nom_lunette VARCHAR(100),
    genre VARCHAR(50),
    indice_protection INT,
    longueur_branches INT,
    largeur_verres INT,
    largeur_pont INT,
    prix_lunette DECIMAL(10,2),
    marque VARCHAR(50),
    stock INT,
    image VARCHAR(255),
    couleur_id INT NOT NULL,
    categorie_id INT NOT NULL,
    PRIMARY KEY(id_lunette),
    FOREIGN KEY(couleur_id) REFERENCES couleur(id_couleur),
    FOREIGN KEY(categorie_id) REFERENCES categorie(id_categorie)
);

CREATE TABLE ligne_commande(
   commande_id INT,
   lunette_id INT,
   prix DECIMAL(10,2),
   quantite INT,
   PRIMARY KEY(commande_id, lunette_id),
   FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
   FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette)
);

CREATE TABLE ligne_panier(
   utilisateur_id INT,
   lunette_id INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(utilisateur_id, lunette_id),
   FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(lunette_id) REFERENCES lunette(id_lunette)
);

CREATE TABLE article_commande(
    lunette_id INT,
    commande_id INT,
    PRIMARY KEY (lunette_id,commande_id),
    FOREIGN KEY (lunette_id) REFERENCES lunette(id_lunette),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande)
);

CREATE TABLE couleur_dispo(
    lunette_id INT,
    couleur_id INT,
    FOREIGN KEY (lunette_id) REFERENCES lunette(id_lunette),
    FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur)
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
                                                     (5,'rose'),
                                                     (6, 'dorée');

INSERT INTO  categorie(id_categorie, libelle_categorie) VALUES
            (1,'Soleil'),
            (2,'Protection'),
            (3,'Vue');

INSERT INTO commande(id_commande, date_achat, etat_id, utilisateur_id) VALUES
            (1,'2024-08-24',1,1),
            (2,'2025-01-13',2,2),
            (3, '2025-03-10',1,2),
            (4, '2024-12-25',2,1),
            (5, '2025-02-28', 3, 2),
            (6, '2025-01-29',1,1),
            (7,'2024-10-19',2,1),
            (8, '2025-02-21',1,2);

INSERT INTO lunette(id_lunette, nom_lunette, genre, indice_protection, longueur_branches,largeur_verres,largeur_pont, prix_lunette, marque, stock, image, couleur_id, categorie_id) VALUES
            (1,'Hedley','Homme',NULL,145,53,18,74.99,'SmartBuy Collection',5,'lunette1',4,3),
            (2,'L6024S 662','Femme',3,145,52,22,120.99,'Lacoste',2,'lunette2',5,1),
            (3,'Murf','Femme',NULL,148,53,19,54.99,'SmartBuy Collection',3,'lunette3',1,3),
            (4,'RB2140 Original Wayfarer 901','Homme',2,150,50,22,138.99,'Ray-Ban',6,'lunette4',1,1),
            (5,'Nike 7170 425', 'Unisexe',NULL,145, 56, 16, 135.00, 'Nike', 8, 'lunette5', 2, 3 ),
            (6, 'Anna-Karin Karlsson CLAW OPTICAL OCTAGONAL - DIAMOND Gold Diamond', 'Femme', NULL, 145, 54, 18, 6227.00, 'Anna-Karin Karlsson', 3, 'lunette6', 6, 3),
            (7, 'Police VK129 BEYOND JR 2 2GHM', 'Enfant', NULL, 135, 48, 18, 60.00, 'Police', 20, 'lunette7',3, 3),
            (8, 'Ray Ban Kids Ray-Ban Kids RJ9069S 100/71', 'Enfant', 3, 130, 48, 16, 73.00, 'Ray-Ban Kids', 15, 'lunette8', 1, 1),
            (9, 'Montana Eyewear MS47 MS47', 'Unisexe', 1, 150, 58, 13, 13.00, 'Montana Eyewear', 50, 'lunette9', 1, 1),
            (10, ' Prada PR 17ZV 15J1O1', 'Femme', NULL, 140, 54, 18, 189.00, 'Prada', 10, 'lunette10', 5, 3 ),
            (11, 'SmartBuy Collection Halia 3362 C2', 'Unisexe', NULL, 147, 55, 19, 32.00, 'SmartBuy Collection', 4, 'lunette11', 4, 3 ),
            (12, 'Tom Ford FT5958-B Blue-Light Block 001', 'Homme', NULL, 140, 60, 12, 283.00, 'Tom Ford', 2, 'lunette12', 1, 3),
            (13, 'Celine CL41390/F Clara Asian Fit BMP', 'Femme', NULL, 145, 52, 18, 108.00, 'Celine', 10, 'lunette13', 2, 3 ),
            (14, 'BOSS Boss 1479/F Asian Fit PJP', 'Homme', NULL, 145, 52, 20, 105.00, 'BOSS', 15, 'lunette14', 2, 3),
            (15, 'Oakley OX8076 CROSSLINK ZERO 807603', 'Homme', NULL, 138, 56, 16, 104.00, 'Oakley', 4, 'lunette15', 1, 3);


INSERT INTO article_commande(lunette_id, commande_id) VALUES
            (1,1),
            (3,1),
            (2,2),
            (4,2),
            (1,2),
            (6, 3),
            (5, 4),
            (8, 4),
            (7, 5),
            (9,5),
            (10, 5),
            (11, 4),
            (12, 6),
            (13, 6),
            (14, 7),
            (15, 7),
            (3, 8),
            (5, 8),
            (10, 8);



INSERT iNTO couleur_dispo(lunette_id, couleur_id) VALUES
    (1,2),
    (1,3),
    (2,2),
    (2,1),
    (3,4),
    (3,1),
    (4, 1),
    (4, 3),
    (5, 2),
    (5, 3),
    (6, 6),
    (7, 3),
    (7, 4),
    (8,1),
    (8,3),
    (9,1),
    (9,4),
    (10,5),
    (10,2),
    (11,4),
    (11,1),
    (12,1),
    (12,5),
    (13,2),
    (13,5),
    (14,2),
    (14,4),
    (15,1),
    (15,3);