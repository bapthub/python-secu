# CryptoMail

CryptoMail est une api basée sur Flask qui fournit une authentification sécurisée pour les utilisateurs. 
Une caractéristique clé de cette application est l'utilisation de certificats d'attributs pour une authentification robuste et fiable.


## Prérequis

- Docker : [Télécharger Docker](https://www.docker.com/products/docker-desktop)
- Un compte MongoDB 
- Une adresse mail Google avec les mots de passes d'application de configurés [Configuration](https://support.google.com/mail/answer/185833?hl=fr)


## Setup

Créer un .env dans /auth
```
MONGO_URI = 
MAIL_SMTP = 
PASSWORD_SMTP = 
SECRET_KEY = 
```

Ajouter à votre /etc/hosts ces deux lignes:
```
127.0.0.1 demo.com
127.0.0.1 auth.demo.com
```

## Usage
docker-compose up -d

Url de la démo:
https://demo.com/
