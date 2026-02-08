import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# 🔥 Desactivar proxies incompatibles con OpenAI SDK
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

# ============================
# Cargar variables de entorno
# ============================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("❌ OPENAI_API_KEY no encontrada en el entorno")

# ============================
# Paths
# ============================
try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    # Si __file__ no existe (por ejemplo, ejecución interactiva en VS Code)

    BASE_DIR = Path(os.getcwd())
VECTORSTORE_PATH = BASE_DIR.parent.parent / "vectorstore"

# ============================
# Lazy initialization
# ============================
def get_rag_components():
    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    return retriever, llm


# ============================
# RAG
# ============================
def ask_rag(question: str) -> str:
    retriever, llm = get_rag_components()

    # Buscar documentos
    docs = retriever._get_relevant_documents(question, run_manager=None)



    if not docs:
        return "No se encontró información relevante."

    # Construir contexto
    context = "\n".join(doc.page_content for doc in docs)

    prompt = f"""
    Usa la siguiente información para responder la pregunta.

    Contexto:
    {context}

    Pregunta:
    {question}
    """
    # Llamada segura al LLM
    try:
        response = llm.call_as_llm(prompt=f"Contexto:\n{context}\nPregunta: {question}")
        return response
    except AttributeError:
        # fallback para versiones antiguas
        response = llm.invoke(f"Contexto:\n{context}\nPregunta: {question}")
        return response.content if hasattr(response, "content") else response
    
# ============================
# Consola interactiva
# ============================
if __name__ == "__main__":
    print("💬 RAG Console - Haz tus preguntas sobre los documentos")
    print("Escribe 'salir' para terminar\n")
    
    while True:
        question = input("Pregunta: ").strip()
        if question.lower() in ["salir", "exit", "quit"]:
            break
        if not question:
            continue
        
        print("Pensando... 🤔")
        answer = ask_rag(question)
        print(f"Respuesta: {answer}\n")