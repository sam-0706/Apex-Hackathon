import time
import json
from typing import List, Tuple, Any, Dict

# Use your existing prompt_template from "prompts.py"

# Use the recommended imports from `langchain_openai` to address deprecation warnings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from qdrant_client import QdrantClient, models


###############################################################################
# ONE-TIME INITIALIZATIONS (EMBEDDINGS, QDRANT CLIENT, LLM)
# These are created once at module load time to reduce repeated overhead.
###############################################################################

from config.config import llm, embeddings, qdrant_client

###############################################################################
# HELPER FUNCTIONS
###############################################################################

# ----------------- PROMPT BUILDER ------------------

def _build_prompt(chat_history: List[str], current_question: str, retrieved_context: str) -> List[Dict[str, str]]:
    """
    Returns a list of messages for the ChatOpenAI model.
    Includes a system message with context + chat history + current question.
    """
    messages = []

    # System prompt with context from Qdrant
    messages.append({
        "role": "system",
        "content": f"""You are an intelligent HR assistant trained on company policy documents.
Use the following context to answer the user's question as accurately and concisely as possible.

### Context:
{retrieved_context}

Respond ONLY using the context above. If the answer is not found, say:
"tell something relavant to the company TechNova Solutions Pvt. Ltd and at the end mention this for futher assitance,please mail hr@comapny.com"
"""
    })

    # Add conversation history
    for msg in chat_history:
        messages.append({"role": "user", "content": msg})

    # Append the current user query
    messages.append({"role": "user", "content": current_question})

    return messages

# ----------------- LLM RESPONSE WRAPPER ------------------

def _get_llm_response(chat_history: List[str], current_question: str) -> Tuple[str, float]:
    """
    Queries Qdrant for relevant content, builds system context,
    sends a structured chat to the LLM, and returns the raw response and response time.
    """
    # 1. Embed the current question
    query_vector = embeddings.embed_query(current_question)

    # 2. Retrieve matching chunks from Qdrant
    hits = qdrant_client.query_points(
        collection_name="bot",
        query=query_vector,
        limit=5
    ).points

    # 3. Concatenate retrieved context from payloads
    retrieved_context = "\n\n".join(hit.payload.get("page_content", "") for hit in hits)

    # 4. Construct chat-style prompt messages
    prompt_messages = _build_prompt(chat_history, current_question, retrieved_context)

    # 5. Call the LLM
    start_time = time.monotonic()
    llm_response = llm.invoke(prompt_messages)
    end_time = time.monotonic()

    llm_time = end_time - start_time
    llm_raw_text = getattr(llm_response, "content", str(llm_response)).strip()

    return llm_raw_text, llm_time


# import your existing _get_llm_response function from your module if needed
# # from your_module_name import _get_llm_response

# # Sample chat history (can be empty or filled)
# chat_history = [
#     "What is the company's leave policy?",
#     "How many casual leaves are allowed per year?"
# ]

# # New question to get an answer for
# current_question = "how many leaves are provided"

# # Call the LLM function and print the result
# response, duration = _get_llm_response(chat_history, current_question)

# print("🧠 LLM Response:\n", response)
# print(f"⏱️ Time Taken: {duration:.2f} seconds")


