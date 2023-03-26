from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Clé secrète pour les sessions

@app.route("/")
def start():
    return render_template('start.html')

@app.route("/login")
def login():
    # Récupération des informations de connexion envoyées depuis le formulaire
    username = request.args.get('username')
    password = request.args.get('password')

    # Requête vers l'API pour vérification des informations
    r = requests.get('http://localhost:5000/login', params={'username': username, 'password': password})
    response = r.json()

    # Si l'authentification est réussie, création de la session et redirection vers la page "layout"
    if response['authenticated']:
        session['username'] = username
        return redirect(url_for('start'))
    # Sinon, retour à la page de connexion avec un message d'erreur
    else:
        error = "Login ou mot de passe incorrect"
        return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    # Suppression de la session de l'utilisateur
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/list_profile")
def list_profile():
    # Vérification que l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))

    # Récupération du nom d'utilisateur en session
    username = session['username']

    # Envoi d'une requête à l'API pour récupérer les informations de l'utilisateur
    api_url = f"http://localhost:5000/info?username={username}"
    response = requests.get(api_url)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Récupération des données de l'utilisateur
        user_data = response.json()
        return render_template('list_profile.html', user=user_data)
    else:
        return render_template('error.html', message="Erreur lors de la récupération des informations de l'utilisateur")