import base64
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    Response,
)
from src.services.crypto import *
from src.services.pass_check import *
from src.services.email_checking import *
from src.setup import *

auth_controller = Blueprint("auth_controller", __name__)

### LOGIN PAGE
@auth_controller.route("/login", methods=["POST"])
def login():
    if "certificate" in request.files:
        certificate_file = request.files["certificate"]
        email = request.form["email"]
        password = request.form["password"]
        existing_mail = user_collection.find_one({"email": email})

        if existing_mail:
            user_pass_b64 = existing_mail.get("password")
            user_pass = base64.b64decode(user_pass_b64).decode()
            # Password check
            if check_password_hashed(user_pass, password):
                # Active account check
                if existing_mail.get("status") == "Inactive":
                    flash("Votre compte n'est pas activé.", "error")
                    return redirect(url_for("resend"))
                # Certificate validity check
                if certificate_file.filename != "":
                    serial = existing_mail.get("serial_number")
                    certificate_file.save(f"/tmp/{certificate_file.filename}")
                    file_loc = f"/tmp/{certificate_file.filename}"
                    res = check_certificate_validity(file_loc, email, path, public_key)
                    if res != "valid":
                        flash("Certificat invalide.", "error")
                        return redirect(url_for("login"))
                    if os.path.exists(file_loc):
                        os.remove(file_loc)
                    return "Authentification terminée"
                flash("Upload échoué.", "error")
                return redirect(url_for("login"))
            flash("Utilisateur ou mot de passe incorrect", "error")
            return redirect(url_for("login"))

        else:
            flash("Utilisateur ou mot de passe incorrect", "error")
            return redirect(url_for("login"))
    flash("Données incorrectes", "error")
    return redirect(url_for("login"))


### SIGN-UP PAGE
@auth_controller.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    nom = request.form["nom"]
    prenom = request.form["prenom"]

    if not validate_password(password):
        flash("Le mot de passe ne respecte pas les conditions requises.", "error")
        return render_template("signup.html")

    hashed_password = generate_hashed_password(password)
    hashed_password_b64 = base64.b64encode(hashed_password).decode()

    existing_email = db.user_collection.find_one({"email": email})
    if existing_email:
        flash(f"{email} est déjà utilisé", "error")
        return Response(status=400)
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
    email = request.form["email"]
    code = request.form["code"]

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
        flash("Code valide.", "info")
        return Response(status=200)
    else:
        flash("Email ou code incorrect.", "error")
        return Response(status=400)


### RESEND CODE PAGE
@auth_controller.route("/resend", methods=["POST"])
def resend():
    email = request.form["email"]

    existing_mail = user_collection.find_one({"email": email})
    if existing_mail:
        status = existing_mail.get("status")
        if status == "Active":
            flash("Compte déjà activé.", "info")
            return Response(status=400)

        send_mail(email, cryptomail_collection)
        flash("Code envoyé.", "info")
        return Response(status=200)
    else:
        return Response(status=200)


### CERTIFICATE WITH AUTHENTICATION PAGE
@auth_controller.route("/certificate", methods=["POST"])
def certificate():
    email = request.form["email"]
    password = request.form["password"]
    existing_mail = user_collection.find_one({"email": email})

    if existing_mail:
        user_pass_b64 = existing_mail.get("password")
        user_pass = base64.b64decode(user_pass_b64).decode()
        if check_password_hashed(user_pass, password):
            serial = existing_mail.get("serial_number")
            file_path = f"certificates_ca/{serial}.pem"
            return Response("{serial:" + str(serial) + "}", status=200)
        else:
            flash("Utilisateur ou mot de passe incorrect.", "error")
            return Response(status=400)
    else:
        flash("Utilisateur ou mot de passe incorrect.", "error")
        return Response(status=400)
