from datetime import datetime
import uuid

from faker import Faker

from src.gerador_dados.componentes.dado_gerado import DadoGerado
from src.gerador_dados.componentes.gerador_dados_legitimos import GeradorDadosLegitimos
from src.gerador_dados.componentes.gerador_dados_fraudados import GeradorDadosFraudados


class TestDadoGerado:
    def test_dado_gerado_instanciado_com_sucesso(self):
        # Parâmetros
        user_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ipv4 = Faker().unique.ipv4()
        latitude, longitude = Faker().local_latlng(coords_only = True)
        timestamp = Faker().date_time()
        is_fraude = False
        # Execução
        dado_gerado = DadoGerado(
            user_id = user_id,
            device_id = device_id,
            ipv4 = ipv4,
            latitude = latitude,
            longitude = longitude,
            timestamp = timestamp,
            is_fraude = is_fraude
        )
        # Verificação
        assert dado_gerado.user_id == user_id
        assert dado_gerado.device_id == device_id
        assert dado_gerado.ipv4 == ipv4
        assert dado_gerado.latitude == latitude
        assert dado_gerado.longitude == longitude
        assert dado_gerado.timestamp == timestamp
        assert dado_gerado.is_fraude == is_fraude

    def test_dado_gerado_to_dict_com_sucesso(self):
        # Parâmetros
        user_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ipv4 = Faker().unique.ipv4()
        latitude, longitude = Faker().local_latlng(coords_only = True)
        timestamp = Faker().date_time()
        is_fraude = False
        # Execução
        dado_gerado = DadoGerado(
            user_id = user_id,
            device_id = device_id,
            ipv4 = ipv4,
            latitude = latitude,
            longitude = longitude,
            timestamp = timestamp,
            is_fraude = is_fraude
        )
        # Verificação
        dados_dict = dado_gerado.to_dict()
        assert dados_dict["user_id"] == user_id
        assert dados_dict["device_id"] == device_id
        assert dados_dict["ipv4"] == ipv4
        assert dados_dict["latitude"] == latitude
        assert dados_dict["longitude"] == longitude
        assert dados_dict["timestamp"] == timestamp.isoformat()
        assert dados_dict["is_fraude"] == is_fraude

    def test_dado_gerado_from_dict_com_sucesso(self):
        # Parâmetros
        user_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ipv4 = Faker().unique.ipv4()
        latitude, longitude = Faker().local_latlng(coords_only = True)
        timestamp = Faker().date_time()
        is_fraude = False
        dados_dict = {
            "user_id": user_id,
            "device_id": device_id,
            "ipv4": ipv4,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp.isoformat(),
            "is_fraude": is_fraude
        }
        # Execução
        dado_gerado = DadoGerado.from_dict(dados_dict)
        # Verificação
        assert dado_gerado.user_id == user_id
        assert dado_gerado.device_id == device_id
        assert dado_gerado.ipv4 == ipv4
        assert dado_gerado.latitude == latitude
        assert dado_gerado.longitude == longitude
        assert dado_gerado.timestamp == timestamp
        assert dado_gerado.is_fraude == is_fraude

class TestGeradorDadosLegitimos:
    def test_gerador_dados_legitimos_gerando_quantidades_e_timestamps_corretos(self):
        # Parâmetros
        qtd_usuarios = 10
        qtd_dados_gerados = 30
        data_inicio = datetime.now().replace(hour = 0, minute = 0, second = 0)
        # Execução
        gerador_dados_legitimos = GeradorDadosLegitimos(qtd_usuarios)
        dados_gerados = gerador_dados_legitimos.gerar_dados_legitimos(qtd_dados_gerados, data_inicio)
        # Verificação
        timestamp_min_gerada = min(dado["timestamp"] for dado in dados_gerados)
        timestamp_max_gerada = max(dado["timestamp"] for dado in dados_gerados)
        assert len(gerador_dados_legitimos.user_ids) == qtd_usuarios
        assert len(dados_gerados) == qtd_dados_gerados
        assert data_inicio.date() == timestamp_min_gerada.date()
        assert data_inicio.date() == timestamp_max_gerada.date()

class TestGeradorDadosFraudados:
    def test_gerador_dados_fraudados_gerando_quantidade_correta(self):
        # Parâmetros
        qtd_dados_legitimos = 137
        pct_fraude = 0.01
        data_inicio = datetime.now().replace(hour = 0, minute = 0, second = 0)
        dados_legitimos_dict = GeradorDadosLegitimos().gerar_dados_legitimos(qtd_dados_legitimos, data_inicio)
        dados_legitimos = [DadoGerado.from_dict(dado) for dado in dados_legitimos_dict]
        # Execução
        gerador_dados_fraudados = GeradorDadosFraudados(pct_fraude)
        dados_fraudados = gerador_dados_fraudados.gerar_fraudes(dados_legitimos)
        # Verificação
        assert len(dados_fraudados) == len(dados_legitimos)
        assert sum(1 for dado in dados_fraudados if dado.is_fraude) == int(qtd_dados_legitimos * pct_fraude)