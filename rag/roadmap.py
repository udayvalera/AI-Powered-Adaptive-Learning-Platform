from langchain_core.output_parsers import PydanticOutputParser

#Model Imports
from typing import List
from pydantic import BaseModel, Field


#Load Environment Variables
import os
from dotenv import load_dotenv
load_dotenv()

#Local Imports
from ingest import condensed_metadata
from prompts import ROADMAP_TEMPLATE
from models import Models

#Initialize the Models
model = Models()
roadmap_model = model.roadmap_model

#Roadmap Models
class RoadmapNode(BaseModel):
    """
    Represents a single node in a learning roadmap with detailed information about a topic.
    """
    node_id: int = Field(..., description="Unique identifier for the roadmap node")
    topic: str = Field(..., description="Title or main subject of the learning node")
    related_chunks: List[str] = Field(default_factory=list, description="References or related content chunks")
    summary: str = Field(..., description="Brief overview of the topic's content")
    difficulty: str = Field(..., description="Difficulty level of the topic")
    estimated_time: str = Field(..., description="Approximate time required to learn the topic")

class LearningRoadmap(BaseModel):
    """
    Represents a complete learning roadmap consisting of multiple nodes.
    """
    roadmap: List[RoadmapNode] = Field(..., description="List of learning nodes in the roadmap")


parser = PydanticOutputParser(pydantic_object=LearningRoadmap)

prompt = ROADMAP_TEMPLATE.partial(
    format_instructions=parser.get_format_instructions()
)

chain = prompt | roadmap_model | parser

def create_roadmap(condensed_metadata):
    try:
        roadmap = chain.invoke({"text" : condensed_metadata})
        return roadmap.model_dump()
    except Exception as e:
        print(f"Error creating roadmap: {e}")
        return None

# Example usage
if __name__ == "__main__":
    print("Creating Roadmap...")
    text = condensed_metadata()
    roadmap = create_roadmap(text)
    for node in roadmap.roadmap:
        print(f"Node {node.node_id}: {node.topic}")
        print(f"Summary: {node.summary}")
        print(f"Difficulty: {node.difficulty}")
        print(f"Estimated Time: {node.estimated_time}")
        print(f"Related Chunks: {node.related_chunks}")
        print("-" * 50)  # Separator between nodes
