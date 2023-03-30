import requests
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_USER'] = 'louis'
app.config['MYSQL_PASSWORD'] = 'louis'
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
    cur.execute("use identity")
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
    cur.execute("use identity")
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
    cur.execute("use identity")
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


@app.route("/rp/list")
def rp_list():
    id_rp = request.args.get('id_rp') # Récupération de l'id du RP passé en paramètre
    # Connexion à la base de données
    cur = mysql.connection.cursor()

    # Si l'id du RP est fourni en paramètre, récupération des informations seulement pour ce RP
    if id_rp:
        cur.execute("use config_generator")
        cur.execute("SELECT * FROM reverse_proxies WHERE id=%s", (id_rp,))
        rp_data = cur.fetchone()
        if rp_data:
            rp_list = [{'id': rp_data[0], 'name': rp_data[1], 'ip_address': rp_data[2], 'port': rp_data[3]}]
        else:
            rp_list = []
    else:
        # Sinon, récupération de tous les reverse proxies
        cur.execute("use config_generator")
        cur.execute("SELECT * FROM reverse_proxies")
        rp_list = []
        for rp in cur.fetchall():
            rp_data = {'id': rp[0], 'name': rp[1], 'ip_address': rp[2], 'port': rp[3]}
            rp_list.append(rp_data)

    # Fermeture du curseur
    cur.close()

    # Retourne la liste des reverse proxies au format JSON à l'application Flask appelante
    return jsonify(rp_list)

@app.route("/rp/delete/<int:id_rp>", methods=["DELETE"])
def rp_delete(id_rp):
    # Connexion à la base de données
    cur = mysql.connection.cursor()

    # Suppression du reverse proxy correspondant à l'identifiant fourni
    cur.execute("use config_generator")
    cur.execute("DELETE FROM reverse_proxies WHERE id=%s", (id_rp,))
    mysql.connection.commit()

    # Fermeture du curseur
    cur.close()

    # Retourne une réponse pour indiquer que la suppression a réussi
    response = {'message': f'Suppression du reverse proxy {id_rp} réussie'}
    return jsonify(response)


