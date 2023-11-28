from flask import Flask, Response
from src.services.crypto import *
from src.services.pass_check import *
from src.services.email_checking import *
from flask_bcrypt import Bcrypt
from src.controllers.auth_controller import auth_controller
from src.controllers.download_controller import download_controller
from src.setup import *

app = Flask(__name__)

app.register_blueprint(auth_controller)
app.register_blueprint(download_controller)

@app.route('/test', methods=['GET'])
def test():
    return Response("{test: 'message de test'}", status=200)

app.secret_key = os.getenv("SECRET_KEY")
### BCRYPT
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=False)
