import requests
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_USER'] = 'louis'
app.config['MYSQL_PASSWORD'] = 'louis'
app.config['MYSQL_DB'] = 'identity'
app.config['MYSQL_HOST'] = 'localhost'

# Initialisation de la connexion à la base de données
mysql = MySQL(app)

@app.route("/login")
def login():
    # Récupération des informations de connexion envoyées depuis website.py
    username = request.args.get('username')
    password = request.args.get('password')    
    
    # Connexion à la base de données
    cur = mysql.connection.cursor()
    
    # Récupération de l'utilisateur correspondant au nom d'utilisateur
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    
    # Vérification du mot de passe
    if user and user[2] == password:
        # Utilisateur authentifié
        response = {'authenticated': True}
        status_code = 200
    else:
        # Nom d'utilisateur ou mot de passe incorrect
        response = {'authenticated': False, 'error': 'Nom d\'utilisateur ou mot de passe incorrect'}
        status_code = 401
    
    # Fermeture du curseur
    cur.close()
    
    # Retourne la réponse au format JSON à l'application Flask appelante
    return jsonify(response), status_code


@app.route("/identity/<username>")
def identity(username):
    # Affichage d'un message de débogage
    print(f"Requête reçue pour l'utilisateur {username}")

    # Connexion à la base de données
    cur = mysql.connection.cursor()

    # Récupération de l'utilisateur correspondant au nom d'utilisateur
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    # Fermeture du curseur
    cur.close()

    # Si l'utilisateur existe, on renvoie ses informations, sinon une erreur
    if user:
        response = {'id': user[0], 'username': user[1], 'password': user[2], 'firstname': user[3], 'lastname': user[4], 'birthdate': str(user[5])}
    else:
        response = {'error': 'Utilisateur non trouvé'}
    # Retourne la réponse au format JSON à l'application Flask appelante
    return jsonify(response)

@app.route("/users")
def users():
    # Connexion à la base de données
    cur = mysql.connection.cursor()

    # Récupération de tous les utilisateurs
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    # Fermeture du curseur
    cur.close()

    # Création d'une liste contenant les informations de chaque utilisateur
    user_list = []
    for user in users:
        user_data = {'id': user[0], 'username': user[1], 'password': user[2], 'firstname': user[3], 'lastname': user[4], 'birthdate': str(user[5])}
        user_list.append(user_data)

    # Retourne la liste des utilisateurs au format JSON à l'application Flask appelante
    return jsonify(user_list)
