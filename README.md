# 🧪 Revisión de Calidad de Encuestas

Esta aplicación desarrollada en Streamlit permite revisar automáticamente la calidad metodológica y estructural de un instrumento de encuesta (en formato PDF, Excel o CSV), usando inteligencia artificial (OpenAI GPT-3.5).

---

## 🚀 Funcionalidades principales

✅ Carga de archivos PDF, CSV y Excel  
✅ Extracción automática de preguntas  
✅ Evaluación con IA basada en criterios metodológicos:  
- Claridad  
- Pertinencia  
- Tipo de pregunta  
- Sesgos  
- Redacción  
- Recomendación de mejora  
- Puntaje de 1 a 10  
✅ Generación automática de informe en PDF  
✅ Revisión estructural del instrumento (introducción, variables, escalas, etc.)

---

## 🛠 Requisitos

- Python 3.9+
- Cuenta en [OpenAI](https://platform.openai.com/) y tu propia API Key
- Cuenta en [Streamlit Cloud](https://streamlit.io/cloud) para desplegar

---

## 📦 Instalación local

```bash
git clone https://github.com/TU_USUARIO/REPO_NOMBRE.git
cd REPO_NOMBRE
pip install -r requirements.txt
streamlit run app.py
```

Crea un archivo llamado `.streamlit/secrets.toml` con este contenido:

```toml
OPENAI_API_KEY = "sk-..."
```

---

## ☁️ Despliegue en línea (Streamlit Cloud)

1. Sube este repositorio a GitHub.
2. Ve a [https://streamlit.io/cloud](https://streamlit.io/cloud).
3. Crea una nueva app y selecciona el archivo `app.py`.
4. En la pestaña **Secrets**, agrega tu clave API así:

```toml
OPENAI_API_KEY = "sk-..."
```

5. ¡Listo! Tu app estará en línea con una URL como:

```
https://tuusuario-nombreapp.streamlit.app
```

---

## 📄 Licencia

MIT License
