import base64
from flask import (
    request,
    Blueprint,
    Response,
    send_file
)
from src.services.crypto import *
from src.services.pass_check import *
from src.services.email_checking import *
from src.server import check_password_hashed, generate_hashed_password
from src.setup import *
from src.services.service_jwt import *

auth_controller = Blueprint("auth_controller", __name__)

### SIGN-UP PAGE
@auth_controller.route("/signup", methods=["POST"])
def signup():
    request_data = request.get_json()
    
    email = request_data['email']
    password = request_data['password']
    nom = request_data['nom']
    prenom = request_data['prenom']

    if not validate_password(password):
        return Response("{error: 'password do not match required statements'}", status=400)
    
    hashed_password = generate_hashed_password(password)
    hashed_password_b64 = base64.b64encode(hashed_password).decode()

    existing_email = db.user_collection.find_one({"email": email})
    if existing_email:
        return Response("{error: 'email déjà utilisé'}", status=400)
    else:
        db.user_collection.insert_one(
            {
                "email": email,
                "password": hashed_password_b64,
                "nom": nom,
                "prenom": prenom,
                "serial_number": "",
                "status": "Inactive",
            }
        )
        send_mail(email, cryptomail_collection)
        return Response(status=200)


### CODE VERIFICATION PAGE
@auth_controller.route("/code", methods=["POST"])
def code():
    request_data = request.get_json()

    email = request_data['email']
    code = request_data['code']

    if verify_mail(email, cryptomail_collection, code):
        existing_mail = user_collection.find_one({"email": email})
        nom = existing_mail.get("nom")
        prenom = existing_mail.get("prenom")
        pem_cert, serial_number = generate_attribute_certificate(
            prenom, nom, email, private_key, public_key
        )
        with open(f"{path}/certificates_ca/{serial_number}.pem", "wb") as file:
            file.write(pem_cert)
        db.user_collection.update_one(
            {"email": email}, {"$set": {"serial_number": serial_number}}
        )
        db.user_collection.update_one({"email": email}, {"$set": {"status": "Active"}})
        return Response("{status:'Code valide.'}", status=200)
    else:
        return Response("{error: 'Email ou code incorrect.'}", status=400)

### RESEND CODE PAGE
@auth_controller.route("/resend", methods=["POST"])
def resend():
    request_data = request.get_json()
    email = request_data['email']   
     
    existing_mail = user_collection.find_one({"email": email})
    if existing_mail:
        status = existing_mail.get("status")
        if status == "Active":
            # flash("", "info")
            return Response("{status:'Compte déjà activé.'}",status=400)

        send_mail(email, cryptomail_collection)
        return Response("{status: 'Code envoyé.'}",status=200)
    return Response("{error: 'email inconnu'}",status=400)


### CERTIFICATE WITH AUTHENTICATION PAGE
@auth_controller.route("/certificate", methods=["POST"])
def certificate():
    request_data = request.get_json()
    
    email = request_data['email']
    password = request_data['password']
    existing_mail = user_collection.find_one({"email": email})

    if existing_mail:
        user_pass_b64 = existing_mail.get("password")
        user_pass = base64.b64decode(user_pass_b64).decode()
        if check_password_hashed(user_pass, password):
            serial = existing_mail.get("serial_number")
            file_path = f"/app/certificates_ca/{serial}.pem"
            return send_file(file_path, as_attachment=True)
        else:
            return Response("{error: 'Utilisateur ou mot de passe incorrect.'}",status=400)
    else:
        return Response("{error: 'Utilisateur ou mot de passe incorrect.'}",status=400)
    
### LOGIN PAGE
@auth_controller.route("/login", methods=["POST"])
def login():
    
    email = request.form['email']
    password = request.form['password']
    certificate_file = request.files["certificate"]
    
    if "certificate" in request.files:
        existing_mail = user_collection.find_one({"email": email})

        if existing_mail:
            user_pass_b64 = existing_mail.get("password")
            user_pass = base64.b64decode(user_pass_b64).decode()
            # Password check
            if check_password_hashed(user_pass, password):
                # Active account check
                if existing_mail.get("status") == "Inactive":
                    return Response("{error:'Compte inactif'}",status=400)
                # Certificate validity check
                serial = existing_mail.get("serial_number")
                certificate_file.save(f"/tmp/{serial}.pem")
                file_loc = f"/tmp/{serial}.pem"
                res = check_certificate_validity(file_loc, email, path, public_key)
                if res != "valid":
                    return Response("{error:'Certificat invalide.'}",status=400)
                if os.path.exists(file_loc):
                    os.remove(file_loc)
                jwt_token = encode_payload(2)
                return Response("{status: 'Authentification terminée', 'jwt': '" + jwt_token + "'}", status=200)
            return Response("{error:'Utilisateur ou mot de passe incorrect'}",status=400)

        else:
            return Response("{error:'Utilisateur ou mot de passe incorrect'}",status=400)
    return Response("{error:'Données incorrectes'}",status=400)

### LOGIN PAGE WITH JWT
@auth_controller.route("/login_jwt", methods=["POST"])
def login_jwt():
    
    request_data = request.get_json()
    encoded_jwt = request_data["jwt"]
    return_val = check_payload(encoded_jwt)
    if return_val == True:
        return Response("{status:'Token Valide, authentification réussie'}", status=200)
    else:
        return Response('{"error": "' + str(return_val) + '"}', status=400)