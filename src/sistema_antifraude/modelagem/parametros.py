class ParametrosArvoreDecisao(object):
    
    DEFAULT = {
        'max_depth': 3,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
    }

class ParametrosRegressaoLogistica(object):

    DEFAULT = {
        'max_iter': 800,
        'solver': 'lbfgs',
    }