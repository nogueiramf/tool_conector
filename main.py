import os
import pandas as pd
import yaml
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class ReviewFetcherTool(BaseTool):
    """
    Classe que busca reviews do MongoDB e salva em um arquivo CSV.

    Atributos:
        name (str): Nome da ferramenta.
        description (str): Descrição da ferramenta.
    """
    name: str = "review_fetcher_tool"
    description: str = "Fetches reviews from MongoDB and saves them to a CSV file"

    def _run(self) -> str:
        """
        Busca reviews do MongoDB e salva em um arquivo CSV.

        Returns:
            str: Mensagem indicando o status da operação.
        """
        # Obter a URI do MongoDB a partir da variável de ambiente
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            return "Environment variable 'MONGO_URI' not set."

        # Carregar parâmetros da consulta do arquivo consulta.yaml
        try:
            with open('config/consulta.yaml', 'r') as file:
                consulta = yaml.safe_load(file)
        except FileNotFoundError:
            return "consulta.yaml file not found in config directory."
        except yaml.YAMLError as e:
            return f"Error parsing consulta.yaml file: {e}"

        app_id = consulta.get('appId')
        store = consulta.get('store')
        lang = consulta.get('lang')
        start_date_str = consulta.get('start_date')
        end_date_str = consulta.get('end_date')

        if not app_id or not store or not lang or not start_date_str or not end_date_str:
            return "Missing query parameters in consulta.yaml."

        # Converter strings de datas para objetos datetime
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%SZ')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as e:
            return f"Error parsing dates: {e}"

        # Conectar ao MongoDB
        try:
            client = MongoClient(mongo_uri)
            db = client['ReviewsGplay']
            collection = db['reviews']
        except Exception as e:
            return f"Error connecting to MongoDB: {e}"

        # Realizar a consulta
        query = {
            "appId": app_id,
            "store": store,
            "lang": lang,
            "date": {"$gte": start_date, "$lte": end_date}
        }

        try:
            results = collection.find(query)
        except Exception as e:
            return f"Error executing query: {e}"

        # Converter os resultados para um DataFrame do pandas
        try:
            df = pd.DataFrame(list(results))
        except Exception as e:
            return f"Error converting results to DataFrame: {e}"

        # Verificar se o diretório de saída existe, se não, criá-lo
        output_dir = os.path.join('data', 'output')
        os.makedirs(output_dir, exist_ok=True)

        # Caminho completo para salvar o arquivo CSV
        output_file = os.path.join(output_dir, "reviews_export.csv")

        # Exportar para um arquivo CSV
        try:
            df.to_csv(output_file, index=False)
        except Exception as e:
            return f"Error exporting to CSV: {e}"

        # Fechar a conexão
        client.close()

        return f"Reviews fetched and saved to {output_file}"

# Exemplo de como usar a ferramenta
if __name__ == "__main__":
    tool = ReviewFetcherTool()
    result = tool._run()
    print(result)
