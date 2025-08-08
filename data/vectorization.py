import pandas as pd
import json
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

CSV_PATH = "data/processed/patients_register_documents.csv"
VECTORSTORE_PATH = "data/processed/vectorized_documents"
INDEX_NAME = "faiss_index"

# Carregar CSV
df = pd.read_csv(CSV_PATH)

# Textos e metadados
texts = df["text"].tolist()
metadatas = df[["patient_id", "start_date", "end_date"]].to_dict(orient="records")

# Embeddings LangChain
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Criar FAISS com LangChain
vectorstore = FAISS.from_texts(texts=texts, embedding=embedding_model, metadatas=metadatas)

# Salvar no formato LangChain
vectorstore.save_local(VECTORSTORE_PATH, index_name=INDEX_NAME)

print("Vetorização concluída e índice salvo no formato LangChain.")
