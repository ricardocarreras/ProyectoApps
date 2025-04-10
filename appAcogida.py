import streamlit as st

import openai
from openai import OpenAI

# Configura tu clave API de OpenAI
import os

from dotenv import load_dotenv

# Cargar API KEY
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def generar_publicacion_con_gpt(nombre, puesto, cv, fecha, empresa):
    try:
        client = OpenAI(api_key=openai.api_key)

        prompt = f"imagina que eres un profesional en el departamento de recursos humanos, y prepara tres cosas relacionadas con el plan de acogida, la persona se llama {nombre}. Se incorpora como {puesto}, en la empresa {empresa}.con una experiencia detallada en este documento {cv}, y con fecha de incorporación el {fecha}. Crea tres documentos, un plan de acogida detallado, un correo de bienvenida desde rrhh y un borrador de la publicación de su incorporación en la intranet"

        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=3000  # Ajusta según la longitud deseada
        )
        return response.choices[0].text.strip()
    
    except Exception as e:
        return f"Error al generar la publicación: {e}"

# Interfaz de Streamlit
st.title("Generador de documentos para proceso de acogida")

puesto = st.text_input("Ingresa el perfil incorporado:")
cv = st.text_input("Ingresa en texto el cv:")
nombre = st.text_input("Ingresa el nombre de la persona:")
fecha = st.text_input("Ingresa la fecha de incorporación:")
empresa = st.text_input("Ingresa características de la empresa final donde trabajará:")


if st.button("Generar Publicación"):
    publicacion = generar_publicacion_con_gpt(nombre, puesto, cv, fecha, empresa)
    st.text_area("Publicación Generada:", publicacion, height=300)


