# Notebooks
O diretório de notebooks deve conter todos os notebooks. Nele, existem dois sub-diretórios:
- `exploratory`: incluir apenas notebooks de análise exploratória ou experimentos, sem muito detalhamento;
- `reports`: incluir notebooks com explicações detalhadas das análises, através de textos e gráficos;

## Código repetido entre notebooks? `src` é a resposta
Caso precise repetir muito código, considere encapsular a lógica no pacote python compartilhado (`src`). Nele você pode criar funções ou classes que serão importadas por um ou mais notebooks. Por exemplo, toda vez que formos baixar dados externos do Kaggle, precisarímos repetir a mesma lógica, copiando e colando. Ao invés disso, criei uma função que recebe o nome do dataset e baixa ele automaticamente.

## Para rodar os notebooks
Você pode desenvolver os notebooks no seu ambiente de preferência e no final incluir aqui para deixar registro das análises e dos experimentos. Caso queira rodar tudo dentro da sua IDE, para se beneficiar do pacote compartilhado (`src`), siga os seguintes passos:
- Crie um ambiente virtual dentro do diretório `notebooks/`;
- Instale as dependências de `notebooks/requirements.txt` (específicas para os notebooks);
- Selecione o ambiente virtual criado em `notebooks/` como o ambiente do kernel do seu notebook;

## Algumas dúvidas que podem surgir

### Porque dois ambientes virtuais separados?
Optei por separar o ambiente virtual dos notebooks do ambiente virtual geral, pois existem bibliotecas que só são utilizadas nos notebooks. Caso isso esteja dificultando o uso pra você, crie um ambiente virtual único e instale as dependências presentes em ambos arquivos de requisitos (`requirements.txt` e `notebooks/requirements.txt`).

### Meu notebook não reconhece o pacote python compartilhado `src`
- Certifique-se de que o Kernel do seu notebook está com todas as dependências presentes em `notebooks/requirements.txt`;
- Reinicie seu Kernel após qualquer alteração em `src`;
- Se o problema persistir, tente reinstalar as dependências presentes em `notebooks/requirements.txt`;