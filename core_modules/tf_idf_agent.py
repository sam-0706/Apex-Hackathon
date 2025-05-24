import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  
def tfidf_similarity(doc1: str, doc2: str) -> float:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity_matrix[0][0])


def bert_similarity(doc1: str, doc2: str) -> float:
    # Encode documents to get embeddings
    embeddings = model.encode([doc1, doc2], convert_to_tensor=True)

    # Compute cosine similarity
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    normalized_similarity = (similarity.item() + 1) / 2
    return normalized_similarity

# doc1 = "Machine learning is a field of artificial intelligence."
# doc2 = "Artificial intelligence includes machine learning as a subset."
# start_time=time.time()
# print(f"BERT Similarity: {bert_similarity(doc1, doc2):.4f}")
# print("time",time.time()-start_time)
