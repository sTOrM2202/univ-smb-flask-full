# Démarrage

Connexion à Gitpod :

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/sTOrM2202/univ-smb-flask-full)

# Sites

Démarrage du Site Web API :

`cd src/flask-api/ && flask --app api run -p 5000`

Démarrage du Site Web WebSite :

`cd src/flask-website/ && flask --app website run -p 5001`

# Base de données

## Pour voir l'état du serveur de base de données

`sudo /etc/init.d/mysql status`

## Pour configurer la base de données

`cd manifest/ && chmod +x db.sh`

## Se connecter à la base de données

Le mot de passe est dans le fichier de base de données.

`sudo mysql -u root -p`

## Avancé du projet

Pour la partie utilisateur nous pouvons tout faire. CAD
-	Une authentification
-	Lister son profil 
-	Lister tout les profils
- Lister un profil spécifique

Pour la partie Serveur. J'ai fais que les Reverse Proxi
- Nous pouvons lister les RP
- Nous pouvons Supprimer un RP en fonction de son ID
- Nous pouvons créer un RP en fonction

Pour importer la BDD voir databases.txt

Merci à vous pour le projet.




