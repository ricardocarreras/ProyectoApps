import streamlit as st

import openai
from openai import OpenAI

# Configura tu clave API de OpenAI
openai.api_key = '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'

def generar_publicacion_con_gpt(tema, palabras_clave, matiz):
    try:
        client = OpenAI(api_key=openai.api_key)

        prompt = f"Escribe una publicación de 1000 palabras sobre {tema}. Considera que {matiz}. La publicación debe estar optimizada ante los buscadores, desde un punto de vista SEO, para las siguientes palabras clave: {palabras_clave}. La densidad de cada una de esas palabras clave debe ser del 2%, es decir que por cada 100 palabras del texto, la palabra clave o un sinónimo aparece 2 veces. Por favor incluye para cada palabra clave un hipervínculo hacia una página web relevante como la wikipedia u otra de alta credibilidad, cuyo texto ancla (del hipervínculo) sea en cada caso las palabras clave"

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3600  # Ajusta según la longitud deseada
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error al generar la publicación: {e}"

# Interfaz de Streamlit
st.title("Generador de Publicaciones con GPT-3.5")

tema = st.text_input("Ingresa el tema de la publicación:")
palabras_clave = st.text_input("Ingresa las palabras clave (separadas por comas):")
matiz = st.text_input("Ingresa el matiz que quieras añadir:")

if st.button("Generar Publicación"):
    publicacion = generar_publicacion_con_gpt(tema, palabras_clave, matiz)
    st.text_area("Publicación Generada:", publicacion, height=300)


