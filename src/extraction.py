import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SYMBOL = os.getenv("SYMBOL")

def fetch_daily_data():
    """
    Recolhe os dados diarios de ações usando a API Alpha Vantage.
    A API Key é lida de uma variável de ambiente chamada 'API_KEY'.
    
    :param symbol: O símbolo da ação (ex.: "EDP.LS" para EDP Portugal).
    :return: DataFrame contendo os dados históricos mensais ajustados.
    """
    # Verificar a API Key do ambiente    
    if not API_KEY:
        raise ValueError("A API Key não está definida. Configure a variável de ambiente 'API_KEY'.")

    # Endpoint da API
    url = "https://www.alphavantage.co/query"
    
    # Parâmetros da solicitação
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": SYMBOL,
        "outputsize": "full", # full ou compact
        "datatype": "json",  # JSON ou CSV
        "apikey": API_KEY  
    }
    
    # Fazendo a solicitação à API
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Garante que erros HTTP sejam tratados
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
    
    # Verificar a resposta da API
    data = response.json()
    if "Time Series (Daily)" not in data:
        print("Erro: Não foram encontrados dados para o símbolo fornecido.")
        return None

    # Processar os dados
    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.index = pd.to_datetime(df.index)  # Converte o índice para datetime
    df.columns = [
        "open", "high", "low", "close", "volume"
    ]
    df = df.sort_index()  # Ordena por data
    
    # Caminho para salvar o CSV
#    output_path = r"data\\daily_adjusted_data.csv"
#    try:
#        df.to_csv(output_path)
#        print(f"Dados diarios ajustados salvos em: {output_path}")
#    except Exception as e:
#        print(f"Erro ao salvar o arquivo CSV: {e}")
#        return None

    return df

def fetch_company_overview():
    """
    Recolhe os dados fundamentais da empresa via a API Alpha Vantage.
    A API Key é lida de uma variável de ambiente chamada 'API_KEY'.
    
    :param symbol: O símbolo da ação (ex.: "EDP.LS" para EDP Portugal).
    :return: DataFrame contendo os dados relevantes da accao.
    """
    # Verificar a API Key do ambiente    
    if not API_KEY:
        raise ValueError("A API Key não está definida. Configure a variável de ambiente 'API_KEY'.")

    # Endpoint da API
    url = "https://www.alphavantage.co/query"
    
    # Parâmetros da solicitação
    params = {
        "function": "OVERVIEW",
        "symbol": SYMBOL,
        "apikey": API_KEY  
    }

        # Fazendo a solicitação à API
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Garante que erros HTTP sejam tratados
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
    
    # Verificar a resposta da API
    data = response.json()

    return pd.DataFrame([data])
        

if __name__ == "__main__":
    # Certifique-se de que a variável de ambiente 'API_KEY' está configurada antes de rodar o código
#    try:
#        stock_data = fetch_daily_data()
#        if stock_data is not None:
#            print(stock_data.head())
#    except Exception as e:
#        print(f"Erro no programa principal: {e}")

#    try:
#        company_data = fetch_daily_data()
#        if stock_data is not None:
#            print(stock_data.head())
#    except Exception as e:
#        print(f"Erro no programa principal: {e}")

    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    daily_output_path = os.path.join(output_dir, 'jva_daily_raw.csv')
    overview_output_path = os.path.join(output_dir, 'jva_overview_raw.csv')

    df_daily = fetch_daily_data()
    df_overview = fetch_company_overview()

    df_daily.to_csv(daily_output_path, index=False)
    df_overview.to_csv(overview_output_path, index=False)

    print(" Extração finalizada com sucesso!\n"
          f" Dados diários salvos em: {daily_output_path}\n"
          f" Dados gerais salvos em: {overview_output_path}")