# predictions/recommendations.py
"""
Moteur de recommandations personnalisées basé sur les valeurs SHAP.
Chaque règle analyse les features les plus négatives et génère
une recommandation ciblée.
"""


RECOMMENDATIONS_RULES = [
    {
        'feature':    'total_clicks',
        'condition':  lambda v: v < -0.05,
        'type':       'Engagement',
        'priority':   1,
        'content':    "Votre engagement sur la plateforme VLE est insuffisant. "
                      "Essayez de vous connecter au moins 3 fois par semaine et "
                      "d'interagir avec les ressources du cours (vidéos, quiz, forums).",
    },
    {
        'feature':    'avg_score',
        'condition':  lambda v: v < -0.05,
        'type':       'Évaluation',
        'priority':   1,
        'content':    "Votre moyenne aux évaluations est en dessous du seuil de réussite. "
                      "Consacrez plus de temps à la révision avant chaque TMA et CMA. "
                      "N'hésitez pas à revoir les modules précédents.",
    },
    {
        'feature':    'nb_assessments',
        'condition':  lambda v: v < -0.04,
        'type':       'Assiduité',
        'priority':   2,
        'content':    "Vous n'avez pas soumis toutes vos évaluations. "
                      "Chaque évaluation non soumise pèse lourdement sur votre résultat final. "
                      "Contactez votre tuteur si vous rencontrez des difficultés.",
    },
    {
        'feature':    'nb_vle_days',
        'condition':  lambda v: v < -0.04,
        'type':       'Régularité',
        'priority':   2,
        'content':    "Votre activité sur la plateforme est trop irrégulière. "
                      "Établissez un planning de travail hebdomadaire fixe "
                      "et respectez-le pour maintenir un rythme d'apprentissage stable.",
    },
    {
        'feature':    'num_prev_attempts',
        'condition':  lambda v: v < -0.03,
        'type':       'Historique',
        'priority':   3,
        'content':    "Votre historique de tentatives précédentes impacte votre prédiction. "
                      "Identifiez les raisons de vos difficultés passées et mettez en place "
                      "un plan d'action concret avec votre tuteur.",
    },
    {
        'feature':    'studied_credits',
        'condition':  lambda v: v < -0.03,
        'type':       'Charge académique',
        'priority':   3,
        'content':    "Votre charge de crédits semble impacter votre performance. "
                      "Envisagez de discuter avec votre conseiller académique "
                      "pour ajuster votre parcours si nécessaire.",
    },
    {
        'feature':    'nb_vle_types',
        'condition':  lambda v: v < -0.02,
        'type':       'Diversification',
        'priority':   4,
        'content':    "Vous n'exploitez pas toute la diversité des ressources disponibles. "
                      "Utilisez les forums, wikis, quiz interactifs et vidéos "
                      "pour enrichir votre expérience d'apprentissage.",
    },
]

DEFAULT_RECOMMENDATION = {
    'type':     'Général',
    'priority': 5,
    'content':  "Continuez à maintenir votre rythme de travail. "
                "Restez régulier dans vos connexions à la plateforme "
                "et n'hésitez pas à solliciter votre tuteur en cas de doute.",
}


def generate_recommendations(shap_values: dict, risk_level: str) -> list:
    """
    Génère une liste de recommandations personnalisées
    basées sur les valeurs SHAP d'un étudiant.
    """
    recommendations = []

    for rule in RECOMMENDATIONS_RULES:
        feature = rule['feature']
        value   = shap_values.get(feature, 0)

        if not isinstance(value, (int, float)):
            continue

        if rule['condition'](value):
            recommendations.append({
                'type':     rule['type'],
                'priority': rule['priority'],
                'content':  rule['content'],
                'feature':  feature,
                'impact':   round(value, 4),
            })

    # Trier par priorité
    recommendations.sort(key=lambda x: x['priority'])

    # Si aucune recommandation spécifique → recommandation générale
    if not recommendations:
        recommendations.append(DEFAULT_RECOMMENDATION)

    # Ajouter une recommandation urgente si risque élevé
    if risk_level == 'HIGH':
        recommendations.insert(0, {
            'type':     'URGENT',
            'priority': 0,
            'content':  "⚠️ Votre profil indique un risque élevé d'échec. "
                        "Contactez immédiatement votre tuteur pour mettre en place "
                        "un plan de soutien personnalisé. Ne tardez pas à agir.",
            'feature':  None,
            'impact':   None,
        })

    return recommendations[:6]  # Max 6 recommandations