from typing import Any

import pandas as pd

from sistema_antifraude.utilidades.geolocalizacao import distancia_entre_latlongs_km
from sistema_antifraude.utilidades.geolocalizacao import obter_geolocalizacao_do_ip
from sistema_antifraude.utilidades.geolocalizacao import obter_paises_estados_cidades_das_latlongs
from sistema_antifraude.default import ColunasDadosBrutos, ColunasDadosProcessados

def executar_pipeline_processamento(dados: dict[str, Any]):
    df = pd.DataFrame(dados)
    df[ColunasDadosBrutos.TIMESTAMP] = pd.to_datetime(df[ColunasDadosBrutos.TIMESTAMP])
    df.sort_values(by = ColunasDadosBrutos.TIMESTAMP, inplace = True)
    df = variacao_tempo_entre_acessos(df)
    df = horario_suspeito(df)
    df = dispositivo_usado_previamente_pelo_usuario(df)
    df = localidades_ip(df)
    df = localidades_latlong(df)
    df = localidades_concordando(df)
    df = distancia_km_entre_acessos_do_usuario(df)
    return df

def variacao_tempo_entre_acessos(df: pd.DataFrame):
    df[ColunasDadosProcessados.VARIACAO_TEMPO_ENTRE_ACESSOS] = 0
    for user_id in df[ColunasDadosBrutos.USER_ID].unique():
        registros_usuario = df[ df[ColunasDadosBrutos.USER_ID] == user_id ].copy()
        registros_usuario.sort_values(by = ColunasDadosBrutos.TIMESTAMP, inplace = True)
        df.loc[
            df[ColunasDadosBrutos.USER_ID] == user_id, ColunasDadosProcessados.VARIACAO_TEMPO_ENTRE_ACESSOS
        ] = (registros_usuario[ColunasDadosBrutos.TIMESTAMP].diff().dt.total_seconds()).fillna(0).map(int)
    return df

def horario_suspeito(df: pd.DataFrame):
    df[ColunasDadosProcessados.HORARIO_SUSPEITO] = \
        df[ColunasDadosBrutos.TIMESTAMP].map(lambda timestamp: 1 if timestamp.hour < 6 else 0)
    return df

def dispositivo_usado_previamente_pelo_usuario(df: pd.DataFrame):
    df[ColunasDadosProcessados.DISPOSITIVO_UTILIZADO_ANTERIORMENTE] = 0
    for user_id in df[ColunasDadosBrutos.USER_ID].unique():
        todos_acessos = df[ df[ColunasDadosBrutos.USER_ID] == user_id ].copy()
        todos_acessos.sort_values(by = ColunasDadosBrutos.TIMESTAMP, inplace = True)
        for idx, acesso_atual in todos_acessos.iterrows():
            dispositivos_anteriores = \
                todos_acessos[todos_acessos[ColunasDadosBrutos.TIMESTAMP] < acesso_atual[ColunasDadosBrutos.TIMESTAMP]][ColunasDadosBrutos.DEVICE_ID].values
            if acesso_atual[ColunasDadosBrutos.DEVICE_ID] in dispositivos_anteriores:
                df.loc[idx, ColunasDadosProcessados.DISPOSITIVO_UTILIZADO_ANTERIORMENTE] = 1
    return df

def localidades_ip(df: pd.DataFrame):
    #TODO: Otimizar essa função
    df[ColunasDadosProcessados.PAIS_IP] = \
        df[ColunasDadosBrutos.IPV4].map(lambda ip: obter_geolocalizacao_do_ip(ip)['pais'])
    df[ColunasDadosProcessados.CIDADE_IP] = \
        df[ColunasDadosBrutos.IPV4].map(lambda ip: obter_geolocalizacao_do_ip(ip)['cidade'])
    return df

def localidades_latlong(df: pd.DataFrame):
    geolocalizacoes = list(
        zip(
            df[ColunasDadosBrutos.LATITUDE].copy().astype(float).values, 
            df[ColunasDadosBrutos.LONGITUDE].copy().astype(float).values
        )
    )
    df[ColunasDadosProcessados.PAIS_LATLONG], df[ColunasDadosProcessados.ESTADO_LATLONG], df[ColunasDadosProcessados.CIDADE_LATLONG] = \
        obter_paises_estados_cidades_das_latlongs(geolocalizacoes)
    return df

def localidades_concordando(df: pd.DataFrame):
    df[ColunasDadosProcessados.PAIS_IP_LATLONG_CONCORDANDO] = \
        df[ColunasDadosProcessados.PAIS_IP] == df[ColunasDadosProcessados.PAIS_LATLONG]
    df[ColunasDadosProcessados.CIDADE_IP_LATLONG_CONCORDANDO] = \
        df[ColunasDadosProcessados.CIDADE_IP] == df[ColunasDadosProcessados.CIDADE_LATLONG]
    df[ColunasDadosProcessados.PAIS_IP_LATLONG_CONCORDANDO] =\
        df[ColunasDadosProcessados.PAIS_IP_LATLONG_CONCORDANDO].map(lambda x: 1 if x else 0)
    df[ColunasDadosProcessados.CIDADE_IP_LATLONG_CONCORDANDO] =\
        df[ColunasDadosProcessados.CIDADE_IP_LATLONG_CONCORDANDO].map(lambda x: 1 if x else 0)
    return df

def distancia_km_entre_acessos_do_usuario(df: pd.DataFrame):
    #TODO: Otimizar essa função
    df[ColunasDadosProcessados.DISTANCIA_KM_ENTRE_ACESSOS] = 0.0
    for user_id in df[ColunasDadosBrutos.USER_ID].unique():
        registros_usuario = df[df[ColunasDadosBrutos.USER_ID] == user_id].copy()
        registros_usuario.sort_values(by = ColunasDadosBrutos.TIMESTAMP, inplace = True)
        for idx, acesso_atual in registros_usuario.iterrows():
            latlong_anteriores = registros_usuario[registros_usuario[ColunasDadosBrutos.TIMESTAMP] < acesso_atual[ColunasDadosBrutos.TIMESTAMP]][[ColunasDadosBrutos.LATITUDE, ColunasDadosBrutos.LONGITUDE]].values
            if len(latlong_anteriores) > 0:
                latlong_anterior = latlong_anteriores[-1]
                distancia = distancia_entre_latlongs_km(
                    (acesso_atual[ColunasDadosBrutos.LATITUDE], acesso_atual[ColunasDadosBrutos.LONGITUDE]), 
                    (latlong_anterior[0], latlong_anterior[1])
                )
                df.loc[idx, ColunasDadosProcessados.DISTANCIA_KM_ENTRE_ACESSOS] = round(distancia, 1)
    return df
