from flask_login import login_required

@route('/protected')
@login_required
def protected_page():
    # Votre contenu protégé ici
    return "Contenu protégé !"