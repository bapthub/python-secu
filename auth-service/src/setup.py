import os
from dotenv import load_dotenv
from flask_pymongo import pymongo
from src.services.crypto import *

### PUBKEY & PRIVKEY GENERATION
path = os.getcwd()
private_key_file = f"{path}/private_key.pem"
public_key_file = f"{path}/public_key.pem"

### ENV VARIABLES
load_dotenv('./src/.env')
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
MAIL_SMTP = os.getenv("MAIL_SMTP")
PASSWORD_SMTP = os.getenv("PASSWORD_SMTP")

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

