# app.py
import streamlit as st
from query import ask_rag

# Configuración de la página
st.set_page_config(page_title="💬 RAG Onboarding", page_icon="🤖", layout="wide")

st.title("💬 RAG Onboarding")
st.write("Escribe tu pregunta sobre la documentación y la base de datos, y la RAG te responderá.")

# Inicializar historial en session_state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Input del usuario
user_question = st.text_input("Pregunta:")

if user_question:
    with st.spinner("Buscando respuesta..."):
        try:
            answer = ask_rag(user_question)  # Llamada al backend
        except Exception as e:
            answer = f"❌ Error al procesar la pregunta: {e}"

    # Guardar en historial
    st.session_state['history'].append(("Usuario", user_question))
    st.session_state['history'].append(("RAG", answer))

# Mostrar historial
for role, msg in st.session_state['history']:
    if role == "Usuario":
        st.markdown(f"**{role}:** {msg}")
    else:
        st.markdown(f"**{role}:** {msg}")
