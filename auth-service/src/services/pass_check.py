import re
from flask_bcrypt import generate_password_hash,check_password_hash

def validate_password(password):
    # Vérifier la longueur du mot de passe
    if len(password) < 10:
        return False

    # Vérifier la présence d'au moins une lettre majuscule
    if not re.search(r'[A-Z]', password):
        return False

    # Vérifier la présence d'au moins une lettre minuscule
    if not re.search(r'[a-z]', password):
        return False

    # Vérifier la présence d'au moins un chiffre
    if not re.search(r'\d', password):
        return False

    # Vérifier la présence d'au moins un caractère spécial parmi !@#$%^&*-+=€
    if not re.search(r'[!@#$%^&*\-+=€]', password):
        return False

    return True

def generate_hashed_password(password):
    return generate_password_hash(password)

def check_password_hashed(pass_hash, password):
    return check_password_hash(pass_hash, password)
