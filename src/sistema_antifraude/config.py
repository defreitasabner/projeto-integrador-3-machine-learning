import os
from pathlib import Path


BASE_ROOT_PATH = str(Path(os.path.abspath(__file__)).parent.parent.parent)
DATA_PATH = os.path.join(BASE_ROOT_PATH, 'data')
CREDENTIALS_PATH = os.path.join(BASE_ROOT_PATH, 'credentials')
MODELS_PATH = os.path.join(BASE_ROOT_PATH, 'models')
PLOTS_PATH = os.path.join(BASE_ROOT_PATH, 'plots')