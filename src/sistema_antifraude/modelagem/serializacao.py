import os
import json
import pickle
from typing import Any

from sistema_antifraude import config


def salvar_modelo(nome_modelo: str, modelo, dir_modelos = config.CACHE_DIR_PATH):
    path_dir_modelo = os.path.join(dir_modelos, nome_modelo)
    os.makedirs(path_dir_modelo, exist_ok = True)
    with open(os.path.join(path_dir_modelo, "modelo.pkl"), 'wb') as arquivo:
        pickle.dump(modelo, arquivo)

def salvar_parametros(nome_modelo: str, parametros: dict[str, Any],  dir_modelos = config.CACHE_DIR_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "parametros.json")
    with open(path_arquivo, 'w') as arquivo:
        json.dump(parametros, arquivo, indent = 4)

def salvar_metricas(
    nome_modelo: str,
    metricas: dict[str, Any], 
    formato = 'json', 
    dir_modelos = config.CACHE_DIR_PATH
):
    if formato not in ['json', 'csv']:
        raise ValueError("Formato deve ser 'json' ou 'csv'.")
    path_arquivo = os.path.join(dir_modelos, nome_modelo, f"metricas.{formato}")
    if formato == 'json':
        with open(path_arquivo, 'w') as arquivo:
            json.dump(metricas, arquivo, indent = 4)
    elif formato == 'csv':
        with open(path_arquivo, 'w') as arquivo:
            arquivo.write("metricas\n")
            for key, value in metricas.items():
                arquivo.write(f"{key},{value}\n")

def salvar_metadados(nome_modelo: str, metadados: dict[str, Any], dir_modelos = config.CACHE_DIR_PATH):
    path_arquivo = os.path.join(dir_modelos, nome_modelo, "metadados.json")
    with open(path_arquivo, 'w') as arquivo:
        json.dump(metadados, arquivo, indent = 4)


def salvar_tudo(
    nome_modelo: str,
    modelo,
    parametros: dict[str, Any] = None,
    metricas: dict[str, Any] = None,
    metadados: dict[str, Any] = None,
    dir_modelos = config.CACHE_DIR_PATH
):
    salvar_modelo(nome_modelo, modelo, dir_modelos)
    if parametros is not None:
        salvar_parametros(nome_modelo, parametros, dir_modelos)
    if metricas is not None:
        salvar_metricas(nome_modelo, metricas, 'json', dir_modelos)
    if metadados is not None:
        salvar_metadados(nome_modelo, metadados, dir_modelos)

def carregar_modelo(nome_modelo: str, cache_dir_path = config.CACHE_DIR_PATH):
    path_arquivo = os.path.join(cache_dir_path, nome_modelo, "modelo.pkl")
    with open(path_arquivo, 'rb') as arquivo:
        modelo = pickle.load(arquivo)
    return modelo

def carregar_parametros(nome_modelo: str, cache_dir_path = config.CACHE_DIR_PATH):
    path_arquivo = os.path.join(cache_dir_path, nome_modelo, "parametros.json")
    with open(path_arquivo, 'r') as arquivo:
        parametros = json.load(arquivo)
    return parametros
