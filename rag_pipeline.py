# rag_chain.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import os

def load_rag_pipeline():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.load_local(
        folder_path="data/processed/vectorized_documents",
        embeddings=embedding_model,
        index_name="faiss_index",
        allow_dangerous_deserialization=True
    )

    hf_pipeline = pipeline("text-generation", model="tiiuae/falcon-7b-instruct")
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    rag_pipeline = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff"
    )

    return rag_pipeline
