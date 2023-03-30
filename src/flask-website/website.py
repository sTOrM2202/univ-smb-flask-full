from flask import Flask, render_template, request, redirect, url_for, session, flash
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
    api_url = f"http://localhost:5000/identity/{username}"
    response = requests.get(api_url)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Récupération des données de l'utilisateur
        user_data = response.json()
        return render_template('list_profile.html', user=user_data)
    else:
        return f"Erreur lors de la récupération des informations de l'utilisateur : {response.status_code}"

@app.route('/list_all')
def list_all():
    # Vérification que l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))

    # Requête vers l'API pour récupérer tous les utilisateurs
    api_url = 'http://localhost:5000/users'
    response = requests.get(api_url)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Récupération des données de tous les utilisateurs
        users_data = response.json()
        # Création du dictionnaire user avec le nom d'utilisateur
        user = {'username': session['username']}
        return render_template('list_all.html', users=users_data, user=user)
    else:
        return f"Erreur lors de la récupération des informations des utilisateurs : {response.status_code}"


@app.route('/profil/<username>')
def list_specific_profil(username):
    # Envoi d'une requête à l'API pour récupérer les informations de l'utilisateur
    api_url = f"http://localhost:5000/identity/{username}"
    response = requests.get(api_url)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Récupération des données de l'utilisateur
        user_data = response.json()
        return render_template('list_specific_profil.html', user=user_data)
    else:
        return f"Erreur lors de la récupération des informations de l'utilisateur : {response.status_code}"


@app.route('/profil', methods=['GET', 'POST'])
def search_specific_profil():
    # Vérification que l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('list_specific_profil', username=username))

    return render_template('list_specific_profil.html')

@app.route('/rp/list', methods=['GET'])
def rp_list():
    # Vérification que l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))

    # Récupération de l'id du RP sélectionné (ou None si aucun n'est sélectionné)
    id_rp = request.args.get('id_rp')

    # Requête vers l'API pour récupérer les reverse proxies
    api_url = 'http://localhost:5000/rp/list'
    if id_rp:
        api_url += '?id_rp={}'.format(id_rp)
    response = requests.get(api_url)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Récupération des données des reverse proxies
        reverse_proxies_data = response.json()
        return render_template('display_rp.html', reverse_proxies=reverse_proxies_data)
    else:
        return f"Erreur lors de la récupération des informations des reverse proxies : {response.status_code}"

@app.route('/rp/delete/<int:id_rp>', methods=['POST', 'DELETE'])
def delete_rp(id_rp):
    # Vérification que l'utilisateur est connecté
    if 'username' not in session:
        return redirect(url_for('login'))

    # Vérification de la méthode HTTP
    if request.method == 'DELETE':
        # Envoi de la demande de suppression à l'API
        api_url = f'http://localhost:5000/rp/delete/{id_rp}'
        response = requests.delete(api_url)

        # Vérification que la requête a réussi
        if response.status_code == 200:
            flash('Le reverse proxy a été supprimé avec succès.', 'success')
        else:
            flash(f'Erreur lors de la suppression du reverse proxy : {response.status_code}', 'error')

        # Redirection vers la liste des reverse proxies
        return redirect(url_for('rp_list'))
    else:
        # Méthode HTTP non autorisée
        abort(405)




