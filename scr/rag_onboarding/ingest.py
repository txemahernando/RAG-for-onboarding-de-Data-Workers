# ============================
# ingest.py
# ============================
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Cargar variables de entorno
load_dotenv()

DOCS_PATH = "doc"
VECTORSTORE_PATH = "vectorstore.index"

# 1. Cargar documentos con metadata
loader = DirectoryLoader(
    DOCS_PATH,
    glob="**/*.md",
    show_progress=True
)
documents = loader.load()

# Añadir metadata según la ruta
for doc in documents:
    path = doc.metadata.get("source", "")
    if "domains" in path:
        doc.metadata["doc_type"] = "domain"
    elif "tables" in path:
        doc.metadata["doc_type"] = "table"
    else:
        doc.metadata["doc_type"] = "glossary"

# 2. Dividir documentos
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)
splits = text_splitter.split_documents(documents)

# 3. Crear embeddings
embeddings = OpenAIEmbeddings()

# 4. Crear y guardar vectorstore
vectorstore = FAISS.from_documents(splits, embeddings)
vectorstore.save_local(VECTORSTORE_PATH)

print("✅ Ingesta completada y vectorstore guardado")

