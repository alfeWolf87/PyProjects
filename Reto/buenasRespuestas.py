import os
import time
import pandas as pd
from google import genai
from google.genai import errors

# 1. Configuración del nuevo cliente de Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("ERROR: No se encontró la variable de entorno 'GEMINI_API_KEY'.")

# Inicializamos el cliente moderno
client = genai.Client(api_key=API_KEY)

def clasificar_sentimiento(texto):
    """
    Llama a la API moderna de Gemini para clasificar el sentimiento.
    """
    # Usamos el modelo estándar actual
    NOMBRE_MODELO = "gemini-2.5-flash" 
    
    prompt = f"""
    Eres un analista de datos experto en experiencia del cliente (CX). 
    Analiza la siguiente respuesta a la pregunta "¿Qué tan satisfecho estás con el servicio de atención al cliente?".
    
    Clasifica el sentimiento de la respuesta ÚNICAMENTE en una de estas tres categorías:
    - Positivo
    - Negativo
    - Neutro

    Regla estricta: Responde solo con la palabra de la categoría (ej. "Positivo"). No agregues puntos, saludos ni explicaciones.

    Respuesta: "{texto}"
    Sentimiento:
    """
    
    try:
        # Sintaxis moderna: client.models.generate_content
        response = client.models.generate_content(
            model=NOMBRE_MODELO,
            contents=prompt,
        )
        resultado = response.text.strip()
        
        # Validación de categoría
        for categoria in ["Positivo", "Negativo", "Neutro"]:
            if categoria.lower() in resultado.lower():
                return categoria
        return "Neutro"
        
    except errors.APIError as e:
        print(f"Error de API con el modelo {NOMBRE_MODELO}: {e}")
        return "Error"
    except Exception as e:
        print(f"Error inesperado: {e}")
        return "Error"

def main():
    input_filename = "respuestas_encuesta.csv"
    output_filename = "resultados_sentimiento.csv"
    
    # Verificar existencia en el directorio actual
    if not os.path.exists(input_filename):
        print(f"ERROR: No se encuentra el archivo '{input_filename}' en el directorio actual: {os.getcwd()}")
        return
        
    df = pd.read_csv(input_filename)
    
    if 'id' not in df.columns or 'respuesta' not in df.columns:
        print("ERROR: El CSV debe contener las columnas 'id' y 'respuesta'.")
        return

    print(f"Iniciando clasificación de {len(df)} respuestas usando google-genai...")
    resultados_sentimiento = []
    
    for index, fila in df.iterrows():
        print(f"Procesando ID {fila['id']}...")
        sentimiento = clasificar_sentimiento(fila['respuesta'])
        resultados_sentimiento.append(sentimiento)
        
        # Respetar Rate Limit de la capa gratuita (15 RPM)
        time.sleep(4.5)
        
    df['sentimiento'] = resultados_sentimiento
    
    df_final = df[['id', 'respuesta', 'sentimiento']]
    df_final.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nProceso completado. Archivo guardado como '{output_filename}'")
    
    print("\n" + "="*30)
    print("      RESUMEN DE SENTIMIENTOS")
    print("="*30)
    conteo = df_final['sentimiento'].value_counts()
    for cat in ["Positivo", "Negativo", "Neutro", "Error"]:
        print(f"{cat.ljust(12)}: {conteo.get(cat, 0)}")
    print("="*30)

if __name__ == "__main__":
    main()