import re
import joblib
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.feature_extractor import FeatureExtractor
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    model = None
    tokenizer = None


except FileNotFoundError:
    modelo = None
    print("Advertencia: Modelo no encontrado. Ejecuta primero modelo.py")

def clasificar_direccion(direccion):

    global model, tokenizer
    if model is None or tokenizer is None:
        model_path = os.path.join(BASE_DIR, '..', 'modelos', '01_clasificarDireccion')
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        model.eval()

    # Limpieza básica
    direccion = re.sub(r'\s+', ' ', direccion).strip().lower()
    
    # Tokenizar
    inputs = tokenizer(direccion, return_tensors="pt", padding=True, truncation=True, max_length=64)

    # Lista de palabras clave problemáticas
    palabras_problematicas = ["mz", "manzana", "lt", "lote", "block", "etapa", "mzna", "lote", "lte", "dep", "piso", 
                              "cruce", "entre", "alt", "altura", "etp", "carretera", "cdr", "interior", "edificio", "int.", "dpto.", "dpto"]
    
    # 1. Si no contiene números → problemática
    if not re.search(r'\d', direccion):
        return 1, "⚠️ Dirección sin número, requiere interpretación humana"

    # 2. Si contiene palabras problemáticas → problemática
    if any(p in direccion for p in palabras_problematicas):
        return 1, "⚠️ Dirección ambigua, requiere interpretación humana"
    
    # Inferencia
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = torch.argmax(logits, dim=1).item()

    # Mapear clases a mensajes
    problemas = {
        0: "✅ Dirección estándar, se puede buscar directamente",
        1: "⚠️ Dirección ambigua, requiere interpretación humana"
    }

    return pred, problemas.get(pred, "Clase desconocida")



def obtener_explicacion_problema(codigo):
    """Devuelve el mensaje descriptivo para cada código de problema"""
    explicaciones = {
        0: "La dirección es correcta y completa",
        1: "Contiene referencias a manzana (Mz) y/o lote (Lt)",
    }
    return explicaciones.get(codigo, "Código de problema desconocido")