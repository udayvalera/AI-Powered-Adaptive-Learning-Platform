import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4


from models import Models
from prompts import SUMMARY_TEMPLATE

load_dotenv()

#Initialize the Models
models = Models()
embeddings = models.embeddings_model
llm = models.chat_model
summary_llm = models.summary_model

#Initialize the summary chain
summary_chain = SUMMARY_TEMPLATE | summary_llm

#Constants
data_folder = "./data"
chunk_size = 1000
chunk_overlap = 200
check_interval = 10

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chrome_langchain_db"
)

def ingest_file(file_path):
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
        # Track chunks per page
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
        # Add chunk_id to metadata
        documents[i].metadata = metadata
        
        print("-"*100)
        print(f"CHUNK : {i+1}")
        # print(documents[i].page_content)
        # print(documents[i].metadata)
        chunk_summary = summary_chain.invoke({"text": documents[i].page_content})

        documents[i].metadata['summary'] = chunk_summary.content
        # print(chunk_summary)
    
    vector_store.add_documents(documents)

def search_documents_with_score(query, vector_store=vector_store, k=4):
    """
    Perform a similarity search with relevance scores.
    
    Args:
        vector_store: The initialized vector store
        query (str): The search query
        k (int, optional): Number of top results to return. Defaults to 4.
    
    Returns:
        List of tuples containing (document, similarity_score)
    """
    return vector_store.similarity_search_with_score(query, k=k)

def return_documents_summary():
    chunks = vector_store.get(include=["metadatas"])
    metadatas = chunks['metadatas']

    # Sort metadata by page number and chunk_id
    sorted_metadatas = sorted(metadatas, key=lambda x: (x['page'], int(x['chunk_id'].split(':')[1])))

    # for metadata in sorted_metadatas:
    #     print("-"*100)
    #     print(f"Page: {metadata['page']}")
    #     print(f"Chunk ID: {metadata['chunk_id']}")
    #     print(f"Summary: {metadata['summary']}")
    #     print("-"*100)
    return sorted_metadatas