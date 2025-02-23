from pathlib import Path
from openai import OpenAI

from ingest import initialize_vector_store, return_chunk_by_id
from model import Models
from prompts import TRANSCRIPT_TEMPLATE

models = Models
transcript_model = models.transcript_model
chain = TRANSCRIPT_TEMPLATE | transcript_model

def generate_transcript(chunk_ids, filename: str) -> str:
    vector_store = initialize_vector_store(filename)
    formatted_text = ""
    for chunk_id in chunk_ids:
        chunk = return_chunk_by_id(chunk_id, vector_store)
        formatted_text += chunk.page_content + "\n"

    transcript = chain.invoke({"text": formatted_text})
    return transcript


def generate_audio(text: str, node_id, filename: str) -> Path:
    client = OpenAI()
    filename = f"audio_{filename}_{node_id}.mp3"
    speech_file_path = Path(__file__).parent / filename
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    
    response.stream_to_file(speech_file_path)
    return speech_file_path