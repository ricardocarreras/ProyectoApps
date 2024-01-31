import streamlit as st

import openai
from openai import OpenAI

# Configura tu clave API de OpenAI
import os

from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Asignar la API KEY de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generar_publicacion_con_gpt(tema, palabras_clave, matiz, fechahoy, urlnoticia1, urlnoticia2):
    try:
        client = OpenAI(api_key=openai.api_key)

        prompt = f"Escribe una noticia periodística de 1000 palabras sobre {tema}. Considera que hoy es {fechahoy}. Considera que {matiz}. Para crear la noticia comienza por fusionar dos noticias, la primera la puedes encontrar en esta url {urlnoticia1}. La segunda en esta otra url {urlnoticia2}. Fusiona esas dos noticias en un texto de 500 palabras. Después agrega más texto relevante sobre el tema, hasta llegar a las 1000 palabras. La noticia que escribes debe estar optimizada para las siguientes palabras clave: {palabras_clave}. La densidad de cada una de esas palabras clave debe ser del 2%, es decir que por cada 100 palabras del texto, la palabra clave o un sinónimo aparece 2 veces. Asegúrate de que los datos que das en la noticia son reales y verídicos, por favor no sufras alucinaciones ni inventes datos que no son reales"

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3700  # Ajusta según la longitud deseada
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error al generar la publicación: {e}"

# Interfaz de Streamlit
st.title("Generador de Noticias Optimizadas")

tema = st.text_input("Ingresa el tema de la noticia:")
palabras_clave = st.text_input("Ingresa las palabras clave (separadas por comas):")
matiz = st.text_input("Ingresa el matiz que consideres oportuno añadir:")
fechahoy = st.text_input("Ingresa la fecha de hoy:")
urlnoticia1 = st.text_input("Ingresa la url de la noticia inicial:")
urlnoticia2 = st.text_input("Ingresa la url de la segunda noticia:")

if st.button("Generar Publicación"):
    publicacion = generar_publicacion_con_gpt(tema, palabras_clave, matiz, fechahoy, urlnoticia1, urlnoticia2)
    st.text_area("Publicación Generada:", publicacion, height=300)

