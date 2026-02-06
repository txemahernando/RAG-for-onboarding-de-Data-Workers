
# ============================
# query.py
# ============================
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, SystemMessage

# Cargar variables de entorno
load_dotenv()

VECTORSTORE_PATH = "vectorstore.index"

# 1. Cargar vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# Retriever con filtro por tipo de documento
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

# 2. Modelo LLM
llm = ChatOpenAI(temperature=0)

# 3. Función de pregunta
def ask_rag(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    messages = [
        SystemMessage(
            content=(
                "Eres un asistente de onboarding de datos. "
                "Responde SOLO usando la información del contexto. "
                "Si no sabes la respuesta, dilo claramente."
            )
        ),
        HumanMessage(
            content=f"Contexto:\n{context}\n\nPregunta: {question}"
        )
    ]

    response = llm.invoke(messages)
    return response.content


# 4. CLI interactivo
if __name__ == "__main__":
    print("💬 RAG Onboarding (escribe 'salir' para terminar)")

    while True:
        q = input("Pregunta: ")
        if q.lower() in ["salir", "exit", "quit"]:
            break
        answer = ask_rag(q)
        print("\n🧠 Respuesta:\n", answer)
        print("\n" + "-" * 50 + "\n")


