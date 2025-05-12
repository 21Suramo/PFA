# IRM Monitoring – Guide de déploiement

## 🧠 Concept

Ce projet permet de surveiller en temps réel la température et la pression affichées sur un écran (par exemple, d’un IRM ou d’un capteur) en utilisant une webcam USB connectée à un Raspberry Pi. Deux zones spécifiques de l'écran sont capturées en continu, et leurs valeurs sont extraites via OCR (Tesseract). Les données sont ensuite envoyées à une API Flask qui les enregistre dans une base de données MongoDB. Une interface web interroge l'API en temps réel pour afficher les valeurs.

## 🧰 Prérequis

- Raspberry Pi 4 (4 GB+) sous Raspberry Pi OS
- Webcam USB
- Serveur (ou le Pi) pour héberger l’API Flask
- Navigateur web pour le dashboard

## 📁 Structure du projet
PFA/
├── raspberry_pi/ # Script Python OCR + envoi
├── backend/ # API Flask + configuration MongoDB
├── frontend/ # Dashboard HTML + JS
└── service/ # Fichier systemd
##  !!!!!!!!!!!!!!!!!!!!! GIT CLONE !!!!!!!!!!!!!!!!!!!!
cd ~
git clone https://github.com/ton_compte/irm-monitoring-project.git

---

## ⚙️ 1. Déploiement sur le Raspberry Pi

sudo apt install -y python3 python3-pip

1. **Mettre à jour le système**  
   ```bash
   sudo apt update && sudo apt upgrade -y

2. **Installer dépendances Python & OCR**

sudo apt install python3-pip tesseract-ocr libjpeg-dev libtiff5 libpng-dev
pip install opencv-python pytesseract requests
pip install -r raspberry_pi/requirements.txt

3. **Copier le dossier du script**

mkdir -p ~/irm-monitoring
cp -r raspberry_pi/ ~/irm-monitoring/


4. **test**
python3 ~/irm-monitoring/main.py

## ⚙️ 2. Déploiement du Backend (API Flask)

1- Installer MongoDB (local ou Atlas): 
   sudo apt install -y mongodb
   sudo systemctl enable mongodb
   sudo systemctl start mongodb

2- **Installer dépendances :**
   cd backend
   pip install -r requirements.txt

3- Configurer l’accès MongoDB dans database.py
4- lancer serveur : 
   python app.py

## 3. Déploiement du Frontend (dashboard)

1- Copier le dossier frontend/ sur une machine avec navigateur
2- Ouvrir index.html directement dans le navigateur
3- Vérifier que le graphique charge les données depuis l’API
npm install -g http-server

## 4. Automatisation du script OCR

1- Copier service/ocr-monitor.service dans /etc/systemd/system/
   sudo cp ~/irm-monitoring-project/service/ocr-monitor.service /etc/systemd/system/
2- Activer et démarrer le service :
   sudo cp service/ocr-monitor.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable ocr-monitor
   sudo systemctl start ocr-monitor
3- Vérifier le statut et logs
   sudo systemctl status ocr-monitor
   journalctl -u ocr-monitor -f


pip install -r requirements.txt
🔧 À noter : il faudra aussi installer Tesseract OCR au niveau système (sudo apt install tesseract-ocr) et, selon la version de Raspbian, des libs OpenCV système (libjpeg-dev, libtiff5-dev, etc.).
