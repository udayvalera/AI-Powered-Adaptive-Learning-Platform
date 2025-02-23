from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


QA_TEMPLATE = PromptTemplate.from_template(
    template="""You are a helpful AI assistant. Use the following context to answer the question.
    If you cannot find the answer in the context, say "I cannot find the answer in the provided context."

    Context:
    {context}

    Question:
    {question}

    Answer:"""
)

CHAT_TEMPLATE = ChatPromptTemplate.from_messages(
   [
       ("system", "You are a helpful AI assistant. Use the following context to answer the question."),
       ("human", "Use the user question {input} to answer the question. Use only the {context} to answer the question."),
   ]
)

SUMMARY_TEMPLATE = PromptTemplate.from_template(
    template="""You are tasked with identifying the main topic or key details of a fragmented chunk of text. Follow these instructions:

1. Context:
   - This chunk is part of a larger document, and the topic may be spread across multiple chunks.
   - The chunk might not contain the topic or full description. If the topic is missing or unclear, note that it's part of a larger discussion.
   - Some chunks might seem incomplete. Be aware that the full context may come from other parts of the document.

2. Instructions:
   - Provide a brief overview of the topic or key points of this chunk.
   - If the topic is not fully clear or described, mention that it’s part of a broader discussion, and the full topic may appear elsewhere.
   - Do not summarize the content in detail, just capture the main idea or focus.
   - If the chunk is cut off or incomplete, note that it's part of a larger conversation or that further details are missing.
   - Keep it concise and avoid unnecessary elaboration.

3. Format:
   - STRICTLY KEEP THE OUTPUT TO 1-2 SENTENCES.
   - The response should be a general statement about the topic, or a short description of the main idea.
   - Avoid long descriptions or redundant details. Focus on what the chunk is about.

4. Tone:
   - Match the tone of the original text (formal/informal, etc.)

Here is the chunk of text:

{text}

Please identify the main idea or topic of the chunk in 1-2 sentences. If the topic is incomplete or unclear, mention that it's part of a larger discussion. 
"""
)



