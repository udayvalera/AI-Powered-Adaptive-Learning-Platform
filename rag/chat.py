from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


from models import Models
from prompts import CHAT_TEMPLATE

models = Models()
embeddings = models.embeddings_model
llm = models.chat_model

vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chrome_langchain_db"
)

retriever = vector_store.as_retriever(kwargs={"k":3})
# print(retriever)
combined_docs_chain = create_stuff_documents_chain(llm, CHAT_TEMPLATE)

retriever_chain = create_retrieval_chain(retriever, combined_docs_chain)
test = retriever_chain.invoke({"input" : "When attention should not be used?"})

if test:
    print(test["answer"])
