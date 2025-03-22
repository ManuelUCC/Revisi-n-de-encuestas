import streamlit as st
import pandas as pd
import openai
import PyPDF2
import io
import base64
from fpdf import FPDF

# --- Configura tu clave API de OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Revisión de Calidad de Encuestas", layout="wide")
st.title("📋 Evaluador de Calidad de Encuestas")
st.write("Sube tu archivo de preguntas para revisar su calidad metodológica y estructural.")

uploaded_file = st.file_uploader("Carga tu archivo de encuesta (CSV, Excel o PDF)", type=["csv", "xlsx", "pdf"])
preguntas_extraidas = []
texto_completo = ""
evaluaciones = []

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        preguntas_extraidas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        preguntas_extraidas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        texto_completo = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        posibles_preguntas = texto_completo.split("\n")
        for linea in posibles_preguntas:
            if '?' in linea or linea.strip().lower().startswith("¿"):
                preguntas_extraidas.append(linea.strip())

    if preguntas_extraidas:
        st.subheader("📄 Preguntas extraídas")
        st.write(f"Se han detectado {len(preguntas_extraidas)} posibles preguntas.")
        for i, pregunta in enumerate(preguntas_extraidas):
            st.markdown(f"{i+1}. {pregunta}")

        st.subheader("🔎 Revisión automática por IA")

        criterio_eval = """ 
Evalúa cada pregunta de encuesta considerando los siguientes criterios de calidad:

1. Claridad: ¿Está formulada de forma comprensible y sin ambigüedades?
2. Pertinencia: ¿Está alineada con los objetivos de la investigación y variables definidas?
3. Tipo de pregunta: ¿Es adecuada según el indicador (abierta, cerrada, Likert, etc.)?
4. Sesgos: ¿Evita preguntas capciosas, sugestivas o dobles?
5. Redacción: ¿Está bien redactada y sin errores gramaticales?
6. Recomendación de mejora, si aplica.
7. Valoración global: Puntaje del 1 al 10.
"""

        for i, pregunta in enumerate(preguntas_extraidas):
            with st.expander(f"Pregunta {i+1}: {pregunta}"):
                prompt = f"""
{criterio_eval}

Pregunta: \"{pregunta}\"
Proporciona una evaluación breve (máx. 100 palabras), una sugerencia concreta de mejora y asigna un puntaje del 1 al 10.
"""
                response = client.chat.completions.create(

                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                evaluacion = response["choices"][0]["message"]["content"]
                st.markdown(evaluacion)
                evaluaciones.append((pregunta, evaluacion))

        st.subheader("📤 Generar informe PDF")

        if st.button("Descargar informe"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, "Informe de Evaluación de Encuesta\n\n")
            for idx, (pregunta, evaluacion) in enumerate(evaluaciones):
                pdf.multi_cell(0, 10, f"Pregunta {idx+1}: {pregunta}\nEvaluación: {evaluacion}\n")
            pdf_output = io.BytesIO()
            pdf.output(pdf_output)
            b64_pdf = base64.b64encode(pdf_output.getvalue()).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="informe_encuesta.pdf">📥 Haz clic aquí para descargar el informe</a>'
            st.markdown(href, unsafe_allow_html=True)

    else:
        st.warning("No se detectaron preguntas en el archivo.")

    st.subheader("📊 Evaluación general del instrumento")
    st.markdown("Esta sección revisa el diseño general de la encuesta:")
    st.markdown("- 📌 **Introducción**: ¿Está clara la finalidad, la confidencialidad y el consentimiento informado?")
    st.markdown("- 📋 **Sección demográfica**: ¿Incluye edad, género, programa, semestre?")
    st.markdown("- 🧪 **Variables e indicadores**: ¿Las preguntas corresponden con variables claramente definidas?")
    st.markdown("- 🔁 **Secuencia lógica**: ¿Las preguntas están organizadas de forma progresiva?")
    st.markdown("- ⏱️ **Extensión**: ¿La encuesta es razonablemente breve?")
    st.markdown("- 📎 **Escalas**: ¿Se usan escalas Likert, numéricas y opciones múltiples correctamente?")

    st.success("Este módulo está listo y conectado con OpenAI. Puedes usarlo para generar informes reales.")

else:
    st.info("Esperando que subas un archivo con tus preguntas.")

st.markdown("---")
st.caption("Desarrollado con base en la Guía para la Creación de Encuestas, Introducción a las Variables y ejemplos reales de encuestas universitarias.")
