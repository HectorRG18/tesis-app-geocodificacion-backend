
'''
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from routes import router
from descargar_modelos import descargar_modelo

app = FastAPI()
BUCKET = "mis-modelos-tesis"
descargar_modelo('modelos/randomForest_problematica/', 'modelos/randomForest_problematica')

# Configuración CORS para permitir conexión desde el frontend en Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Puerto del frontend de Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas que definimos en routes.py
app.include_router(router) 
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from descargar_modelos import descargar_modelo_azure
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI
app = FastAPI()

# Configuración CORS para permitir conexión desde Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si tu frontend está en otro dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Descargar modelos desde Azure Blob Storage
carpetas = [
    "modelos/randomForest_problematica/",
    "modelos/randomForest_distancia/",
    "modelos/bert_direcciones/",
    "modelos/bert_clasificacion_rf/",
    "modelos/bert_crf_referencia/",
    "modelos/bert_crf_referencia/modelo_bert_softmax_tokenizer/"
]
carpeta_base_local = "modelos"

for carpeta in carpetas:
    descargar_modelo_azure(carpeta, carpeta_base_local)

# Incluir rutas
app.include_router(router)

# Ejecutar con Uvicorn si se corre directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
