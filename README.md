# Projeto Integrador 3 - Machine Learning
Este é o repositório de Machine Learning do Projeto Integrador 3 do grupo 013 da DRP14 da UNIVESP. Consiste em um sistema de detecção de operações fraudulentas utilizando modelos de classificação treinados com dados sintetizados.

## Sobre a organização do repositório
A organização do repositório foi inspirada na proposta por [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/).

## Onde estão os dados?
Nenhum dado ficará salvo nesse repositório, pois os dados costumam ocupar muito espaço no repositório. Todos os dados utilizados nesse projeto são baixados ou gerados através de scripts. Eles estaram disponíveis na sua máquina local dentro do diretório `data/` conforme você executar os notebooks.

## Como rodar o projeto?
- Crie um ambiente virtual utilizando o comando: `python -m venv venv`;
- Ative o ambiente virtual via script (`source venv/bin/activate) ou altere o interpretador da sua IDE para utilizá-lo;
- Com o ambiente virtual ativo, utilize o comando: `pip install -e .`;
- Altere o Kernel dos notebooks para utilizar o ambiente virtual criado na raiz do projeto (`venv`);