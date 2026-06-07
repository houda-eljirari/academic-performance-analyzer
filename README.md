# AcademiX : Academic Performance Analyzer

Application web intelligente d'analyse de performance académique développée dans le cadre du module **Technologies du Web et Web Sémantique** Filiére **SDIA — Systèmes Distribués et Intelligence Artificielle** 
## Présentation

AcademiX est une plateforme web full-stack dédiée à l'analyse et à la prédiction des performances académiques des étudiants à partir du dataset **OULAD** (Open University Learning Analytics Dataset). Elle combine des visualisations analytiques interactives, un modèle de Machine Learning XGBoost et une explicabilité SHAP pour identifier les étudiants à risque et générer des recommandations personnalisées.

---

## Fonctionnalités

- Import et gestion des données CSV (dataset OULAD)
- Tableau de bord analytique connecté aux données réelles (28 785 étudiants)
- Consultation et recherche des profils étudiants
- Gestion des notes avec calcul automatique des moyennes
- Prédiction réussite/échec via modèle XGBoost (accuracy 89.06%)
- Visualisation SHAP des facteurs d'influence par étudiant
- Détection automatique des étudiants à risque (LOW / MEDIUM / HIGH)
- Centre d'alertes connecté aux vraies données OULAD

---

## Dataset OULAD

Téléchargez le dataset sur Kaggle : [Open University Learning Analytics Dataset](https://www.kaggle.com/code/vjcalling/oulad-open-university-learning-analytics-dataset)

Fichiers utilisés :

| Fichier | Contenu | Utilisation |
|---|---|---|
| studentInfo.csv | Données démographiques (32 593 étudiants) | Import principal |
| studentAssessment.csv | Scores aux évaluations (173 912 entrées) | Features ML |
| studentVle.csv | Activité plateforme VLE | Engagement étudiant |

---
## Installation et lancement local

### Prérequis

- Python 3.11 ou supérieur
- Node.js 18 ou supérieur
- npm
- Git

---

### Cloner le dépôt

```bash
git clone https://github.com/houda-eljirari/academic-performance-analyzer.git
cd academic-performance-analyzer
```

---

### Backend Django

**1. Créer et activer l'environnement virtuel**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Créer le fichier `.env` à la racine**

```
SECRET_KEY=votre-cle-secrete-ici
DEBUG=True
```

**4. Appliquer les migrations**

```bash
python manage.py migrate
```

**5. Créer un superutilisateur (optionnel)**

```bash
python manage.py createsuperuser
```

**6. Lancer le serveur Django**

```bash
python manage.py runserver
```

L'API est accessible sur : http://127.0.0.1:8000/api/

---

### Import des données OULAD

Une fois le serveur lancé, importez les données via Postman ou curl :

```bash
# Import des étudiants
curl -X POST http://127.0.0.1:8000/api/import/students/ \
  -F "file=@studentInfo.csv"

# Import des évaluations
curl -X POST http://127.0.0.1:8000/api/import/assessments/ \
  -F "file=@studentAssessment.csv"
```

---

### Entraînement du modèle ML

Après l'import des données, entraînez le modèle XGBoost :

```bash
python manage.py train_model
```

Résultat attendu :

```
Algorithme : XGBoost
Accuracy   : 0.8906
F1 Score   : 0.8903
CV F1      : 0.8159 +/- 0.0575
```

Les fichiers du modèle sont sauvegardés dans `ml_models/saved_models/`.

---

### Générer les visualisations ML

```bash
python manage.py generate_viz
```

Les graphiques sont sauvegardés dans `ml_models/visualizations/`.

---

### Frontend Angular

**1. Aller dans le dossier frontend**

```bash
cd academic-frontend
```

**2. Installer les dépendances**

```bash
npm install
```

**3. Lancer le serveur Angular**

```bash
ng serve --port 4300
```

L'application est accessible sur : http://localhost:4300

Identifiants de test : `admin@test.com` / `1234`

---

### Lancer les deux serveurs simultanément

Ouvrez deux terminaux :

```bash
# Terminal 1 — Backend
cd academic-performance-analyzer
venv\Scripts\activate   # ou source venv/bin/activate sur Mac/Linux
python manage.py runserver

# Terminal 2 — Frontend
cd academic-performance-analyzer/academic-frontend
ng serve --port 4300
```

---

## Architecture technique

``` bash
academic-performance-analyzer/
├── config/                  Django — configuration, settings, urls
├── students/                Modèles OULAD, CRUD, import CSV
├── analytics/               Endpoints statistiques et alertes
├── predictions/             Stockage prédictions et recommandations
├── ml_models/               Pipeline ML — XGBoost, SHAP, joblib
│   ├── feature_engineering.py
│   ├── train.py
│   ├── predictor.py
│   ├── generate_visualizations.py
│   └── management/commands/train_model.py
├── manage.py
├── requirements.txt
└── academic-frontend/       Angular 21 — SPA frontend
    └── src/app/
        ├── core/services/   ApiService, AuthService
        └── pages/           Dashboard, Students, Grades, Predictions,
                             Alerts, SHAP, CsvImport, StudentProfile
```

---

## Résultats du modèle ML

| Métrique | Valeur |
|---|---|
| Algorithme | XGBoost |
| Dataset | 28 785 étudiants OULAD |
| Accuracy | 0.8906 (89.06%) |
| F1-Score | 0.8903 |
| Precision | 0.8939 |
| Recall | 0.8906 |
| CV F1 (5-fold) | 0.8159 +/- 0.0575 |
| Features | 22 (démographiques, assessment, VLE) |

---

### Équipe

| Membre | Rôle | Responsabilités |
|---|---|---|
| EL JIRARI Houda | Backend et Intelligence Artificielle | Django REST API, Pipeline ML, SHAP, Import OULAD |
| EL BARNAOUI Maroua | Frontend et Visualisations | Angular, Dashboard, Visualisation SHAP |


