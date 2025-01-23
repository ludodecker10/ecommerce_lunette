DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS lunette;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS commande;


CREATE TABLE utilisateur(
   id_utilisateur INT,
   login VARCHAR(50),
   email VARCHAR(50),
   nom VARCHAR(50),
   password VARCHAR(50),
   role VARCHAR(50),
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
