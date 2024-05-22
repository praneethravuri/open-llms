from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import importlib
from app.data_loader import load_and_construct_retrieval
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain import HuggingFacePipeline
from langchain.chains import RetrievalQA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Question(BaseModel):
    question: str

# Load dataset and construct retrieval system
dataset_name = "databricks/databricks-dolly-15k"
page_content_column = "context"
model_path = "sentence-transformers/all-MiniLM-l6-v2"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': False}

db = load_and_construct_retrieval(dataset_name, page_content_column, model_path, model_kwargs, encode_kwargs)

@app.get("/api/server-status")
def read_root():
    return {"message": "Server is running"}

@app.post("/api/ask")
async def ask_question(question: Question):
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-l6-v2", padding=True, truncation=True, max_length=512)

    # Define the question-answering pipeline
    question_answerer = pipeline(
        "question-answering", 
        model="Intel/dynamic_tinybert", 
        tokenizer=tokenizer,
        device=0  # Ensure it uses the specified device (e.g., GPU)
    )

    # Create an instance of the HuggingFacePipeline
    llm = HuggingFacePipeline(
        pipeline=question_answerer,
        model_kwargs={"temperature": 1.0, "max_length": 512},
    )

    # Create a retriever object from the 'db' with a search configuration
    retriever = db.as_retriever(search_kwargs={"k": 4})

    # Create a question-answering instance using the RetrievalQA class
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever, return_source_documents=False)

    # Generate the answer
    retrieved_docs = retriever.get_relevant_documents(question.question)
    context = " ".join([doc.page_content for doc in retrieved_docs])

    # Ensure the context and question are passed correctly to the QA pipeline
    response = question_answerer(question=question.question, context=context)
    
    return {"answer": response['answer']}
