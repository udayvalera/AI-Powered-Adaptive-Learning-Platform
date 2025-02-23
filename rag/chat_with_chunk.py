from models import Models
from ingest import return_chunk_by_id, initialize_vector_store
from prompts import CHUNK_TEMPLATE

model = Models()
chunk_model = model.chunk_model
chain = CHUNK_TEMPLATE | chunk_model

def format_related_chunks(node, vector_store):
    formatted_text = ""
    for chunk_id in node["related_chunks"]:
        chunk = return_chunk_by_id(vector_store=vector_store, chunk_id=chunk_id)
        if chunk:
            formatted_text += f"Chunk ID: {chunk_id}\n"
            formatted_text += f"Content: {chunk['content']}\n"
            formatted_text += "---\n"
    return formatted_text

def chat(text, node, filename):
    vector_store = initialize_vector_store(filename)
    context = format_related_chunks(node, vector_store)
    response = chain.invoke({"user_query": text, "context": context})
    return response

if __name__ == "__main__":
    node = {
        "node_id": 1,
        "topic": "Transformer Architecture Fundamentals",
        "related_chunks": ["0:1", "0:2", "1:5", "2:1", "8:2"]
    }
    text = "What is the purpose of the Chunk?"
    filename = "338_Introduction_To_Law_Eng_L1.pdf"
    response = chat(text, node, filename)
    print(response)



