# embedding.py (OpenAI v1.0 이상 호환)
import os
from openai import OpenAI
from typing import List
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text: str) -> List[float]:
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )
    return response.data[0].embedding

def embed_sentences(sentences: List[str]) -> List[List[float]]:
    return [get_embedding(s) for s in sentences]
