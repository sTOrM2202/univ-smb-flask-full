from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/")
def start():
    return render_template('login.html')

@app.route("/layout")
def layout():
    return render_template('layout.html')

@app.route("/login")
def login():
    # Récupération du formulaire de connexion
    username = request.args.get('username')
    password = request.args.get('password')

    # Requête vers l'API pour vérification des informations
    r = requests.get('http://localhost:5000/login', params={'username': username, 'password': password})
    response = r.json()

    # Si l'authentification est réussie, redirection vers la page "layout"
    if response['authenticated']:
        return redirect(url_for('layout'))
    # Sinon, retour à la page de connexion
    else:
        return redirect(url_for('start'))

