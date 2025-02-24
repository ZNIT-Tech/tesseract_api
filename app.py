from fastapi import FastAPI, File, UploadFile
import pytesseract
from pdf2image import convert_from_bytes
import os
import cv2
import numpy as np
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def preprocess_image(img):
    """Pré-processa a imagem para melhorar a qualidade do OCR."""
    open_cv_image = np.array(img)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)

def process_page(img):
    """Aplica OCR na página pré-processada."""
    img = preprocess_image(img)
    return pytesseract.image_to_string(img, lang="por")

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Converter PDF para imagens com DPI reduzido para acelerar
        images = convert_from_bytes(file.file.read(), dpi=100)

        # Processar OCR em paralelo
        with ThreadPoolExecutor() as executor:
            texts = list(executor.map(process_page, images))

        # Concatenar todas as páginas
        extracted_text = "\n".join([f"\n--- Página {i+1} ---\n{text}" for i, text in enumerate(texts)])

        return {"text": extracted_text.strip()}

    except Exception as e:
        return {"error": f"Erro ao processar o PDF: {str(e)}"}

@app.get('/lifecheck')
async def read_root():
    return {"message": "Hello!"}
