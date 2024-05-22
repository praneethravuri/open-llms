from langchain_community.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_and_construct_retrieval(dataset_name, page_content_column, model_path, model_kwargs, encode_kwargs):
    # Create a loader instance
    loader = HuggingFaceDatasetLoader(dataset_name, page_content_column)
    
    # Load the data
    data = loader.load()
    
    # Split the text into documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(data)
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name=model_path,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    # Initialize FAISS vector store with the documents and embeddings
    db = FAISS.from_documents(docs, embeddings)
    
    return db
