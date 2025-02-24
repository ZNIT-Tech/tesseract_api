# Usa a imagem oficial do Python
FROM python:3.10

# Instala pacotes necessários
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libtesseract-dev \
    tesseract-ocr-por \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY requirements.txt .
COPY app.py .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "$PORT"]

