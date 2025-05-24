# config/config.py

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# -------------------------------
# Hardcoded Config Values
# -------------------------------
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("open_api_key"),
)

qdrant_client = QdrantClient(
    url="https://504712c7-28c6-428d-9c36-85de639f9f09.us-west-2-0.aws.cloud.qdrant.io:6333",
    api_key=os.getenv("qdrant_api"),
)

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    api_key=os.getenv("open_api_key"),
)
# print("loading done")
