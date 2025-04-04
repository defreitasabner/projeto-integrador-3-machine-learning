import os

from sistema_antifraude import config


def baixar_dados_externos_kaggle(
    kaggle_username_dataset: str, 
    file_name: str = None, 
    dest_path: str = os.path.join(config.DATA_PATH, 'external')
) -> None:
    """
        Baixa os dados de um dataset do Kaggle para `data/external` por padrão. Caso o parâmetro `file_name` seja passado,
        será baixado o único arquivo correspondente ao nome especificado. Caso contrário, todos os arquivos serão baixados.
    """
    if dest_path and not os.path.exists(dest_path):
        raise FileNotFoundError(f"""Diretório {dest_path} não encontrado.""")
    if not os.path.exists(os.path.join(config.CREDENTIALS_PATH, 'kaggle.json')):
        if not os.path.exists(config.CREDENTIALS_PATH):
            os.mkdir(config.CREDENTIALS_PATH)
        raise FileNotFoundError(f"""
            Credenciais não encontradas.
            Por favor, adicione o arquivo kaggle.json em {config.CREDENTIALS_PATH}
        """)
    os.environ['KAGGLE_CONFIG_DIR'] = config.CREDENTIALS_PATH
    os.environ.get('KAGGLE_CONFIG_DIR')
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    if file_name:
        api.dataset_download_file(
            kaggle_username_dataset, 
            file_name, 
            path = os.path.join(dest_path)
        )
    else:
        api.dataset_download_files(
            kaggle_username_dataset, 
            path = os.path.join(dest_path), 
            unzip = True
        )