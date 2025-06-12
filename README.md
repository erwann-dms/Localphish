# localphish

![Badge Docker](https://img.shields.io/docker/image-size/library/python/latest)
![GitHub](https://img.shields.io/github/license/erwann-dms/Localphish)

## Objectif
Outil pédagogique complet de gestion de campagnes phishing local, inspiré de GoPhish, pour sensibilisation, tests internes et formation.

## Fonctionnalités
- Interface web admin sécurisée (login, gestion complète des campagnes, visualisation des identifiants récoltés)
- Création, modification, lancement, arrêt et suppression de campagnes phishing
- Gestion intuitive de templates HTML personnalisables pour pages de phishing
- Module DNS spoofing local intégré, activable par campagne ou globalement
- Reverse proxy HTTP(S) local pour rediriger les requêtes vers le serveur phishing adéquat
- Envoi d’emails via SMTP configurable depuis l’interface
- Stockage sécurisé des données et identifiants en base SQLite via SQLAlchemy
- Architecture modulaire et professionnelle avec Docker pour un déploiement facile
- Sécurité renforcée : hash des mots de passe admin, protection CSRF, contrôle d’accès

## Installation

### Prérequis
- Python 3.11+
- Docker & Docker Compose (optionnel mais recommandé)

### Installation manuelle
```bash
git clone https://github.com/votreuser/LocalPhish-Advanced.git
cd LocalPhish-Advanced
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Docker
```bash
docker-compose up --build
```
L’application sera disponible sur : http://localhost:5000

### Configuration
Le fichier config.yaml permet de configurer :

- Admin (utilisateur / mot de passe hashé)
- SMTP (serveur, port, TLS, identifiants)
- DNS spoofing (activation, domaines, IP de redirection)

## Utilisation
- Connectez-vous avec vos identifiants admin.
- Créez et configurez une campagne (choix template HTML, spoofing DNS).
- Lancez la campagne, envoyez les emails via SMTP.
- Visualisez les identifiants récoltés en temps réel.
- Gérer le cycle complet de la campagne (modifier, arrêter, supprimer).

## Disclaimer éthique
Ce projet est uniquement destiné à un usage pédagogique, légal et éthique.
N’utilisez jamais cet outil sans consentement explicite des personnes ciblées.
Toute utilisation malveillante est strictement interdite et hors de la portée de ce projet.

## Licence
MIT

## Architecture du projet
```bash
LocalPhish-Advanced/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── campaigns.py
│   ├── dns_spoof.py
│   ├── proxy.py
│   ├── smtp_sender.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── campaigns.html
│   │   ├── campaign_form.html
│   │   ├── credentials.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
├── config.yaml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── run.py
├── LICENSE
└── README.md
```

## Ajouter des templates de phishing
Depuis l’interface, éditez ou créez une campagne.
Collez votre code HTML personnalisé dans le champ template.
Enregistrez et utilisez ce template pour votre campagne.
