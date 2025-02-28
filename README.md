# Documentação da API OCR

## Visão Geral
Esta API permite a extração de texto de arquivos PDF utilizando OCR (Reconhecimento Óptico de Caracteres) com Tesseract.

## Tecnologias Utilizadas
- **FastAPI** para criação da API.
- **Tesseract OCR** para extração de texto.
- **pdf2image** para converter PDFs em imagens.
- **Python 3**.
- **Docker** (opcional) para execução em contêineres.

## Endpoints

### 1. Extração de Texto de PDF

**Endpoint:** `/extract`  
**Método:** `POST`

**Descrição:**
Este endpoint permite o envio de um arquivo PDF para extrair texto das suas páginas utilizando OCR.

**Parâmetros:**
- `file`: Arquivo PDF enviado via multipart/form-data.

**Resposta (Sucesso):**
```json
{
  "text": "Texto extraído do PDF."
}
```

**Resposta (Erro):**
```json
{
  "error": "Mensagem de erro."
}
```

### 2. Verificação de Saúde

**Endpoint:** `/health`  
**Método:** `GET`

**Descrição:**
Verifica se a API está em execução corretamente.

**Resposta:**
```json
{
  "message": "Healthy"
}
```

### 3. Página Inicial

**Endpoint:** `/`  
**Método:** `GET`

**Descrição:**
Retorna uma mensagem indicando que a API está em execução.

**Resposta:**
```json
{
  "message": "OCR API is running!"
}
```

## Instalação e Execução

### 1. Requisitos
-- Docker

## Execução com Docker

```bash
docker-compose up --build
```


