import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from dotenv import load_dotenv

load_dotenv()

class Models:
    def __init__(self):
        self.embeddings_model = OllamaEmbeddings(
            base_url= os.environ.get("OLLAMA_BASE_URL"),
            model=os.environ.get("OLLAMA_EMBEDDING_MODEL")
        )
        
        self.chat_model = ChatOllama(
            base_url= os.environ.get("OLLAMA_BASE_URL"),
            model=os.environ.get("OLLAMA_CHAT_MODEL"),
            temperature=0.1
        )

        self.summary_model = ChatOllama(
            base_url= os.environ.get("OLLAMA_BASE_URL"),
            model=os.environ.get("OLLAMA_SUMMARY_MODEL")
        )