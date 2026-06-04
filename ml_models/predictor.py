# ml_models/predictor.py
import joblib
from django.conf import settings

MODELS_DIR = settings.ML_MODELS_DIR

_model          = None
_label_encoders = None
_feature_cols   = None


def load_model():
    global _model, _label_encoders, _feature_cols

    # Essayer best_model.pkl d'abord, sinon random_forest.pkl
    model_path = MODELS_DIR / 'best_model.pkl'
    if not model_path.exists():
        model_path = MODELS_DIR / 'random_forest.pkl'
    if not model_path.exists():
        raise FileNotFoundError(
            "Modèle introuvable. Lancez : python manage.py train_model"
        )

    _model          = joblib.load(model_path)
    _label_encoders = joblib.load(MODELS_DIR / 'label_encoders.pkl')
    _feature_cols   = joblib.load(MODELS_DIR / 'feature_cols.pkl')

    return _model, _label_encoders, _feature_cols


def predict_student(student_id):
    global _model, _label_encoders, _feature_cols

    if _model is None:
        load_model()

    from .feature_engineering import extract_features_for_student
    X_row, error = extract_features_for_student(
        student_id, _label_encoders, _feature_cols
    )
    if error:
        return {'error': error}

    proba      = float(_model.predict_proba(X_row)[0][1])
    result     = 'Pass' if proba >= 0.5 else 'Fail'
    risk_level = 'LOW' if proba >= 0.75 else 'MEDIUM' if proba >= 0.5 else 'HIGH'
    shap_vals  = compute_shap(X_row)

    return {
        'student_id':  student_id,
        'result':      result,
        'probability': round(proba, 4),
        'risk_level':  risk_level,
        'shap_values': shap_vals,
        'algorithm':   type(_model).__name__,
    }


def compute_shap(X_row):
    try:
        import shap
        explainer = shap.TreeExplainer(_model)
        shap_vals = explainer.shap_values(X_row)
        if isinstance(shap_vals, list):
            vals = shap_vals[1][0]
        else:
            vals = shap_vals[0]
        result = {
            col: round(float(v), 4)
            for col, v in zip(_feature_cols, vals)
        }
        return dict(sorted(result.items(), key=lambda x: abs(x[1]), reverse=True))
    except Exception as e:
        return {'error': str(e)}


def get_model_info():
    global _model, _feature_cols
    if _model is None:
        try:
            load_model()
        except FileNotFoundError:
            return {'status': 'not_trained'}
    return {
        'status':        'loaded',
        'algorithm':     type(_model).__name__,
        'n_features':    len(_feature_cols),
        'feature_names': _feature_cols,
    }