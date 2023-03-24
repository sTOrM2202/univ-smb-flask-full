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
    else:
        # Nom d'utilisateur ou mot de passe incorrect
        response = {'authenticated': False}
    
    # Retourne la réponse au format JSON à l'application Flask appelante
    return jsonify(response)
