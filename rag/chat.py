from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from models import Models
from prompts import CHAT_TEMPLATE
from ingest import initialize_vector_store
import re

def filter_think_tags(response_content):
    """
    Filters out <think> tags and their content from the response text.
    
    Args:
        response_content (str): Text containing potential <think> tags
        
    Returns:
        str: Text with <think> tags and their content removed
    """
    pattern = r'<think>.*?</think>*'
    filtered_content = re.sub(pattern, '', response_content, flags=re.DOTALL)
    return filtered_content.strip()


def chat_with_docs(query: str, collection_name: str = "documents") -> str:
    models = Models()
    embeddings = models.embeddings_model
    llm = models.chunk_model

    vector_store = initialize_vector_store(collection_name=collection_name)
    retriever = vector_store.as_retriever(kwargs={"k":3})
    combined_docs_chain = create_stuff_documents_chain(llm, CHAT_TEMPLATE)
    retriever_chain = create_retrieval_chain(retriever, combined_docs_chain)

    response = retriever_chain.invoke({"input": query})
    filtered_response = filter_think_tags(response["answer"])
    return response["answer"] if response else ""

if __name__ == "__main__":
    response = chat_with_docs("When attention should not be used?")
    if response:
        print(response)