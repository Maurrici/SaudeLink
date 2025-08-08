import pandas as pd
import faiss
import json
from sentence_transformers import SentenceTransformer
import os

CSV_PATH = "data/processed/patients_register_documents.csv"
FAISS_PATH = "data/processed/vectorized_documents.faiss"
METADATA_PATH = "data/processed/metadata.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv(CSV_PATH)

embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, FAISS_PATH)

metadata = df[["patient_id", "start_date", "end_date"]].to_dict(orient="records")
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("Vetorização concluída e arquivos salvos.")
