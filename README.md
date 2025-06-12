# LocalPhish-Pro

![Badge Docker](https://img.shields.io/docker/image-size/library/python/latest)
![GitHub](https://img.shields.io/github/license/youruser/LocalPhish-Pro)

## Objectif
Outil professionnel de démonstration de phishing en local pour sensibilisation et tests internes.

## Fonctionnalités
- Interface web admin (login, gestion campagnes, logs)
- Import facile de templates de phishing
- Spoof DNS local intégré
- Envoi de mails via SMTP (configurable)
- Stockage des identifiants en base SQLite

## Installation
```bash
git clone https://github.com/votreuser/LocalPhish-Pro.git
cd LocalPhish-Pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
```

## Docker
```bash
docker-compose up --build
```

## Disclaimer éthique
**Ce projet est uniquement pour la sensibilisation à la sécurité. N'utilisez jamais cet outil sans consentement explicite.**

## Licence
MIT