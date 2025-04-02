import random
import uuid
from datetime import datetime

from faker import Faker

from src.gerador_dados.componentes.dado_gerado import DadoGerado


class GeradorDadosFraudados:
    def __init__(self, pct_fraude: float):
        self.__pct_fraude = pct_fraude
        self.__idx_fraudados = []
    
    def gerar_fraudes(self, dados_legitimos: list[DadoGerado]) -> list[DadoGerado]:
        qtd_fraudes = int(len(dados_legitimos) * self.__pct_fraude)
        for i in range(qtd_fraudes):
            idx_aleatorio = random.randint(0, len(dados_legitimos) - 1)
            while idx_aleatorio in self.__idx_fraudados:
                idx_aleatorio = random.randint(0, len(dados_legitimos) - 1)
            self.__idx_fraudados.append(idx_aleatorio)
            dados_legitimos[idx_aleatorio] = self.__gerar_fraude(dados_legitimos[idx_aleatorio])
        return dados_legitimos
    
    def __gerar_fraude(self, dado_legitimo: DadoGerado) -> DadoGerado:
        return self.fraude_padrao(dado_legitimo)
    
    def fraude_padrao(self, dado_legitimo: DadoGerado) -> DadoGerado:
        """Fraude padrão: troca de device_id, ipv4, localização e horário da madrugada (alta probabilidade)."""
        device_id_fraude = uuid.uuid4().hex
        ipv4_fraude = Faker().unique.ipv4_public()
        latitude_fraude, longitude_fraude = self.__localizacao_fraude()
        horario_fraude = self.__horario_fraude(dado_legitimo.timestamp)
        return DadoGerado(
            user_id = dado_legitimo.user_id,
            device_id = device_id_fraude,
            ipv4 = ipv4_fraude,
            latitude = latitude_fraude,
            longitude = longitude_fraude,
            timestamp = horario_fraude,
            is_fraude = True
        )
    
    def fraude_invasao(self, dado_legitimo: DadoGerado) -> DadoGerado:
        """Fraude de invasão: mesmo device_id, ipv4 e localização, mas horário madrugada."""
        horario_fraude = self.__horario_fraude(dado_legitimo.timestamp, prob_madrugada = 1.0)
        return DadoGerado(
            user_id = dado_legitimo.user_id,
            device_id = dado_legitimo.device_id,
            ipv4 = dado_legitimo.ipv4,
            latitude = dado_legitimo.latitude,
            longitude = dado_legitimo.longitude,
            timestamp = horario_fraude,
            is_fraude = True
        )

    def __horario_fraude(self, data_inicio: datetime, prob_madrugada = 0.90) -> datetime:
        if random.random() <= prob_madrugada:
            return Faker().date_time_between_dates(
                datetime_start = data_inicio.replace(hour = 0, minute = 0, second = 0),
                datetime_end = data_inicio.replace(hour = 4, minute = 59, second = 59)
            )
        else:
            return Faker().date_time_between_dates(
                datetime_start = data_inicio.replace(hour = 5, minute = 0, second = 0),
                datetime_end = data_inicio.replace(hour = 23, minute = 59, second = 59)
            )
        
    def __localizacao_fraude(self) -> tuple[float, float]:
        return Faker().local_latlng(coords_only = True)