import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4

from models import Models
from summary import summarize_chunk

load_dotenv()

# Initialize the Models
models = Models()
embeddings = models.embeddings_model
llm = models.chat_model

# Constants
data_folder = "./data"
chunk_size = 1000
chunk_overlap = 200
check_interval = 10

def initialize_vector_store(collection_name="documents"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory="./db/chrome_langchain_db"
    )

default_vector_store = initialize_vector_store()

def ingest_file(file_path, vector_store=default_vector_store):
    if not file_path.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    loader = PyPDFLoader(file_path)
    loaded_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    documents = text_splitter.split_documents(loaded_documents)
    chunks_by_page = {}

    for i in range(len(documents)):
        page_num = documents[i].metadata['page']
        if page_num not in chunks_by_page:
            chunks_by_page[page_num] = 1
        else:
            chunks_by_page[page_num] += 1
        
        metadata = {
            "source": file_path,
            "page": page_num,
            "chunk_id": f"{page_num}:{chunks_by_page[page_num]}"
        }
        documents[i].metadata = metadata
        
        chunk_summary = summarize_chunk(documents[i].page_content)
        documents[i].metadata['summary'] = chunk_summary.summary
        documents[i].metadata['topic'] = chunk_summary.topic
        documents[i].metadata['keywords'] = chunk_summary.keywords
    
    vector_store.add_documents(documents)

def search_documents_with_score(query, vector_store=default_vector_store, k=4):
    return vector_store.similarity_search_with_score(query, k=k)

def return_chunk_by_id(chunk_id, vector_store=default_vector_store):
    chunks = vector_store.get(include=["metadatas", "documents"])
    metadatas = chunks['metadatas']
    documents = chunks['documents']
    
    for metadata, document in zip(metadatas, documents):
        if metadata['chunk_id'] == chunk_id:
            return {
                "metadata": metadata,
                "content": document
            }
    return None

def return_documents_summary(vector_store=default_vector_store):
    chunks = vector_store.get(include=["metadatas"])
    metadatas = chunks['metadatas']
    sorted_metadatas = sorted(metadatas, key=lambda x: (x['page'], int(x['chunk_id'].split(':')[1])))
    return sorted_metadatas

def condensed_metadata(vector_store=default_vector_store):
    metadata = return_documents_summary(vector_store)
    formatted_metadata = ""
    for data in metadata:
        formatted_metadata += f"Chunk ID: {data['chunk_id']}\n"
        formatted_metadata += f"Keywords for this chunk: {data['keywords']}\n"
        formatted_metadata += f"Topic of this chunk: {data['topic']}\n"
        formatted_metadata += f"Summary of this chunk: {data['summary']}\n"
        formatted_metadata += "---\n"
    return formatted_metadata