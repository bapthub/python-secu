from flask import Flask, Response
from src.services.crypto import *
from src.services.pass_check import *
from src.services.email_checking import *
from flask_bcrypt import Bcrypt
from src.controllers.auth_controller import auth_controller
from src.setup import *

app = Flask(__name__)
app.register_blueprint(auth_controller)
app.config.from_pyfile("setup.py")

app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=False)
