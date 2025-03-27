# Data
Esse é o diretório de dados irá conter todos os **dados necessários para as análises e os treinamentos e validações dos modelos**. Esse diretório está dividido em 3 sub-diretórios:
- `raw`: incluir os dados brutos, obtidos ou gerados por nós;
- `processed`: incluir dados que foram processados de alguma forma;
- `external`: incluir dados baixados de fontes externas;
É importante que você mantenha a estrutura de sub-diretórios. **Não inclua arquivos desse diretório no controle de versão, pois os dados costumam ser arquivos pesados** e podem exceder a quantidade permitida no GitHub. **Todos os dados são devem ser baixados ou gerados pelos scripts durante as análises e experimentos.**