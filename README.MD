

## Instalação

Certifique-se de que você tem Python >=3.10 <=3.13 instalado em seu sistema. Este projeto usa `pip` para gerenciamento de dependências e manipulação de pacotes.

Primeiro, crie um ambiente virtual (opcional, mas recomendado):


```bash
python -m venv venv
```
## WINDOWS
```bash
venv\Scripts\activate
```
Em seguida, instale as dependências usando pip:
```bash
pip install -r requirements.txt
```

## Personalização
Adicione o seu MONGO_URI no arquivo .env

Modifique config/consulta.yaml para configurar os parâmetros da consulta.
Modifique main.py se necessário para ajustar a lógica, ferramentas e argumentos específicos.
Executando o Projeto
Para executar o script e executar a ferramenta de busca de avaliações, execute o seguinte comando a partir da pasta raiz do seu projeto:
```bash
python main.py
```

Este comando inicializa o ReviewFetcherTool, realiza a consulta ao MongoDB e salva as avaliações obtidas em um arquivo CSV no diretório data/output.

Compreendendo Sua Ferramenta
O ReviewFetcherTool foi projetado para buscar avaliações de um banco de dados MongoDB com base nos parâmetros especificados em config/consulta.yaml. Em seguida, ele salva essas avaliações em um arquivo CSV.

- **Parâmetros**:
  - `appId`: O ID do aplicativo para as avaliações.
  - `store`: A loja da qual buscar as avaliações.
  - `lang`: O idioma das avaliações.
  - `start_date`: A data de início para as avaliações.
  - `end_date`: A data de término para as avaliações.
