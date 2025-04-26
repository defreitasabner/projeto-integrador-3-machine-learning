class ColunasDadosBrutos(object):
    """
    Classe para armazenar os nomes das colunas do DataFrame de dados brutos.
    """
    USER_ID = "user_id"
    DEVICE_ID = "device_id"
    IPV4 = "ipv4"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    TIMESTAMP = "timestamp"
    IS_FRAUDE = "is_fraude"

class ColunasDadosProcessados(object):
    """
    Classe para armazenar os nomes das colunas do DataFrame de dados processados.
    """
    VARIACAO_TEMPO_ENTRE_ACESSOS = 'variacao_tempo_entre_acessos'
    DISPOSITIVO_UTILIZADO_ANTERIORMENTE = 'dispositivo_utilizado_anteriormente'
    PAIS_IP_LATLONG_CONCORDANDO = 'pais_ip_latlong_concordando'
    CIDADE_IP_LATLONG_CONCORDANDO = 'cidade_ip_latlong_concordando'
    HORARIO_SUSPEITO = 'horario_suspeito'
    DISTANCIA_KM_ENTRE_ACESSOS = 'distancia_km_entre_acessos'
    PAIS_IP = 'pais_ip'
    CIDADE_IP = 'cidade_ip'
    PAIS_LATLONG = 'pais_latlong'
    ESTADO_LATLONG = 'estado_latlong'
    CIDADE_LATLONG = 'cidade_latlong'