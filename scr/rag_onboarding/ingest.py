# ingest.py
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DOCS_PATH = "doc"

BASE_DIR = Path(__file__).resolve().parent
VECTORSTORE_PATH = BASE_DIR.parent.parent / "vectorstore"

loader = DirectoryLoader(
    DOCS_PATH,
    glob="**/*.md",
    show_progress=True
)

documents = loader.load()

for doc in documents:
    path = doc.metadata.get("source", "")
    if "domains" in path:
        doc.metadata["doc_type"] = "domain"
    elif "tables" in path:
        doc.metadata["doc_type"] = "table"
    else:
        doc.metadata["doc_type"] = "glossary"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

splits = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_documents(splits, embeddings)
vectorstore.save_local(VECTORSTORE_PATH)

print("✅ Vectorstore creado correctamente")
