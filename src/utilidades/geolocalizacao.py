from typing import Any

from geolite2 import geolite2
from geopy.geocoders import Nominatim
import reverse_geocoder
import pycountry
from geopy.distance import geodesic


def obter_geolocalizacao_do_ip(ip: str) -> dict[str, Any]:
    """Obtém a geolocalização de um IP público usando a biblioteca geolite2."""
    reader = geolite2.reader()
    dados = reader.get(ip)
    return {
        "latitude": dados['location']['latitude'] if dados and dados.get('location') else None,
        "longitude": dados['location']['longitude'] if dados and dados.get('location') else None,
        "cidade": dados['city']['names']['en'] if dados and dados.get('city') else None,
        "estado": dados['subdivisions'][0]['names']['en'] if dados and dados.get('subdivisions') else None,
        "pais": dados['country']['iso_code'] if dados and dados.get('country') else None,
    }

def obter_paises_estados_cidades_das_latlongs(lista_latlong: list[tuple[float, float]]) -> list[tuple[str, str, str]]:
    """Obtém o país, estado e cidade a partir de uma lista de tuplas de latitude e longitude."""
    paises = []
    estados = []
    cidades = []
    dados = reverse_geocoder.search(lista_latlong)
    for dado in dados:
        paises.append(dado['cc'])
        estados.append(dado['admin1'])
        cidades.append(dado['name'])
    return (paises, estados, cidades)

def distancia_entre_latlongs_km(
    latlong_1: tuple[float, float],
    latlong_2: tuple[float, float]
) -> float:
    """Calcula a distância entre duas geolocalizações em quilômetros."""
    return geodesic(latlong_1, latlong_2).kilometers

def codigo_para_nome_pais(codigo_pais: str) -> str:
    """Converte o código do país para o nome do país."""
    return pycountry.countries.get(alpha_2 = codigo_pais, default = None).name
