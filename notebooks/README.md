# Notebooks
O diretório de notebooks deve conter todos os notebooks. Nele, existem dois sub-diretórios:
- `exploratory`: incluir apenas notebooks de análise exploratória ou experimentos, sem muito detalhamento;
- `reports`: incluir notebooks com explicações detalhadas das análises, através de textos e gráficos;

## Código repetido entre notebooks? `src` é a resposta
Caso precise repetir muito código, considere encapsular a lógica no pacote python compartilhado (`src`). Nele você pode criar funções ou classes que serão importadas por um ou mais notebooks. Por exemplo, toda vez que formos baixar dados externos do Kaggle, precisaríamos repetir a mesma lógica, copiando e colando. Ao invés disso, criei uma função que recebe o nome do dataset e baixa ele automaticamente.

## Meu notebook não reconhece o pacote python compartilhado `src`
- Certifique-se de que o ambiente virtual do Kernel do seu notebook está com o pacote instalado, para isso, ative o ambiente virtual e utilize o comando `pip install -e .` na raiz do projeto;
- Reinicie seu Kernel após qualquer alteração em `src`;