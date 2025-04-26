import os
from pathlib import Path


BASE_ROOT_PATH = str(Path(os.path.abspath(__file__)).parent.parent.parent)
DATA_PATH = os.path.join(BASE_ROOT_PATH, 'data')
CREDENTIALS_PATH = os.path.join(BASE_ROOT_PATH, 'credentials')
MODELS_PATH = os.path.join(BASE_ROOT_PATH, 'models')
PLOTS_PATH = os.path.join(BASE_ROOT_PATH, 'plots')

CACHE_DIR_PATH = os.path.join(os.getcwd(), '.sistema_antifraude_cache')

def criar_diretorio_cache(path = CACHE_DIR_PATH):
    os.makedirs(path, exist_ok = True)