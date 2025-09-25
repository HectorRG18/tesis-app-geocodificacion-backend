#import boto3
#import os
"""
s3 = boto3.client('s3') 
BUCKET = "mis-modelos-tesis"

def descargar_modelo(bucket_name, carpeta_s3, carpeta_local):
    print(f"🔽 Descargando: {carpeta_s3}")
    respuesta = s3.list_objects_v2(Bucket=bucket_name, Prefix=carpeta_s3)

    if 'Contents' not in respuesta:
        print(f"⚠️ No se encontró la carpeta: {carpeta_s3}")
        return

    for obj in respuesta['Contents']:
        ruta_s3 = obj['Key']
        if ruta_s3.endswith("/"):
            continue  # Es carpeta, no archivo

        ruta_local = os.path.join(carpeta_local, *ruta_s3.split("/")[2:])
        os.makedirs(os.path.dirname(ruta_local), exist_ok=True)

        if not os.path.exists(ruta_local):
            s3.download_file(bucket_name, ruta_s3, ruta_local)
            print(f"✅ Descargado: {ruta_local}")
        else:
            print(f"🟡 Ya existe: {ruta_local}")

# Lista de carpetas a descargar
carpetas = [
    "modelos/randomForest_problematica/",
    "modelos/randomForest_distancia/",
    "modelos/bert_direcciones/",
    "modelos/bert_clasificacion_rf/",
    "modelos/bert_crf_referencia/",
    "modelos/bert_crf_referencia/modelo_bert_softmax_tokenizer/"
]

for carpeta in carpetas:
    descargar_modelo(BUCKET, carpeta, "modelos")


"""
'''
import os
def descargar_modelo(carpetas, carpeta_base_local):
    for carpeta_relativa in carpetas:
        ruta_local = os.path.join(carpeta_base_local, *carpeta_relativa.split("/")[1:])
        print(f"🔍 Verificando: {ruta_local}")

        if os.path.exists(ruta_local):
            print(f"✅ Disponible localmente: {ruta_local}")
        else:
            print(f"⚠️ No se encontró: {ruta_local}")

# Lista de carpetas que deberían existir localmente
carpetas = [
    "modelos/randomForest_problematica/",
    "modelos/randomForest_distancia/",
    "modelos/bert_direcciones/",
    "modelos/bert_clasificacion_rf/",
    "modelos/bert_crf_referencia/",
    "modelos/bert_crf_referencia/modelo_bert_softmax_tokenizer/"
]

# Carpeta base donde están los modelos
carpeta_base_local = "modelos"

descargar_modelo(carpetas, carpeta_base_local)
'''

import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# 🔹 Cargar variables de entorno desde .env
load_dotenv()
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER")

# 🔹 Conexión a Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def descargar_modelo_azure(carpeta_blob, carpeta_local):
    print(f"\n🔽 Descargando desde Azure: {carpeta_blob}")
    
    blobs = container_client.list_blobs(name_starts_with=carpeta_blob)

    for blob in blobs:
        if blob.name.endswith("/"):
            continue  # Ignorar carpetas virtuales

        # 🔹 Construir ruta local manteniendo estructura relativa
        partes = blob.name.split("/")
        ruta_local = os.path.join(carpeta_local, *partes[1:] if partes[0] == "modelos" else partes)
        os.makedirs(os.path.dirname(ruta_local), exist_ok=True)

        # 🔹 Verificar si el blob existe antes de descargar
        blob_client = container_client.get_blob_client(blob.name)
        if blob_client.exists():
            if not os.path.exists(ruta_local):
                with open(ruta_local, "wb") as f:
                    f.write(blob_client.download_blob().readall())
                print(f"✅ Descargado: {ruta_local}")
            else:
                print(f"🟡 Ya existe: {ruta_local}")
        else:
            print(f"❌ Blob no encontrado: {blob.name}")

# 🔹 Lista de carpetas a descargar
carpetas = [
    "modelos/randomForest_problematica/",
    "modelos/randomForest_distancia/",
    "modelos/bert_direcciones/",
    "modelos/bert_clasificacion_rf/",
    "modelos/bert_crf_referencia/",
    "modelos/bert_crf_referencia/modelo_bert_softmax_tokenizer/"
]

# 🔹 Carpeta base local donde se guardarán
carpeta_base_local = "modelos"

# 🔹 Ejecutar descarga por carpeta
for carpeta in carpetas:
    descargar_modelo_azure(carpeta, carpeta_base_local)


