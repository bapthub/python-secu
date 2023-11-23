import os
from flask import Flask,request,render_template,redirect,url_for, flash
from crypto import *
from flask_pymongo import pymongo
from dotenv import load_dotenv

app = Flask(__name__)

### ENV VARIABLES
load_dotenv('.env')
app.secret_key = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)

db = client.get_database('crypto_users')
user_collection = pymongo.collection.Collection(db,'user_collection')

def flask_mongodb_atlas():
    return "flask mongodb atlas!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        existing_username = db.user_collection.find_one({"username": username})
        if existing_username:
            return "user exists"
        else:
            db.user_collection.insert_one({"name": username})
            return "insert"
    else:
        return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

@app.route('/delete/<username>', methods=['POST'])
def delete_entries(username):
    # Supprimer toutes les entrées pour l'utilisateur actuel dans la base de données
    db.user_collection.delete_many({"username": username})
    flash("All entries have been deleted.")
    return redirect(url_for('visited', username=username))

if __name__ == '__main__':
    app.run(debug=True)