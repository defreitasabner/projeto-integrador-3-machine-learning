import random
from datetime import datetime, timedelta
from typing import Any

from src.gerador_dados.componentes.dado_gerado import DadoGerado
from src.gerador_dados.componentes.gerador_dados_legitimos import GeradorDadosLegitimos
from src.gerador_dados.componentes.gerador_dados_fraudados import GeradorDadosFraudados


class Gerador:
    def __init__(self):
        pass

    def gerar_dados(
        self, 
        qtd_usuarios = 500,
        media_acessos_por_dia = 1000,
        data_inicial = datetime.now() - timedelta(days = 30), 
        data_final = datetime.now(),
        pct_min_acessos_por_dia = 0.25,
        pct_max_acessos_por_dia = 1.0,
        pct_fraude = 0.01
    ) -> list[dict[str, Any]]:
        self.__validar_datas(data_inicial, data_final)
        self.__validar_porcentagem(pct_min_acessos_por_dia)
        self.__validar_porcentagem(pct_max_acessos_por_dia)
        self.__validar_porcentagem(pct_fraude)
        data_inicial = data_inicial.replace(hour = 0, minute = 0, second = 0)
        variacao_dias = (data_final - data_inicial).days + 1
        qtd_min_acessos_por_dia = int(media_acessos_por_dia * pct_min_acessos_por_dia)
        qtd_max_acessos_por_dia = int(media_acessos_por_dia * pct_max_acessos_por_dia)
        gerador_legitimo = GeradorDadosLegitimos(qtd_usuarios)
        dados_gerados: list[DadoGerado] = []
        for i in range(variacao_dias):
            dia_atual = data_inicial + timedelta(days = i)
            qtd_acessos_do_dia = random.randint(qtd_min_acessos_por_dia, qtd_max_acessos_por_dia)
            dados_legitimos_do_dia = gerador_legitimo.gerar_dados_legitimos(qtd_acessos_do_dia, dia_atual)
            dados_legitimos_do_dia = map(lambda dado_legitimo: DadoGerado.from_dict(dado_legitimo), dados_legitimos_do_dia)
            dados_gerados.extend(dados_legitimos_do_dia)
        dados_gerados = GeradorDadosFraudados(pct_fraude).gerar_fraudes(dados_gerados)
        return list(map(lambda dado_gerado: dado_gerado.to_dict(), dados_gerados))

    def __validar_datas(self, data_inicial, data_final):
        if data_inicial > data_final:
            raise ValueError('Data inicial não pode ser maior que a data final.')

    def __validar_porcentagem(self, porcentagem):
        if porcentagem < 0 or porcentagem > 1:
            raise ValueError('Porcentagens devem estar entre 0 e 1.')
