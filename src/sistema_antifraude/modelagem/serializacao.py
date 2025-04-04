import os
import json
import pickle
from typing import Any

from sistema_antifraude import config


def salvar_modelo(nome_modelo: str, modelo, dir_modelos = config.MODELS_PATH):
    path_dir_modelo = os.path.join(dir_modelos, nome_modelo)
    os.makedirs(path_dir_modelo, exist_ok = True)
    with open(os.path.join(path_dir_modelo, "modelo.pkl"), 'wb') as arquivo:
        pickle.dump(modelo, arquivo)

def salvar_parametros(nome_modelo: str, parametros: dict[str, Any],  dir_modelos = config.MODELS_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "parametros.json")
    with open(path_arquivo, 'w') as arquivo:
        json.dump(parametros, arquivo)

def salvar_metricas(
    nome_modelo: str,
    metricas: dict[str, Any], 
    formato = 'json', 
    dir_modelos = config.MODELS_PATH
):
    if formato not in ['json', 'csv']:
        raise ValueError("Formato deve ser 'json' ou 'csv'.")
    path_arquivo = os.path.join(dir_modelos, nome_modelo, f"metricas.{formato}")
    if formato == 'json':
        with open(path_arquivo, 'w') as arquivo:
            json.dump(metricas, arquivo)
    elif formato == 'csv':
        with open(path_arquivo, 'w') as arquivo:
            arquivo.write("metricas\n")
            for key, value in metricas.items():
                arquivo.write(f"{key},{value}\n")

def salvar_metadados(nome_modelo: str, metadados: dict[str, Any], dir_modelos = config.MODELS_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "metadados.json")
    with open(path_arquivo, 'w') as arquivo:
        json.dump(metadados, arquivo)

def salvar_requisitos(nome_modelo: str, requisitos: list[str], dir_modelos = config.MODELS_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "requirements.txt")
    with open(path_arquivo, 'w') as arquivo:
        for requisito in requisitos:
            arquivo.write(f"{requisito}\n")

def salvar_tudo(
    nome_modelo: str,
    modelo,
    parametros: dict[str, Any] = None,
    metricas: dict[str, Any] = None,
    metadados: dict[str, Any] = None,
    requisitos: list[str] = [],
    dir_modelos = config.MODELS_PATH
):
    salvar_modelo(nome_modelo, modelo, dir_modelos)
    if parametros is not None:
        salvar_parametros(nome_modelo, parametros, dir_modelos)
    if metricas is not None:
        salvar_metricas(nome_modelo, metricas, 'json', dir_modelos)
        salvar_metricas(nome_modelo, metricas, 'csv', dir_modelos)
    if metadados is not None:
        salvar_metadados(nome_modelo, metadados, dir_modelos)
    if len(requisitos) > 0:
        salvar_requisitos(nome_modelo, requisitos, dir_modelos)

def carregar_modelo(nome_modelo: str, dir_modelos=config.MODELS_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "modelo.pkl")
    with open(path_arquivo, 'rb') as arquivo:
        modelo = pickle.load(arquivo)
    return modelo
