import numpy as np
from sklearn.ensemble import ExtraTreesClassifier


# BEST PARAMETERS (HASIL APSO)

def get_best_params():

    return {
        "n_estimators": 487,
        "max_depth": 65,
        "min_samples_split": 22,
        "min_samples_leaf": 8,
        "max_features": 0.42
    }


# BUILD MODEL

def build_model():

    params = get_best_params()

    model = ExtraTreesClassifier(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        min_samples_split=params["min_samples_split"],
        min_samples_leaf=params["min_samples_leaf"],
        max_features=params["max_features"],
        random_state=42,
        n_jobs=-1
    )

    return model