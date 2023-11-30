# CryptoMail

CryptoMail est une api basée sur Flask qui fournit une authentification sécurisée pour les utilisateurs. 
Une caractéristique clé de cette application est l'utilisation de certificats d'attributs pour une authentification robuste et fiable.

## Caractéristiques

1. **Gestion des utilisateurs** : Les utilisateurs peuvent s'inscrire et se connecter en utilisant leurs adresses email. Le mot de passe de l'utilisateur est haché avec Bcrypt (qui utilise l'algorithme Blowfish), puis encodé en base64. Les hachages bcrypt sont des données binaires, et l'encodage en base64 permet de les convertir en chaînes de caractères qui peuvent être facilement stockées dans la base de données MongoDB.

2. **Génération de certificat avec chiffrage RSA** : Pour sécuriser les informations sensibles, l'application utilise le chiffrage RSA. Le fichier crypto.py contient les fonctions pour générer des paires de clés RSA, pour générer des certificats d'attributs et pour vérifier leur validité.

3. **Vérification de validité des certificats d'attributs** : La validité des certificats d'attributs des utilisateurs est vérifiée avant chaque connexion. Les certificats expirés ou révoqués ne sont pas acceptés.

4. **Authentification par certificat d'attributs** : Lors de l'inscription, chaque utilisateur reçoit un certificat d'attributs unique qui doit être téléchargé et utilisé à chaque authentification. Ces certificats sont générés avec des paires de clés RSA et sont stockés sur le serveur.

5. **Vérification par email** : Lorsqu'un utilisateur s'inscrit, un email de vérification avec un code unique est envoyé à l'adresse email de l'utilisateur. Ce code doit être saisi dans l'application pour compléter le processus d'inscription.

## Prérequis

- Docker : [Télécharger Docker](https://www.docker.com/products/docker-desktop)
- Un compte MongoDB 
- Une adresse mail Google avec les mots de passes d'application de configurés [Configuration](https://support.google.com/mail/answer/185833?hl=fr)

## Setup

1. Créer un .env dans /auth
```
MONGO_URI = ""
MAIL_SMTP = "" 
PASSWORD_SMTP = ""
SECRET_KEY = ""
```

2. Ajouter à votre /etc/hosts ces deux lignes:
```
127.0.0.1 demo.com
127.0.0.1 auth.demo.com
```

3. Taper la commande:
   ```bash
   make
   ```

4. Ouvrez votre navigateur web et accédez à `https://demo.com/` pour interagir avec l'application.

5. Pour arrêter et supprimer le conteneur Docker, exécutez :
    ```bash
    make down
    ```
