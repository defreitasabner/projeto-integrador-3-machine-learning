from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def calcular_metricas(y_real, y_predito) -> dict[str, float]:
    acuracia = accuracy_score(y_real, y_predito)
    precisao = precision_score(y_real, y_predito)
    recall = recall_score(y_real, y_predito)
    f1 = f1_score(y_real, y_predito)
    return {
        "acuracia": acuracia,
        "precisao": precisao,
        "recall": recall,
        "f1": f1
    }