import os
import base64
from dotenv import load_dotenv
from flask import Flask,request,render_template,redirect,url_for, flash, send_file
from crypto import *
from pass_check import *
from flask_pymongo import pymongo
from email_checking.email_checking import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.register_blueprint(auth_routes)
app.register_blueprint(download_routes)

### ENV VARIABLES
load_dotenv('.env')
app.secret_key = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")

### MONGODB
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database('crypto_users')
user_collection = db['user_collection']
cryptomail_collection = db['cryptomail_collection']

### PUBKEY & PRIVKEY GENERATION
path = os.getcwd()
private_key_file = f"{path}/private_key.pem"
public_key_file = f"{path}/public_key.pem"

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

def generate_hashed_password(password):
    return bcrypt.generate_password_hash(password)

def check_password_hashed(pass_hash, password):
    return bcrypt.check_password_hash(pass_hash, password)



if __name__ == '__main__':
    app.run(debug=False)