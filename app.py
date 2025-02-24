from fastapi import FastAPI, File, UploadFile
import pytesseract
from pdf2image import convert_from_bytes
import os
import cv2
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def preprocess_image(img):
    """Melhora a qualidade do OCR removendo ruídos e aumentando contraste."""
    open_cv_image = np.array(img)
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
    
    # Remover ruído e melhorar contraste
    filtered = cv2.bilateralFilter(gray, 5, 75, 75)
    
    # Aplicar threshold adaptativo
    binary = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 31, 2)
    
    return Image.fromarray(binary)

def process_page(img):
    """Corrige rotação, melhora contraste e aplica OCR."""
    img = preprocess_image(img)
    return pytesseract.image_to_string(img, lang="por")

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Converter PDF para imagens com DPI alto para melhor definição
        images = convert_from_bytes(file.file.read(), dpi=300)

        # Processamento paralelo (Multiprocessing) para reduzir tempo
        with ProcessPoolExecutor() as executor:
            texts = list(executor.map(process_page, images))

        # Concatenar todas as páginas
        extracted_text = "\n".join([f"\n--- Página {i+1} ---\n{text}" for i, text in enumerate(texts)])

        return {"text": extracted_text.strip()}

    except Exception as e:
        return {"error": f"Erro ao processar o PDF: {str(e)}"}

@app.get('/check')
async def read_root():
    return {"message": "Live Check"}

@app.get("/")
async def home():
    return {"message": "OCR API is running!"}
