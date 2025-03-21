import os
import pytest

from src.datasets import baixar_dados_externos_kaggle
from src import config


class TestDatasets:

    @pytest.mark.teste_integracao
    def test_sucesso_ao_baixar_dados_externos_do_kaggle_apenas_arquivo_especifico(
        self, 
        diretorio_teste_temporario
    ):
        dataset = 'uciml/iris'
        file_name = 'iris.csv'
        path_dir_test = diretorio_teste_temporario()
        baixar_dados_externos_kaggle(dataset, file_name, path_dir_test)
        arquivo_foi_baixado = os.path.exists(os.path.join(path_dir_test, file_name))
        assert arquivo_foi_baixado

    @pytest.mark.teste_integracao
    def test_falha_ao_baixar_dados_externos_do_kaggle_em_diretorio_inexistente(self):
        dataset = 'uciml/iris'
        file_name = 'iris.csv'
        path_inexistente = 'inexistente'
        with pytest.raises(FileNotFoundError):
            baixar_dados_externos_kaggle(dataset, file_name, path_inexistente)

    @pytest.mark.teste_integracao
    def test_falha_ao_tentar_baixar_dados_inexistentes_do_kaggle(self, diretorio_teste_temporario):
        dataset = 'uciml/iris'
        file_name = 'nao_existe.csv'
        path_dir_test = diretorio_teste_temporario()
        with pytest.raises(Exception):
            baixar_dados_externos_kaggle(dataset, file_name, path_dir_test)