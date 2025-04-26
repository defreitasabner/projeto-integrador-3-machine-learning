from typing import Any
import random

import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from sistema_antifraude.gerador_dados.gerador import Gerador
from sistema_antifraude.default import ColunasDadosProcessados, ColunasDadosBrutos
from sistema_antifraude.modelagem.processamento import executar_pipeline_processamento
from sistema_antifraude.modelagem.metricas import calcular_metricas
from sistema_antifraude.modelagem.serializacao import salvar_tudo, carregar_modelo
from sistema_antifraude.modelagem.parametros import ParametrosArvoreDecisao, ParametrosRegressaoLogistica


class Classificador:
    def __init__(
        self, 
        parametros_arvore_decisao = ParametrosArvoreDecisao.DEFAULT,
        parametros_regressao_logistica = ParametrosRegressaoLogistica.DEFAULT,
    ):
        self.__features = [
            ColunasDadosProcessados.VARIACAO_TEMPO_ENTRE_ACESSOS,
            ColunasDadosProcessados.DISPOSITIVO_UTILIZADO_ANTERIORMENTE,
            ColunasDadosProcessados.PAIS_IP_LATLONG_CONCORDANDO,
            ColunasDadosProcessados.HORARIO_SUSPEITO,
            ColunasDadosProcessados.DISTANCIA_KM_ENTRE_ACESSOS
        ]
        self.__target = ColunasDadosBrutos.IS_FRAUDE
        self.__padronizador = StandardScaler()
        self.__parametros_arvore_decisao = parametros_arvore_decisao
        self.__parametros_regressao_logistica = parametros_regressao_logistica
        self.__modelo = self.__obter_melhor_modelo()

    def classificar(
        self, 
        dados: list[dict[str, Any]], 
        processar_dados = True
    ) -> dict[str, Any]:
        if processar_dados:
            dados = executar_pipeline_processamento(dados)
        X = dados[self.__features].iloc[-1:].copy()
        classificacao = int(self.__modelo.predict(X)[0]) == 1
        probabilidade = round(float(self.__modelo.predict_proba(X).max()), 4)
        return {
            'fraude': classificacao,
            'probabilidade': probabilidade
        }

    def __obter_melhor_modelo(self):
        try:
            return carregar_modelo('modelo')
        except:
            print("Modelo não encontrado. Treinando novos modelos e selecionando o melhor...")
            return self.__treinar_modelos_e_selecionar_melhor()

    def __treinar_modelos_e_selecionar_melhor(
        self,
        random_state = 42
    ):
        random.seed(random_state)
        np.random.seed(random_state)

        dados = Gerador().gerar_dados()
        
        dados = executar_pipeline_processamento(dados)

        X = dados[self.__features].copy()
        y = dados[self.__target].map(lambda y: 1 if y else 0).copy()
        
        # Separando os dados em treino e teste
        X_treino, X_teste, y_treino, y_teste = train_test_split(
            X, 
            y, 
            test_size = 0.3, 
            shuffle = True,
            stratify = y,
        )

        # Aplicando SMOTE para balancear os dados
        smote = SMOTE()
        X_treino_smote, y_treino_smote = smote.fit_resample(X_treino, y_treino)
    
        # Padronizando os dados
        X_train_smote_padronizado = self.__padronizador.fit_transform(X_treino_smote)

        # Treinando os modelos
        arvore_decisao = DecisionTreeClassifier(**self.__parametros_arvore_decisao)
        arvore_decisao.fit(X_treino_smote, y_treino_smote)

        regressao_logistica = LogisticRegression(**self.__parametros_regressao_logistica)
        regressao_logistica.fit(X_train_smote_padronizado, y_treino_smote)

        # Calculando as métricas
        metricas_arvore_decisao = calcular_metricas(y_teste, arvore_decisao.predict(X_teste))
        X_teste_padronizado = self.__padronizador.transform(X_teste)
        metricas_regressao_logistica = calcular_metricas(y_teste, regressao_logistica.predict(X_teste_padronizado))

        # Selecionando melhor modelo
        modelo_selecionado = None
        metricas_selecionadas = None
        parametros_selecionados = None
        if metricas_arvore_decisao['f1'] > metricas_regressao_logistica['f1']:
            modelo_selecionado = arvore_decisao
            metricas_selecionadas = metricas_arvore_decisao
            parametros_selecionados = self.__parametros_arvore_decisao
        else:
            modelo_selecionado = regressao_logistica
            metricas_selecionadas = metricas_regressao_logistica
            parametros_selecionados = self.__parametros_regressao_logistica

        # Salvando o melhor modelo
        salvar_tudo(
            nome_modelo = 'modelo',
            modelo = modelo_selecionado,
            metricas = metricas_selecionadas,
            parametros = parametros_selecionados,
            metadados = {
                'tipo_modelo': modelo_selecionado.__class__.__name__,
                'features': self.__features,
                'target': self.__target,
                'random_state': random_state
            }
        )

        return modelo_selecionado