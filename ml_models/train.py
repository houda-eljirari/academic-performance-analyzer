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
    import os
    import joblib
    import numpy as np
    from django.conf import settings
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.metrics import (
        accuracy_score, f1_score, precision_score,
        recall_score, confusion_matrix, classification_report
    )
    from xgboost import XGBClassifier
    from .feature_engineering import extract_features_from_db, preprocess

    MODELS_DIR = settings.ML_MODELS_DIR

    print("[ 1/6 ] Extraction des features depuis la DB...")
    df = extract_features_from_db()

    if df.empty or len(df) < 20:
        return {'error': 'Pas assez de données.'}

    print(f"         {len(df)} étudiants · {len(df.columns)-2} features")

    print("[ 2/6 ] Prétraitement...")
    X, y, label_encoders, feature_cols = preprocess(df, fit=True)
    print(f"         Distribution : {y.value_counts().to_dict()}")
    print(f"         Features utilisées ({len(feature_cols)}) : {feature_cols}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── Entraîner Random Forest ──────────────────────────
    print("[ 3/6 ] Entraînement Random Forest...")
    rf_params = {
        'n_estimators':      [100, 200, 300],
        'max_depth':         [10, 20, None],
        'min_samples_split': [2, 5],
        'max_features':      ['sqrt', 'log2'],
    }
    rf = RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1)
    rf_grid = GridSearchCV(rf, rf_params, cv=3, scoring='f1_weighted', n_jobs=-1)
    rf_grid.fit(X_train, y_train)
    best_rf = rf_grid.best_estimator_

    # ── Entraîner XGBoost ────────────────────────────────
    print("[ 4/6 ] Entraînement XGBoost...")
    xgb_params = {
        'n_estimators':  [100, 200, 300],
        'max_depth':     [4, 6, 8],
        'learning_rate': [0.05, 0.1, 0.2],
        'subsample':     [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
    }
    xgb = XGBClassifier(
        random_state=42,
        eval_metric='logloss',
        use_label_encoder=False,
        n_jobs=-1,
    )
    xgb_grid = GridSearchCV(xgb, xgb_params, cv=3, scoring='f1_weighted', n_jobs=-1)
    xgb_grid.fit(X_train, y_train)
    best_xgb = xgb_grid.best_estimator_

    # ── Comparer et choisir le meilleur ─────────────────
    print("[ 5/6 ] Comparaison des modèles...")
    rf_f1  = f1_score(y_test, best_rf.predict(X_test),  average='weighted')
    xgb_f1 = f1_score(y_test, best_xgb.predict(X_test), average='weighted')

    print(f"         Random Forest F1  : {rf_f1:.4f}")
    print(f"         XGBoost       F1  : {xgb_f1:.4f}")

    if xgb_f1 >= rf_f1:
        best_model    = best_xgb
        best_algo     = "XGBoost"
        best_params   = xgb_grid.best_params_
    else:
        best_model    = best_rf
        best_algo     = "RandomForest"
        best_params   = rf_grid.best_params_

    print(f"         Meilleur modèle : {best_algo}")

    # ── Évaluation finale ────────────────────────────────
    y_pred    = best_model.predict(X_test)
    y_proba   = best_model.predict_proba(X_test)[:, 1]
    accuracy  = round(accuracy_score(y_test, y_pred), 4)
    f1        = round(f1_score(y_test, y_pred, average='weighted'), 4)
    precision = round(precision_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    recall    = round(recall_score(y_test, y_pred, average='weighted', zero_division=0), 4)
    cm        = confusion_matrix(y_test, y_pred).tolist()
    report    = classification_report(y_test, y_pred, output_dict=True)

    cv_scores = cross_val_score(best_model, X, y, cv=5, scoring='f1_weighted')
    cv_mean   = round(float(cv_scores.mean()), 4)
    cv_std    = round(float(cv_scores.std()), 4)

    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        fi = dict(zip(
            feature_cols,
            [round(float(v), 4) for v in best_model.feature_importances_]
        ))
        fi = dict(sorted(fi.items(), key=lambda x: x[1], reverse=True))
    else:
        fi = {}

    # ── Sauvegarder ──────────────────────────────────────
    print("[ 6/6 ] Sauvegarde...")
    joblib.dump(best_model,     MODELS_DIR / 'best_model.pkl')
    joblib.dump(best_rf,        MODELS_DIR / 'random_forest.pkl')
    joblib.dump(best_xgb,       MODELS_DIR / 'xgboost.pkl')
    joblib.dump(label_encoders, MODELS_DIR / 'label_encoders.pkl')
    joblib.dump(feature_cols,   MODELS_DIR / 'feature_cols.pkl')

    metrics = {
        'algorithm':             best_algo,
        'best_params':           best_params,
        'accuracy':              accuracy,
        'f1_score':              f1,
        'precision':             precision,
        'recall':                recall,
        'cv_mean_f1':            cv_mean,
        'cv_std':                cv_std,
        'confusion_matrix':      cm,
        'classification_report': report,
        'feature_importance':    fi,
        'train_size':            len(X_train),
        'test_size':             len(X_test),
        'n_features':            len(feature_cols),
        'rf_f1':                 round(rf_f1, 4),
        'xgb_f1':                round(xgb_f1, 4),
    }

    print(f"\n {'='*50}")
    print(f" Algorithme : {best_algo}")
    print(f" Accuracy   : {accuracy}")
    print(f" F1 Score   : {f1}")
    print(f" CV F1      : {cv_mean} ± {cv_std}")
    print(f" {'='*50}")

    # Sauvegarder les métriques pour les visualisations
    import joblib
    joblib.dump(metrics, MODELS_DIR / 'last_metrics.pkl')

    return metrics
