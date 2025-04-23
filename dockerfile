# Usa imagem base com Python 3.12
FROM python:3.10.17-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos e pastas para dentro do container
COPY . .

# Instala dependências do sistema (se necessário futuramente)
RUN apt-get update && apt-get install -y build-essential

# Atualiza pip e instala dependências Python
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Define variável para garantir execução sequencial sem buffer
ENV PYTHONUNBUFFERED=1

# Comando principal: executa a pipeline ETL
CMD ["bash", "-c", "python src/extraction.py && python src/transformation.py && python src/load.py"]