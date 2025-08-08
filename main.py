from fastapi import FastAPI, Request
from pydantic import BaseModel
from rag_pipeline import load_rag_pipeline

app = FastAPI()
rag_pipeline = load_rag_pipeline()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    print("Pergunta recebida:", request.question)
    prompt = request.question 
    response = rag_pipeline.run(prompt)
    print("Processamento concluído")
    if isinstance(response, dict) and "result" in response:
        answer = response["result"]
    elif isinstance(response, str):
        answer = response
    else:
        answer = str(response)

    answer = answer.strip()
    return {"answer": answer}