import uuid
import random
from datetime import datetime

from faker import Faker

from sistema_antifraude.gerador_dados.defaults import horarios


class GeradorDadosLegitimos:
    def __init__(
        self, 
        qtd_usuarios = 100, 
        prob_novo_device = 0.01, 
        prob_novo_ip = 0.1, 
        prob_nova_lat_long = 0.25,
        prob_acesso_madrugada = 0.01,
        prob_acesso_manha = 0.1,
        prob_acesso_noturno = 0.15,
    ):
        self.__faker = Faker()
        # Informações dos usuários
        self.__user_ids = [uuid.uuid4().hex for _ in range(qtd_usuarios)]
        self.__devices_por_usuarios = { user_id: [uuid.uuid4().hex] for user_id in self.__user_ids }
        self.__ips_por_usuarios = { user_id: [self.__faker.unique.ipv4_public()] for user_id in self.__user_ids }
        self.__lat_long_por_usuarios = { 
            user_id: [self.__faker.local_latlng(country_code = 'BR', coords_only = True)] 
                for user_id in self.__user_ids 
        }
        # Probabilidades
        self.__prob_novo_device = prob_novo_device
        self.__prob_novo_ip = prob_novo_ip
        self.__prob_nova_localizacao = prob_nova_lat_long
        self.__prob_acesso_madrugada = prob_acesso_madrugada
        self.__prob_acesso_manha = prob_acesso_manha + self.__prob_acesso_madrugada
        self.__prob_acesso_noturno = prob_acesso_noturno + self.__prob_acesso_madrugada + self.__prob_acesso_manha

    @property
    def user_ids(self):
        """Retorna a lista de user_ids."""
        return self.__user_ids
    
    def gerar_dado_legitimo(self, data_inicio: datetime) -> dict:
        """Gera um usuário com base nas regras."""
        user_id = random.choice(self.__user_ids)
        latitude, longitude = self.__obter_lat_long(user_id)
        return {
            "user_id": user_id,
            "device_id": self.__obter_device(user_id),
            "ipv4": self.__obter_ip(user_id),
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": self.__obter_timestamp(data_inicio),
            "is_fraude": False
        }

    def gerar_dados_legitimos(self, quantidade: int, data_inicio: datetime) -> list:
        """Gera uma lista de usuários com base nas regras."""
        return [self.gerar_dado_legitimo(data_inicio) for _ in range(quantidade)]

    def __obter_device(self, user_id: str):
        """Gera um novo device ou retorna um padrão."""
        if random.random() <= self.__prob_novo_device:
            novo_device = uuid.uuid4().hex
            self.__devices_por_usuarios[user_id].append(novo_device)
            return novo_device
        return random.choice(self.__devices_por_usuarios[user_id])

    def __obter_ip(self, user_id):
        """Gera um novo IP ou retorna um padrão."""
        if random.random() <= self.__prob_novo_ip:
            novo_ip = self.__faker.unique.ipv4_public()
            self.__ips_por_usuarios[user_id].append(novo_ip)
            return novo_ip
        return random.choice(self.__ips_por_usuarios[user_id])

    def __obter_lat_long(self, user_id):
        """Gera uma nova localização ou retorna uma padrão."""
        if random.random() <= self.__prob_nova_localizacao:
            nova_localizacao = self.__faker.local_latlng(coords_only = True)
            self.__lat_long_por_usuarios[user_id].append(nova_localizacao)
            return nova_localizacao
        return random.choice(self.__lat_long_por_usuarios[user_id])

    def __obter_timestamp(self, data_inicio: datetime) -> datetime:
        """Gera um horário baseado nas probabilidades."""
        probabilidade = random.random()
        if probabilidade <= self.__prob_acesso_madrugada:
            return self.__faker.date_time_between_dates(
                datetime_start = data_inicio,
                datetime_end = data_inicio.replace(**horarios.HORARIO_MADRUGADA_FIM)
            )
        elif probabilidade <= self.__prob_acesso_manha:
            return self.__faker.date_time_between_dates(
                datetime_start = data_inicio.replace(**horarios.HORARIO_MADRUGADA_FIM),
                datetime_end = data_inicio.replace(**horarios.HORARIO_PICO_INICIO)
            )
        elif probabilidade <= self.__prob_acesso_noturno:
            return self.__faker.date_time_between_dates(
                datetime_start = data_inicio.replace(**horarios.HORARIO_PICO_FIM),
                datetime_end = data_inicio.replace(**horarios.HORARIO_NOTURNO_FIM)
            )
        else:
            return self.__faker.date_time_between_dates(
                datetime_start = data_inicio.replace(**horarios.HORARIO_PICO_INICIO),
                datetime_end = data_inicio.replace(**horarios.HORARIO_PICO_FIM)
            )