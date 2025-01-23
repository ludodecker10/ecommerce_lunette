DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS lunette;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;



CREATE TABLE utilisateur(
   id_utilisateur INT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(50),
    est_actif VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE etat(
   id_etat INT,
   libellle_etat VARCHAR(50),
   PRIMARY KEY(id_etat)
);

CREATE TABLE couleur(
   id_couleur INT,
   libelle_couleur TEXT,
   PRIMARY KEY(id_couleur)
);

CREATE TABLE categorie(
   id_categorie INT,
   liibelle_categorie VARCHAR(50),
   PRIMARY KEY(id_categorie)
);

CREATE TABLE commande(
   id_commande INT,
   date_achat DATE,
   id_etat INT NOT NULL,
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

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

CREATE TABLE ligne_commande(
   id_commande INT,
   id_lunette INT,
   prix INT,
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



INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');


