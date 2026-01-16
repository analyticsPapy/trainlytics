# Trainlytics - Guide de Démarrage Rapide

## 🚀 Démarrage en 5 minutes avec Docker

### Prérequis
- Docker et Docker Compose installés
- Git

### Étape 1 : Cloner et configurer

```bash
git clone https://github.com/analyticsPapy/trainlytics.git
cd trainlytics
cp .env.example .env
```

### Étape 2 : Démarrer l'application

```bash
docker-compose up -d
```

Cette commande va :
- ✅ Démarrer PostgreSQL (port 5432)
- ✅ Démarrer Redis (port 6379)
- ✅ Démarrer le backend FastAPI (port 8000)
- ✅ Démarrer le frontend React (port 5173)

### Étape 3 : Accéder à l'application

- **Frontend** : http://localhost:5173
- **API Backend** : http://localhost:8000
- **Documentation API** : http://localhost:8000/api/docs

### Étape 4 : Créer un compte

1. Ouvrez http://localhost:5173
2. Cliquez sur "Register"
3. Créez votre compte
4. Connectez-vous !

---

## 🛠️ Développement Local (sans Docker)

### Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements-dev.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos paramètres

# Démarrer le serveur
uvicorn app.main:app --reload
```

Backend disponible sur http://localhost:8000

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.example .env

# Démarrer le serveur de développement
npm run dev
```

Frontend disponible sur http://localhost:5173

---

## 📦 Structure du Projet

```
trainlytics/
├── backend/              # API Python/FastAPI
│   ├── app/
│   │   ├── api/         # Endpoints API
│   │   ├── models/      # Modèles de base de données
│   │   ├── core/        # Configuration
│   │   └── main.py      # Point d'entrée
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/            # Application React
│   ├── src/
│   │   ├── pages/       # Pages de l'application
│   │   ├── components/  # Composants réutilisables
│   │   ├── store/       # Redux store
│   │   └── services/    # Services API
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml   # Configuration Docker
├── ARCHITECTURE.md      # Documentation architecture
└── README.md            # Documentation principale
```

---

## 🎯 Fonctionnalités Implémentées

### ✅ Authentification
- Inscription / Connexion
- JWT tokens
- Sessions sécurisées

### ✅ Base de Données
- Modèles utilisateurs (athletes, coaches)
- Modèles d'activités
- Modèles de workouts
- Plans d'entraînement
- Commentaires et notifications

### ✅ API Endpoints
- `/api/v1/auth/login` - Connexion
- `/api/v1/auth/register` - Inscription
- `/api/v1/users/me` - Profil utilisateur
- `/api/v1/activities` - Gestion des activités
- `/api/v1/workouts` - Gestion des workouts

### ✅ Interface Utilisateur
- Page de connexion
- Page d'inscription
- Dashboard athlète
- Pages activités et workouts
- Navigation responsive

---

## 🔧 Commandes Utiles

### Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f backend

# Arrêter les services
docker-compose down

# Reconstruire les images
docker-compose build

# Redémarrer un service
docker-compose restart backend
```

### Base de Données

```bash
# Accéder à PostgreSQL
docker-compose exec postgres psql -U trainlytics_user -d trainlytics

# Voir les tables
docker-compose exec postgres psql -U trainlytics_user -d trainlytics -c "\dt"
```

### Backend

```bash
# Lancer les tests
cd backend
pytest

# Créer une migration
alembic revision --autogenerate -m "Description"

# Appliquer les migrations
alembic upgrade head
```

### Frontend

```bash
# Build production
cd frontend
npm run build

# Linter
npm run lint
```

---

## 🐛 Résolution de Problèmes

### Le backend ne démarre pas

1. Vérifiez que PostgreSQL est en cours d'exécution :
```bash
docker-compose ps postgres
```

2. Vérifiez les logs :
```bash
docker-compose logs backend
```

### Le frontend ne se connecte pas au backend

1. Vérifiez la variable d'environnement `VITE_API_URL` dans `frontend/.env`
2. Vérifiez que le backend est accessible : http://localhost:8000/health

### Erreur de connexion à la base de données

1. Vérifiez que le mot de passe dans `.env` correspond
2. Attendez que PostgreSQL soit complètement démarré (healthcheck)

---

## 📚 Prochaines Étapes

1. **Connecteurs Externes** : Implémenter Strava, Garmin, Polar, Coros
2. **Analytics** : Ajouter les graphiques et métriques
3. **Plans d'Entraînement** : Interface de création de plans
4. **Notifications** : WebSocket en temps réel
5. **Tests** : Augmenter la couverture de tests

---

## 📖 Documentation Complète

- [Architecture détaillée](./ARCHITECTURE.md)
- [README principal](./README.md)
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

---

## 🤝 Contribution

Le projet est maintenant prêt pour le développement collaboratif !

1. Créez une branche : `git checkout -b feature/ma-fonctionnalite`
2. Committez vos changements : `git commit -m "Ajout de ma fonctionnalité"`
3. Push vers GitHub : `git push origin feature/ma-fonctionnalite`
4. Créez une Pull Request

---

## 📞 Support

Pour toute question :
- Consultez la [documentation](./ARCHITECTURE.md)
- Créez une [issue GitHub](https://github.com/analyticsPapy/trainlytics/issues)

Bon développement ! 🎉
