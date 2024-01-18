import streamlit as st

import openai
from openai import OpenAI

# Configura tu clave API de OpenAI
openai.api_key = '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'

def generar_publicacion_con_gpt(tema, palabras_clave, matiz):
    try:
        client = OpenAI(api_key=openai.api_key)

        prompt = f"Escribe una noticia periodística de 1000 palabras sobre {tema}. Considera que {matiz}. Para crear el comienzo de la noticia busca en internet sobre ese mismo tema tres(3) noticias cuya fecha de publicación (escrita en la noticia) sea de las últimas 48 horas y que sean relevantes. Comienza la creación de tu nueva noticia por un resumen de 400 palabras de esas 3 noticias que has encontrado en internet. Escribes el resto de la noticia con texto relevante, hasta llegar a las 1000 palabras. La noticia que creas debe estar optimizada para las siguientes palabras clave: {palabras_clave}. La densidad de cada una de esas palabras clave debe ser del 2%, es decir que por cada 100 palabras del texto, la palabra clave o un sinónimo aparece 2 veces. Asegúrate de que los datos que das en la noticia son reales y verídicos, por favor no sufras alucinaciones ni inventes datos que no son reales"

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

if st.button("Generar Publicación"):
    publicacion = generar_publicacion_con_gpt(tema, palabras_clave, matiz)
    st.text_area("Publicación Generada:", publicacion, height=300)


