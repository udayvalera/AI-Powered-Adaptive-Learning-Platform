from langchain_core.output_parsers import PydanticOutputParser

#Model Imports
from typing import List
from pydantic import BaseModel, Field

#Load Environment Variables
import os
from dotenv import load_dotenv
load_dotenv()

#Local Imports
from ingest import return_chunk_by_id
from prompts import QUIZ_TEMPLATE
from models import Models

#Initialize the Models
model = Models()
quiz_model = model.quiz_model

#Quiz Models
class Question(BaseModel):
    """
    Represents a single question in a quiz with detailed information.
    """
    question_id: int = Field(..., description="Unique identifier for the question")
    question: str = Field(..., description="Question text")
    options: List[str] = Field(..., description="List of answer options")
    correct_answer: str = Field(..., description="Correct answer to the question")
    explanation: str = Field(..., description="Explanation of the correct answer")
    related_chunks: List[str] = Field(..., description="References or related content chunks")

class Quiz(BaseModel):
    """
    Represents a complete quiz consisting of multiple questions.
    """
    quiz: List[Question] = Field(..., description="List of questions in the quiz")


parser = PydanticOutputParser(pydantic_object=Quiz)

prompt = QUIZ_TEMPLATE.partial(
    format_instructions=parser.get_format_instructions()
)

chain = prompt | quiz_model | parser

def format_related_chunks(node, vector_store):
    node_topic = node["topic"]
    related_chunks = node["related_chunks"]
    
    formatted_text = f"Topic: {node_topic}\n---\n"
    
    for chunk_id in related_chunks:
        chunk = return_chunk_by_id(chunk_id, vector_store)
        if chunk:
            formatted_text += f"Chunk ID: {chunk_id}\n"
            formatted_text += f"Content: {chunk['content']}\n"
            formatted_text += "---\n"
    return formatted_text

def create_quiz(node, filename):
    vector_store = initialize_vector_store(collection_name=filename)
    formatted_text = format_related_chunks(node, vector_store)
    try:
        quiz = chain.invoke({"text" : formatted_text})
        return quiz.model_dump()
    except Exception as e:
        print(f"Error creating quiz: {e}")
        return None

if __name__ == "__main__":
    node = {
    "node_id": 1,
    "topic": "Transformer Architecture Fundamentals",
    "related_chunks": ["0:1", "0:2", "1:5", "2:1", "8:2"],
    "summary": "Core architecture of Transformer models including encoder-decoder structure, self-attention layers, and parallelization advantages over RNNs/CNNs.",
    "difficulty": "Beginner",
    "estimated_time": "1.5 hours"
  }

    formatted_text = format_related_chunks(node)
    quiz = create_quiz(formatted_text)
    for question in quiz["quiz"]:
        print(f"Question: {question['question']}")
        print(f"Options: {question['options']}")
        print(f"Correct Answer: {question['correct_answer']}")
        print(f"Explanation: {question['explanation']}")
        print(f"Related Chunks: {question['related_chunks']}")
        print("-" * 50)
    



