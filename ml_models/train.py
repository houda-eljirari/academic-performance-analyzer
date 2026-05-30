# ml_models/train.py
import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score,
    recall_score, confusion_matrix, classification_report
)
from .feature_engineering import extract_features_from_db, preprocess


MODELS_DIR = settings.ML_MODELS_DIR


def train_and_save():
    """
    Pipeline complet : extraction → preprocessing → entraînement → évaluation → sauvegarde.
    Retourne un dict avec les métriques.
    """
    print("[ 1/5 ] Extraction des features depuis la DB...")
    df = extract_features_from_db()

    if df.empty or len(df) < 20:
        return {'error': 'Pas assez de données pour entraîner le modèle (minimum 20 étudiants).'}

    print(f"         {len(df)} étudiants trouvés.")

    print("[ 2/5 ] Prétraitement des données...")
    X, y, label_encoders, feature_cols = preprocess(df, fit=True)

    print(f"         Distribution : {y.value_counts().to_dict()}")

    print("[ 3/5 ] Entraînement Random Forest...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Recherche hyperparamètres simplifiée
    param_grid = {
        'n_estimators':  [100, 200],
        'max_depth':     [None, 10, 20],
        'min_samples_split': [2, 5],
    }

    rf = RandomForestClassifier(random_state=42, class_weight='balanced')

    grid_search = GridSearchCV(
        rf, param_grid, cv=3,
        scoring='f1_weighted', n_jobs=-1, verbose=0
    )
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    print(f"         Meilleurs params : {grid_search.best_params_}")

    print("[ 4/5 ] Évaluation...")
    y_pred    = best_model.predict(X_test)
    y_proba   = best_model.predict_proba(X_test)[:, 1]

    accuracy  = round(accuracy_score(y_test, y_pred), 4)
    f1        = round(f1_score(y_test, y_pred, average='weighted'), 4)
    precision = round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    recall    = round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    cm        = confusion_matrix(y_test, y_pred).tolist()
    report    = classification_report(y_test, y_pred, output_dict=True)

    cv_scores  = cross_val_score(best_model, X, y, cv=5, scoring='f1_weighted')
    cv_mean    = round(float(cv_scores.mean()), 4)
    cv_std     = round(float(cv_scores.std()), 4)

    feature_importance = dict(zip(
        feature_cols,
        [round(float(v), 4) for v in best_model.feature_importances_]
    ))
    feature_importance = dict(sorted(
        feature_importance.items(), key=lambda x: x[1], reverse=True
    ))

    print("[ 5/5 ] Sauvegarde du modèle...")
    joblib.dump(best_model,     MODELS_DIR / 'random_forest.pkl')
    joblib.dump(label_encoders, MODELS_DIR / 'label_encoders.pkl')
    joblib.dump(feature_cols,   MODELS_DIR / 'feature_cols.pkl')

    metrics = {
        'accuracy':           accuracy,
        'f1_score':           f1,
        'precision':          precision,
        'recall':             recall,
        'cv_mean_f1':         cv_mean,
        'cv_std':             cv_std,
        'confusion_matrix':   cm,
        'classification_report': report,
        'feature_importance': feature_importance,
        'train_size':         len(X_train),
        'test_size':          len(X_test),
        'best_params':        grid_search.best_params_,
    }

    print(f"\n Accuracy : {accuracy} | F1 : {f1} | CV F1 : {cv_mean} ± {cv_std}")
    return metrics