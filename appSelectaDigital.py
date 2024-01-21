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

def generar_publicacion_con_gpt(puesto, experiencia, tecnología, nivel, idioma, datos, empresa):
    try:
        client = OpenAI(api_key=openai.api_key)

        prompt = f"imagina que eres un profesional en selección de perfiles tecnológicos y trabajas para la consultora de selección especializada Selecta Digital, que se dedica a seleccionar candidatos para sus clientes finales. En este caso tu cliente {empresa}. Tenemos que gestionar un proceso de selección. Buscamos un {puesto}, con una experiencia relevante de {experiencia} años en total. Debe dominar esta tecnología {tecnología} y tener un nivel {nivel} del idioma {idioma}. Considera además que {datos}. Recuerda que lo contratará para trabajar la empresa {empresa}. Debes generar los siguientes documentos siempre pensando que Selecta Digital no contrata al candidato, lo contrata la empresa final. 1. Quiero 10 preguntas relevantes para una entrevista, con las respuestas correctas. Quiero que 5 de esas preguntas sean técnicas, relativas a {tecnología}, y el resto de lo demás. Si el puesto requiere un nivel alto de un idioma, crea dos de las preguntas y respuestas en ese idioma. 2. Quiero además que creas un texto para publicar en la web de selecta digital, en la página de ofertas, con una descripción detallada de este proceso concreto de selección. 3. Y también quiero un resumen de esta publicación detallada, para redes sociales. 4. Crea también el texto de un correo electrónico para enviar por correo electrónico a candidatos interesados. 5. Y finalmente dame una cadena de texto booleana (Boolean string) para buscar este perfil en linkedin recruiter"

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3000  # Ajusta según la longitud deseada
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error al generar la publicación: {e}"

# Interfaz de Streamlit
st.title("Generador de documentos para proceso de selección de Selecta Digital")

puesto = st.text_input("Ingresa el perfil que buscas:")
experiencia = st.text_input("Ingresa los años de experiencia que debería tener como mínimo:")
tecnología = st.text_input("Ingresa la tecnología que debe dominar (si son varias, separadas por comas):")
idioma = st.text_input("Ingresa el idioma que debe dominar (si son varios, separados por comas):")
nivel = st.text_input("Ingresa el nivel que debe tener en ese idioma:")
datos = st.text_input("Ingresa cualquier otro dato relevante:")
empresa = st.text_input("Ingresa características de la empresa final donde trabajará:")


if st.button("Generar Publicación"):
    publicacion = generar_publicacion_con_gpt(puesto, experiencia, tecnología, nivel, idioma, datos, empresa)
    st.text_area("Publicación Generada:", publicacion, height=300)


