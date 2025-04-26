# Projeto Integrador 3 - Machine Learning
Este é o repositório de Machine Learning do Projeto Integrador 3 do grupo 013 da DRP14 da UNIVESP. Consiste em um sistema de detecção de operações fraudulentas utilizando modelos de classificação treinados com dados sintetizados.

## Sobre a organização do repositório
A organização do repositório foi inspirada na proposta por [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/).

## Onde estão os dados?
Nenhum dado ficará salvo nesse repositório, pois os dados costumam ocupar muito espaço no repositório. Todos os dados utilizados nesse projeto são baixados ou gerados através de scripts. Eles estaram disponíveis na sua máquina local dentro do diretório `data/` conforme você executar os notebooks.

## Como rodar o projeto?
### Criando ambiente virtual
- Clone o repositório para sua máquina local através do comando `git clone <url_repo>`;
- Abra o repositório no seu editor de código de preferência (Visual Studio Code, PyCharm, etc...);
- Crie um ambiente virtual utilizando o comando: `python -m venv venv`;
- Ative o ambiente virtual via script (`source venv/bin/activate`, no Linux) ou altere o interpretador do seu editor de código para utilizá-lo;
### Instalando dependências
Rode o script `setup_project` no seu terminal (escolha o adequado para seu sistema operacional). Caso não funcione, siga o passo a passo, abaixo:
- Com o ambiente virtual ativo, utilize o comando: `pip install -e .`;
- Altere o Kernel dos notebooks para utilizar o ambiente virtual criado na raiz do projeto (`venv`) ou instale o pacote do projeto no seu Kernel global do Jupyter utilizando `conda install -e <raiz_do_projeto>`;
- Em seguida, utilize os comandos `nbstripout --install` e `nbdime config-git --enable`, para garantir que os commits dos notebooks serão automaticamente limpos e evitar conflitos de merge;

## Como utilizar o pacote?
Você pode instalar o pacote no seu projeto python utilizando o seguinte comando:
```
pip install git+https://github.com/defreitasabner/projeto-integrador-3-machine-learning.git
```
O pacote conta com diversas funções, mas pode ser utilizado de maneira mais simples através da classe `Classificador` como interface de uso:
```python
    # Importe o Classificador
    from sistema_antifraude import Classificador

    # Instancie o classificador
    classificador = Classificador()

    # Organize os dados de entrada (Caso exista uma tentativa anterior)
    # Mesmo que seja apenas a primeira tentativa, envie apenas ela, mas dentro de uma lista
    exemplo_dados_entrada = [
        {
            'user_id': '12345678',
            'device_id': 'abcdefgh',
            'ipv4': '220.99.195.8',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'timestamp': '2023-10-01 12:00:00',
        },
        {
            'user_id': '12345678',
            'device_id': 'kjhhggf',
            'ipv4': '220.99.195.8',
            'latitude': 23.5505,
            'longitude': 46.6333,
            'timestamp': '2023-10-02 2:00:00',
        },
    ]

    # Passe os dados de entrada para o método classificar()
    resultado = classificador.classificar(exemplo_dados_entrada)
    # Exemplo de resultado: { 'fraude': True, 'probabilidade': 0.9914 }
```
Na primeira vez que você rodar, pode levar um tempo considerável, pois o classificador irá:
- Gerar os dados brutos;
- Processar os dados brutos;
- Treinar os modelos de árvore de decisão e regressão logística;
- Comparar os modelos e selecionar o modelo com melhor performance;

Após realizar esses passos, o classificador estará pronto para fazer classificações. O modelo escolhido ficará salvo dentro do diretório gerado na raiz no projeto (`.sistema_antifraude_cache`), para que numa próxima execução, não seja necessário realizar todos os passos acima. Caso você queira alterar parâmetros dos modelos e treiná-los de novo, basta excluir o diretório `.sistema_antifraude_cache`, pois assim o classificador irá repetir todos os passos anteriores durante a próxima execução.