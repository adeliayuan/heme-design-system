from sklearn.ensemble import ExtraTreesClassifier


def build_model(
    n_estimators,
    max_depth,
    min_samples_split,
    min_samples_leaf,
    max_features
):
    """
    Membangun model Extremely Randomized Trees
    berdasarkan hyperparameter yang diberikan user.
    """

    model = ExtraTreesClassifier(
        n_estimators=int(n_estimators),
        max_depth=int(max_depth),
        min_samples_split=int(min_samples_split),
        min_samples_leaf=int(min_samples_leaf),
        max_features=float(max_features),
        random_state=42,
        n_jobs=-1
    )

    return model
