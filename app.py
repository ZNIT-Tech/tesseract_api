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
    """
    Extract text from an uploaded PDF file using OCR.
    Endpoint: /extract
    Method: POST
    Args:
        file (UploadFile): The uploaded PDF file to be processed.
    Returns:
        dict: A dictionary containing the extracted text or an error message.
    Raises:
        Exception: If an error occurs during the file processing or OCR extraction.
    Process:
    1. Save the uploaded PDF file temporarily.
    2. Convert the PDF into images.
    3. Apply OCR to each image to extract text.
    4. Remove the temporary PDF file.
    5. Return the extracted text as a JSON response.
    """
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

@app.get('/health')
async def read_root():
    return {"message": "Healthy"}

@app.get("/")
async def home():
    return {"message": "OCR API is running!"}
