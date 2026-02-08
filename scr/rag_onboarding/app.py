import streamlit as st
from query import ask_rag  # Tu función del backend

# Configuración de la página
st.set_page_config(page_title="💬 RAG Onboarding", page_icon="🤖", layout="wide")

# Título
st.title("💬 RAG Onboarding")
st.markdown("Haz preguntas sobre tus documentos y obtén respuestas con RAG.")

# Historial de preguntas/respuestas en sesión
if "history" not in st.session_state:
    st.session_state.history = []

# Input de la pregunta
question = st.text_input("Pregunta:", "")

# Botón para enviar la pregunta
ask_button = st.button("Preguntar")

if ask_button and question:
    with st.spinner("Pensando... 🤔"):
        try:
            # Llamada al backend
            result = ask_rag(question)
            
            # Guardar en historial
            st.session_state.history.append({
                "question": question,
                "answer": result
            })

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# Mostrar historial
if st.session_state.history:
    st.subheader("Historial de preguntas")
    for entry in reversed(st.session_state.history):
        st.markdown(f"**Q:** {entry['question']}")
        st.markdown(f"**A:** {entry['answer']}")
        st.markdown("---")