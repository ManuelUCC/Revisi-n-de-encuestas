import streamlit as st
import pandas as pd
import openai
import PyPDF2
import io
import base64
from fpdf import FPDF

# Configura la clave API de OpenAI
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Evaluador de Calidad de Encuestas", page_icon="📊", layout="wide")

st.markdown("""
<div style='display: flex; align-items: center;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/5/5e/Universidad_Cooperativa_de_Colombia_logo.png' width='80' style='margin-right: 20px;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>Evaluador de Calidad de Encuestas</h1>
</div>
""", unsafe_allow_html=True)

st.info("Bienvenido/a al Evaluador de Encuestas. Sube tus preguntas y genera un informe de calidad metodológica.")

uploaded_file = st.file_uploader("📎 Carga tu archivo de encuesta (CSV, Excel o PDF)", type=["csv", "xlsx", "pdf"])
preguntas = []

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        preguntas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        preguntas = df.iloc[:, 0].dropna().tolist()
    elif uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        texto = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        preguntas = [linea.strip() for linea in texto.split("\n") if '?' in linea or linea.strip().startswith("¿")]

    if preguntas:
        st.subheader("📄 Preguntas detectadas")
        st.write(f"Se han detectado {len(preguntas)} preguntas.")

        criterio = """
Evalúa la siguiente pregunta de encuesta bajo estos criterios:
1. Claridad
2. Pertinencia
3. Tipo de pregunta
4. Sesgos
5. Redacción
6. Sugerencia de mejora
7. Puntaje global del 1 al 10
"""

        evaluaciones = []
        puntajes = []

        with st.spinner("Evaluando preguntas con IA..."):
            for i, pregunta in enumerate(preguntas):
                prompt = f"{criterio}\nPregunta: {pregunta}\n"
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                resultado = response.choices[0].message.content
                evaluaciones.append((pregunta, resultado))

                linea = [l for l in resultado.split("\n") if "Puntaje" in l]
                try:
                    score = int("".join([c for c in linea[-1] if c.isdigit()]))
                    puntajes.append(score)
                except:
                    puntajes.append(0)

        st.markdown(f"📊 **Puntaje promedio:** {sum(puntajes)/len(puntajes):.1f}/10")

        for i, (preg, eval) in enumerate(evaluaciones):
            with st.expander(f"Pregunta {i+1}: {preg}"):
                st.markdown(eval)

        if st.button("📥 Descargar informe PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, "Informe de Evaluación de Encuesta", ln=True)
            for i, (preg, eval) in enumerate(evaluaciones):
                pdf.multi_cell(0, 10, f"Pregunta {i+1}: {preg}\nEvaluación:\n{eval}\n")
            output = io.BytesIO()
            pdf.output(output)
            b64 = base64.b64encode(output.getvalue()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="informe_encuesta.pdf">📄 Descargar Informe</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("No se encontraron preguntas.")
else:
    st.info("Carga un archivo para comenzar.")

st.markdown("---")
st.caption("Universidad Cooperativa de Colombia · Proyecto de Evaluación Automatizada de Encuestas con IA.")
