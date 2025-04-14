import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Conexão com o banco
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DBNAME = os.getenv("DB_NAME")
PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
engine = create_engine(DATABASE_URL)

# Caminhos dos arquivos processados
csv_files = {
    "dim_empresa": "data/processed/dim_empresa.csv",
    "dim_indicador": "data/processed/dim_indicador.csv",
    "dim_tempo": "data/processed/dim_tempo.csv",
    "fact_cotacoes": "data/processed/fact_cotacoes.csv",
    "fact_indicadores": "data/processed/fact_indicadores.csv"
}

def create_tables(csv_files, engine):
    for table_name, file_path in csv_files.items():
        print(f"\n Carregando dados para a tabela `{table_name}`...")

        # Lê o CSV
        df = pd.read_csv(file_path)

        # Limpa a tabela antes de inserir (sem derrubar estrutura)
        with engine.begin() as conn:
            print(f" Limpando tabela `{table_name}`...")
            conn.execute(text(f"DELETE FROM {table_name}"))

        # Insere os dados
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f" Tabela `{table_name}` atualizada com sucesso!")

if __name__ == "__main__":
    print(" Iniciando carga dos dados no banco PostgreSQL...\n")
    create_tables(csv_files, engine)
    print("\n Carga finalizada com sucesso!")