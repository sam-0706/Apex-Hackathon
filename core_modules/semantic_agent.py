import openai
import numpy as np
from dotenv import load_dotenv
import os
import numpy as np

# Load environment variables from .env file
load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(text, model="text-embedding-3-large"):
    response = openai.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_score_jd_resume(jd_text, resume_text, model="text-embedding-3-large"):
    embedding_jd = get_embedding(jd_text, model=model)
    embedding_resume = get_embedding(resume_text, model=model)
    return cosine_similarity(embedding_jd, embedding_resume)


