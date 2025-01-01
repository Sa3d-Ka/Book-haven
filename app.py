from flask import Flask, render_template, request
from datetime import datetime


biblio = Flask(__name__)

livres = {}
emprunts = {}
utilisateurs = {}


@biblio.route("/")
def MenuPricipal():
    return render_template("menuPrincipal.html",
                           title='Menu', 
                           css="menuPrincipal")

@biblio.route('/gestion-livres')
def gestion_livres():
    return render_template('gestionLivres/gestionLivres.html',
                           title='Gestion Livres',
                           css='gestionLivres/gestionLivres')

@biblio.route("/ajouter-livre", methods=["GET", "POST"])
def ajouterLivre():
    existe = None
    if request.method == "POST":
        isbn = request.form.get("isbn")
        titre = request.form.get("titre")
        auteur = request.form.get("auteur")
        quantite = int(request.form.get("quantite"))

        if isbn in livres:  
            existe = True
        else:
            existe = False
            livres[isbn] = {
                "titre": titre,
                "auteur": auteur,
                "quantite": quantite
            }
    return render_template('gestionLivres/ajouterLivre.html',
                           title='Ajouter Livre',
                           css='gestionLivres/ajouterLivre',
                           bootstrap='yes',
                           existe=existe,)

@biblio.route("/supprimer-livre", methods=["GET", "POST"])
def supprimerLivre():
    notexiste = None
    if request.method == "POST":
        isbn = request.form.get("isbn")

        if isbn not in  livres:  
            notexiste = True
            
        else:
            notexiste = False
            del livres[isbn]
            
    return render_template('gestionLivres/supprimerLivre.html',
                           title='Supprimer Livre',
                           css='gestionLivres/supprimerLivre',
                           bootstrap='yes',
                           notexiste=notexiste,)

@biblio.route("/gestion-emprunts")
def GestionEmprunts():
    return render_template('emprunts/gestionEmprunts.html',
                           title='Gestion Emprunts',
                           css='emprunts/gestionEmprunts')

@biblio.route("/emprunter-livre", methods=["GET", "POST"])
def EmprunterLivre():
    notexiste = None
    quantite = None
    notcin = None
    notisbn = None

    if request.method == "POST":
        cin = request.form.get("cin")
        isbn = request.form.get("isbn")

        if cin not in utilisateurs:
            notexiste = True
            notcin = f"Client de cin '{cin}' n'existe pas"
        elif isbn not in livres:
            notexiste = True
            notisbn = f"Le livre avec l'ISBN {isbn} n'existe pas."
        elif livres[isbn]['quantite'] <= 0:
            quantite = f"Le livre '{(livres[isbn]['titre'])}' n'est pas disponible pour le moment."
        else:
            notexiste = False
            emprunts[cin] = isbn
            livres[isbn]['quantite'] -= 1

    return render_template(
        'emprunts/emprunterLivre.html',
        title='Emprunter Livre',
        css='emprunts/emprunterLivre',
        bootstrap='yes',
        notexiste=notexiste,
        q=quantite,
        notcin=notcin,
        notisbn=notisbn)

@biblio.route("/retourner-livre", methods=["GET", "POST"])
def RrtournerLivre():
    notexiste = None
    notcin = None

    if request.method == "POST":
        cin = request.form.get("cin")
        isbn = emprunts[cin]

        if cin not in emprunts:
            notexiste = True
            notcin = f"Client de cin '{cin}' a aucun emprunte"
        else:
            notexiste = False
            del emprunts[cin]
            livres[isbn]['quantite'] += 1

    return render_template(
        'emprunts/retournerLivre.html',
        title='Retourner Livre',
        css='emprunts/retournerLivre',
        bootstrap='yes',
        notexiste=notexiste,
        notcin=notcin)

@biblio.route("/calcule-amende")
def CalculAmende():
    return render_template('emprunts/calculAmende.html',
                           title='Calcul Amende',
                           css='emprunts/calculAmende',
                           bootstrap='yes',)

@biblio.route("/afficher-amende", methods=["GET", "POST"])
def AfficherAmende():
    if request.method == "POST":
        date_prevue = request.form.get("date_prevue")
        date_reel = request.form.get("date_reel")

        prevue = datetime.strptime(date_prevue, "%Y-%m-%d")
        reel = datetime.strptime(date_reel, "%Y-%m-%d")

        delta = (reel - prevue).days

        if delta > 0:
            retard = delta
            amende = retard * 10 
        else:
            retard = 0
            amende = 0
        
    return render_template('emprunts/afficherAmende.html',
                           title='Afficher Amende',
                           css='emprunts/afficherAmende',
                           bootstrap='yes',
                           retard=retard,
                           amende=amende)

@biblio.route("/afficher-livres")
def afficherLivres():
    return render_template('afficher/afficherLivres.html',
                           title='Affichage',
                           css='afficher/afficherLivres',
                           bootstrap='yes',
                           LIVRES=livres)

@biblio.route("/recherche-livres")
def RechercheLivres():
    return render_template('recherche/rechercheLivres.html',
                           title='Recherche',
                           css='recherche/rechercheLivres',
                           bootstrap='yes')

@biblio.route("/resultat", methods=["GET", "POST"])
def Resultat():
    resultats = []
    if request.method == "POST":
        mot_cle = request.form.get("recherche")
        
        for isbn, details in livres.items():
            if mot_cle.lower() in details['titre'].lower() or mot_cle.lower() in details['auteur'].lower():
                resultats.append((isbn, details))

    return render_template('recherche/resultat.html',
                           title='Resultat',
                           css='recherche/resultat',
                           bootstrap='yes',
                           RESULTATS=resultats)

@biblio.route("/statistiques")
def StatistiquesLivres():
    livres_disponibles = 0

    total_livres = len(livres)
    total_empruntes = len(emprunts)

    for info in livres.values():
        if info['quantite'] > 0:
            livres_disponibles += 1

    return render_template('statistiques/statistiques.html',
                           title='Statistiques',
                           css='statistiques/statistiques',
                           bootstrap='yes',
                           total_livres=total_livres,
                           total_empruntes=total_empruntes,
                           livres_disponibles=livres_disponibles)

@biblio.route('/gestion-utilisateurs')
def GestionUtilisateurs():
    return render_template('utilisateurs/gestionUtilisateurs.html',
                           title='Gestion Utilisateurs',
                           css='utilisateurs/gestionUtilisateurs')

@biblio.route("/ajouter-utilisateur", methods=["GET", "POST"])
def AjouterUtilisateur():
    existe = None
    if request.method == "POST":
        cin = request.form.get("cin")
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")

        if cin in utilisateurs:  
            existe = True
        else:
            existe = False
            utilisateurs[cin] = {
                "nom": nom,
                "prenom": prenom,
            }
    return render_template('utilisateurs/ajouterUtilisateur.html',
                           title='Ajouter Utilisateur',
                           css='utilisateurs/ajouterUtilisateur',
                           bootstrap='yes',
                           existe=existe,)

@biblio.route("/afficher-utilisateurs")
def AfficherUtilisateurs():
    return render_template('utilisateurs/afficherUtilisateur.html',
                           title='Afficher Utilisateur',
                           css='utilisateurs/afficherUtilisateur',
                           bootstrap='yes',
                           utilisateurs=utilisateurs)

@biblio.route("/supprimer-utilisateur", methods=["GET", "POST"])
def SupprimerUtilisateur():
    notexiste = None
    if request.method == "POST":
        cin = request.form.get("cin")

        if cin not in  utilisateurs:  
            notexiste = True
            
        else:
            notexiste = False
            del utilisateurs[cin]
            
    return render_template('utilisateurs/supprimerUtilisateur.html',
                           title='Supprimer Utilisateur',
                           css='utilisateurs/supprimerUtilisateur',
                           bootstrap='yes',
                           notexiste=notexiste,)
    

if __name__ == "__main__":

    biblio.run(debug=True, port=9000)


