import os
import pandas as pd

# Caminhos dos arquivos CSV de entrada (relativos)
daily_path = "data/jva_daily_raw.csv"
overview_path = "data/jva_overview_raw.csv"
output_path = "data/processed"
os.makedirs(output_path, exist_ok=True)

cotacoes_df = pd.read_csv(daily_path)
overview_df = pd.read_csv(overview_path)

# Criar dim_tempo
dim_tempo = cotacoes_df[['date']].drop_duplicates().copy()
dim_tempo['date'] = pd.to_datetime(dim_tempo['date'])
dim_tempo['tempo_id'] = dim_tempo['date'].dt.strftime('%Y%m%d')
dim_tempo['dia'] = dim_tempo['date'].dt.day
dim_tempo['mes'] = dim_tempo['date'].dt.month
dim_tempo['ano'] = dim_tempo['date'].dt.year
dim_tempo['trimestre'] = dim_tempo['date'].dt.to_period('Q').astype(str)
dim_tempo = dim_tempo[['tempo_id', 'date', 'dia', 'mes', 'trimestre', 'ano']]
dim_tempo.to_csv(f"{output_path}/dim_tempo.csv", index=False)

# Criar dim_empresa
dim_empresa = pd.DataFrame([{
    "empresa_id": 1,
    "simbolo": overview_df.loc[0, 'Symbol'],
    "nome": overview_df.loc[0, 'Name'],
    "setor": overview_df.loc[0, 'Sector'],
    "industria": overview_df.loc[0, 'Industry'],
    "pais": overview_df.loc[0, 'Country']
}])
dim_empresa.to_csv(f"{output_path}/dim_empresa.csv", index=False)

# Criar dim_indicador
indicadores = [
    (1, 'EPS', 'Lucro por ação'),
    (2, 'DividendPerShare', 'Dividendo por ação'),
    (3, 'PERatio', 'Preço sobre Lucro'),
    (4, 'ReturnOnEquityTTM', 'Retorno sobre patrimônio líquido'),
    (5, 'MarketCapitalization', 'Valor de mercado')
]
dim_indicador = pd.DataFrame(indicadores, columns=["indicador_id", "nome_indicador", "descricao"])
dim_indicador.to_csv(f"{output_path}/dim_indicador.csv", index=False)

# Criar fact_cotacoes
cotacoes_df['tempo_id'] = pd.to_datetime(cotacoes_df['date']).dt.strftime('%Y%m%d')
fact_cotacoes = cotacoes_df[['tempo_id', '1. open', '2. high', '3. low', '4. close', '5. volume']].copy()
fact_cotacoes.insert(0, 'cotacao_id', range(1, len(fact_cotacoes)+1))
fact_cotacoes.insert(2, 'empresa_id', 1)
fact_cotacoes.columns = ['cotacao_id', 'tempo_id', 'empresa_id', 'preco_abertura', 'preco_maximo', 'preco_minimo', 'preco_fechamento', 'volume']
fact_cotacoes.to_csv(f"{output_path}/fact_cotacoes.csv", index=False)

# Criar fact_indicadores
fact_indicadores = pd.DataFrame([
    [1, '20241231', 1, 1, overview_df.loc[0, 'EPS']],
    [2, '20241231', 1, 2, overview_df.loc[0, 'DividendPerShare']],
    [3, '20241231', 1, 3, overview_df.loc[0, 'PERatio']],
    [4, '20241231', 1, 4, overview_df.loc[0, 'ReturnOnEquityTTM']],
    [5, '20241231', 1, 5, overview_df.loc[0, 'MarketCapitalization']]
], columns=['indicador_fato_id', 'tempo_id', 'empresa_id', 'indicador_id', 'valor'])

fact_indicadores.to_csv(f"{output_path}/fact_indicadores.csv", index=False)

print(" Transformações concluídas e arquivos salvos em:", output_path)