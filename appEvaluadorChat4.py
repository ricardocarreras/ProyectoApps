import streamlit as st
import os
from PyPDF2 import PdfReader
import pandas as pd
import re
from dotenv import load_dotenv
from openai import OpenAI

# Cargar API KEY
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Evaluador de Candidatos de Selecta Digital", layout="wide")

from PIL import Image

# Mostrar logo
logo_path = "Logo Selecta Digital  FINAL octubre 20202.jpg"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, use_container_width=False, width=250)

st.title("📄 Evaluador de Candidatos de Selecta Digital")

# Descripción del puesto
descripcion_puesto = st.text_area("1. Descripción del puesto de trabajo", height=200)

# Subida de CVs
cvs = st.file_uploader("2. Sube uno o varios CVs en PDF", type="pdf", accept_multiple_files=True)

# Función de evaluación con GPT-4 Turbo
def evaluar_cv_gpt4(texto_cv: str, descripcion_puesto: str) -> str:
    prompt = f"""
Eres un reclutador experto en tecnología. Evalúa el siguiente CV respecto a esta descripción de puesto:

Descripción del puesto:
{descripcion_puesto}

Devuelve un informe con:
1. Puntuación de adecuación al perfil, expresada como 'Puntuación de adecuación al perfil: X/10'.
2. Fortalezas del candidato.
3. Debilidades o carencias.
4. 5 preguntas clave para la entrevista.
5. Resumen final.

CV:
{texto_cv}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Eres un experto en selección de personal tecnológico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error evaluando el CV: {e}"

# Evaluación
if st.button("Evaluar Candidatos") and descripcion_puesto and cvs:
    st.header("📊 Resultados de la Evaluación")
    resultados = []

    for cv in cvs:
        reader = PdfReader(cv)
        texto_cv = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        informe = evaluar_cv_gpt4(texto_cv, descripcion_puesto)

        # Extraer puntuación
        puntuacion_match = re.search(r"Puntuación de adecuación al perfil:\s*(\d+(?:\.\d+)?)/10", informe)
        puntuacion = float(puntuacion_match.group(1)) if puntuacion_match else None

        # Extraer resumen final correctamente
        resumen_match = re.search(r"Resumen final\s*:\s*(.*?)(?:\n\s*\n|$)", informe, re.IGNORECASE | re.DOTALL)
        resumen = resumen_match.group(1).strip() if resumen_match else "-"

        resultados.append({
            "Nombre": cv.name.replace(".pdf", ""),
            "Puntuación": puntuacion,
            "Resumen": resumen,
            "Informe": informe
        })

    # Mostrar informes individuales
    for r in resultados:
        st.subheader(f"👤 Candidato: {r['Nombre']} ({r['Puntuación']}/10)" if r['Puntuación'] else f"👤 Candidato: {r['Nombre']}")
        st.markdown(r["Informe"])

    # Mostrar tabla comparativa
    st.header("📈 Tabla Comparativa")
    df = pd.DataFrame(resultados)

    if not df.empty and "Puntuación" in df.columns:
        df_ordenado = df[["Nombre", "Puntuación", "Resumen"]].sort_values(by="Puntuación", ascending=False, na_position="last")
        st.dataframe(df_ordenado, use_container_width=True)
    else:
        st.warning("No se pudo generar la tabla comparativa.")
