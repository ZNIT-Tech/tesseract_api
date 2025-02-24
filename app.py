from fastapi import FastAPI, File, UploadFile
import pytesseract
from pdf2image import convert_from_bytes
import os
from tempfile import NamedTemporaryFile
import shutil

app = FastAPI()

# Configuração do Tesseract no Docker
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Salvar arquivo temporariamente
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            shutil.copyfileobj(file.file, temp_pdf)
            temp_pdf_path = temp_pdf.name

        # Converter PDF em imagens
        images = convert_from_bytes(open(temp_pdf_path, "rb").read())

        # Inicializar variável para armazenar o texto extraído
        full_text = ""

        # Aplicar OCR em cada página
        for img in images:
            text = pytesseract.image_to_string(img, lang="por")  
            full_text += text + "\n"

        # Remover o arquivo temporário
        os.remove(temp_pdf_path)

        # Retornar o texto extraído como JSON
        return {"text": full_text.strip()}

    except Exception as e:
        return {"error": str(e)}

@app.get('/check')
async def read_root():
    return {"message": "Live Check"}

@app.get("/")
async def home():
    return {"message": "OCR API is running!"}
