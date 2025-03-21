import pytest


@pytest.fixture(scope='function')
def diretorio_teste_temporario(tmp_path_factory):
    def gerar_diretorio_teste_temporario(dir_name = 'tmp_test'):
        path = tmp_path_factory.mktemp(dir_name)
        return path
    return gerar_diretorio_teste_temporario