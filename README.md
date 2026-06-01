# academic-performance-analyzer
# 🎓 Academic Performance Analyzer

Application web intelligente d'analyse de performance académique développée dans le cadre du module **SDIA — Systèmes Distribués et Intelligence Artificielle** (Projet Technologies Web).

> **Dataset utilisé :** [OULAD — Open University Learning Analytics Dataset](https://analyse.kmi.open.ac.uk/open_dataset)

---


##  État d'avancement

### Membre 1 — Backend (Django + ML) — 70% terminé

| Module | Statut |
|--------|--------|
| Setup Django (projet, apps, config, CORS) | ✅ Terminé |
| Modèles de données OULAD (Student, Assessment, VLE...) | ✅ Terminé |
| API REST complète (15 endpoints) | ✅ Terminé |
| Import CSV dataset OULAD | ✅ Terminé |
| Endpoints analytiques (stats, distribution, VLE...) | ✅ Terminé |
| Feature engineering + Random Forest + SHAP | ✅ Terminé |
| API prédiction individuelle + en lot | 🔄 En cours |
| Détection étudiants à risque | 🔄 En cours |
| API recommandations personnalisées | ⏳ À faire |
| Tests unitaires + documentation | ⏳ À faire |

### Membre 2 — Frontend (React) — À démarrer

| Module | Statut |
|--------|--------|
| Setup React + layout + navigation | ⏳ À faire |
| Page import CSV | ⏳ À faire |
| Dashboard analytique (Recharts) | ⏳ À faire |
| Page profil étudiant | ⏳ À faire |
| Page étudiants à risque + SHAP | ⏳ À faire |
| Présentation PPT | ⏳ À faire |
| Vidéo démo | ⏳ À faire |

---

## 🏗️ Architecture technique
academic-performance-analyzer/
├── config/              → Configuration Django (settings, urls, wsgi)
├── students/            → Modèles + API étudiants, modules, import CSV
├── predictions/         → Modèle Prediction en base de données
├── analytics/           → 6 endpoints analytiques (stats, VLE, distribution...)
├── ml_models/           → Pipeline ML (feature engineering, Random Forest, SHAP)
│   ├── saved_models/    → Modèles .pkl sauvegardés (ignorés par git)
│   └── management/
│       └── commands/
│           └── train_model.py  → Commande Django custom
├── manage.py
├── requirements.txt
└── README.md

---
## 👥 Équipe

| Membre | Rôle | Responsabilités |
|--------|------|-----------------|
| **Membre 1** | Backend & IA | Django REST API · Machine Learning · SHAP · Import OULAD |
| **Membre 2** | Frontend & Data | React · Dashboard · Visualisations · PPT · Vidéo |

---

## ⚙️ Installation — Backend (Membre 1)

### Prérequis
- Python 3.11
- Git

### Étapes

```bash
# 1. Cloner le repo
git clone https://github.com/VOTRE_USERNAME/academic-performance-analyzer.git
cd academic-performance-analyzer

# 2. Créer et activer l'environnement virtuel
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer le fichier .env à la racine
# Contenu du .env :
# SECRET_KEY=votre-cle-secrete-ici
# DEBUG=True

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un superuser (optionnel)
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

L'API est accessible sur **http://127.0.0.1:8000/api/**

---

## 📡 Endpoints API disponibles

### Étudiants
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/students/` | Liste paginée avec filtres |
| GET | `/api/students/{id}/` | Profil complet |
| GET | `/api/students/at-risk/?threshold=0.7` | Étudiants à risque |
| GET | `/api/modules/` | Liste des modules |

### Import
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/import/students/` | Import fichier CSV OULAD |

### Analytiques
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/analytics/stats/` | Statistiques globales |
| GET | `/api/analytics/distribution/` | Distribution âge / genre / région |
| GET | `/api/analytics/by-module/` | Stats par module académique |
| GET | `/api/analytics/vle-activity/` | Engagement VLE |
| GET | `/api/analytics/assessments/` | Stats évaluations |
| GET | `/api/analytics/students/{id}/profile/` | Profil analytique complet |

### Machine Learning
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/ml/train/` | Entraîner le modèle Random Forest |
| GET | `/api/ml/info/` | Infos sur le modèle chargé |
| POST | `/api/ml/predict/{id}/` | Prédire résultat + SHAP |
| POST | `/api/ml/predict-all/` | Prédire tous les étudiants en lot |

---

## 🤖 Pipeline Machine Learning
Dataset OULAD (CSV)
↓
Import & parsing (pandas)
↓
Feature Engineering (16 features)
→ gender, disability, num_prev_attempts, studied_credits
→ age_band, highest_education, imd_band
→ avg_score, max_score, min_score
→ nb_assessments, nb_tma, nb_cma
→ total_clicks, nb_vle_types, nb_vle_days
↓
Entraînement Random Forest + GridSearchCV
→ Optimisation : n_estimators, max_depth, min_samples_split
→ Évaluation : Accuracy, F1, Precision, Recall, CV 5-fold
↓
Explicabilité SHAP (TreeExplainer)
→ shap_values par étudiant
→ Top features par prédiction
↓
Sauvegarde joblib (.pkl)
→ random_forest.pkl
→ label_encoders.pkl
→ feature_cols.pkl

### Entraîner le modèle

```bash
# Après avoir importé des données OULAD via POST /api/import/students/
python manage.py train_model
```

Résultat attendu :
[ 1/5 ] Extraction des features depuis la DB...
[ 2/5 ] Prétraitement des données...
[ 3/5 ] Entraînement Random Forest...
[ 4/5 ] Évaluation...
[ 5/5 ] Sauvegarde du modèle...
Accuracy : 0.82 | F1 : 0.81 | CV F1 : 0.80 ± 0.02

---

## 🎨 Installation — Frontend (Membre 2)

> ⚠️ **Le backend doit tourner sur http://127.0.0.1:8000 avant de démarrer le frontend.**

### Prérequis
- Node.js 18+
- npm ou yarn

### Étapes

```bash
# 1. Se placer dans le dossier frontend (à créer)
cd frontend

# 2. Installer les dépendances
npm install

# 3. Lancer le serveur de développement
npm run dev
# ou
npm start
```

L'application React sera accessible sur **http://localhost:3000**

### Pages à développer

| Page | Route | Données API à consommer |
|------|-------|------------------------|
| Dashboard | `/` | `/api/analytics/stats/` + `/api/analytics/by-module/` |
| Import données | `/import` | `POST /api/import/students/` |
| Liste étudiants | `/students` | `/api/students/` |
| Profil étudiant | `/students/:id` | `/api/analytics/students/:id/profile/` |
| Étudiants à risque | `/at-risk` | `/api/students/at-risk/` |
| Prédictions | `/predictions` | `POST /api/ml/predict/:id/` |

### Configuration Axios (à créer dans `src/api/axios.js`)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

### Librairies recommandées

```bash
npm install axios recharts react-router-dom @mui/material @emotion/react
```

| Librairie | Usage |
|-----------|-------|
| `axios` | Appels API vers Django |
| `recharts` | Graphiques (barres, camembert, courbes) |
| `react-router-dom` | Navigation entre les pages |
| `@mui/material` | Composants UI (tableaux, cards, badges) |

---

## 📊 Exemple de réponse API — Prédiction

```json
POST /api/ml/predict/11391/

{
  "student_id": 11391,
  "result": "Pass",
  "probability": 0.7823,
  "risk_level": "LOW",
  "shap_values": {
    "avg_score": 0.1842,
    "total_clicks": 0.1203,
    "studied_credits": 0.0891,
    "nb_assessments": 0.0654,
    "num_prev_attempts": -0.0432
  }
}
```

**Interprétation des `shap_values` pour le frontend :**
- Valeur **positive** → pousse vers la réussite
- Valeur **négative** → pousse vers l'échec
- Plus la valeur absolue est grande → plus la feature est influente

---

## 🗓️ Deadline

**02/06/2026 à 23h59** — Dépôt sur Google Classroom

### Checklist finale
- [ ] Dépôt GitHub **public**
- [ ] Commits individuels des deux membres (vérifiés par l'enseignant)
- [ ] Rapport PDF déposé
- [ ] Présentation PPT déposée
- [ ] Vidéo démo (max 15 min) déposée
- [ ] Code source complet sur GitHub

---

## 📁 Dataset OULAD

Téléchargez le dataset sur : https://analyse.kmi.open.ac.uk/open_dataset

Fichiers nécessaires pour l'import :
- `studentInfo.csv` → données démographiques étudiants
- `studentAssessment.csv` → notes et évaluations
- `studentVle.csv` → activité sur la plateforme VLE

---

*Projet réalisé dans le cadre du Master SDIA — Technologies Web · 2025/2026*
