from dotenv import load_dotenv
from flask import Flask, Response
from src.services.crypto import *
from src.services.pass_check import *
from flask_pymongo import pymongo
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

### ENV VARIABLES
load_dotenv('.env')
app.secret_key = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)

### MONGODB
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('crypto_users')
user_collection = db['user_collection']
cryptomail_collection = db['cryptomail_collection']

if not os.path.exists(f"{path}/certificates_ca"):
    os.makedirs(f"{path}/certificates_ca")

if not os.path.exists(private_key_file) or not os.path.exists(public_key_file):
    # Generate the key pair if the files don't exist
    private_key, public_key = generate_key_pair()
    store_key_pair(private_key, public_key, private_key_file, public_key_file)

else:
    # Load the existing key pair from files
    private_key, public_key = load_key_pair(private_key_file, public_key_file)

### BCRYPT
bcrypt = Bcrypt(app)

if __name__ == '__main__':
    app.run(debug=False)
