from .AI_scoring_agent import score_resume_vs_jd
from .semantic_agent import semantic_score_jd_resume
from .tf_idf_agent import bert_similarity,tfidf_similarity

def score_resume(job_description, resume):
    # Calculate scores using different methods
    semantic_score = semantic_score_jd_resume(job_description, resume)
    tfidf_score = tfidf_similarity(job_description, resume)
    bert_score = bert_similarity(job_description, resume)
    ai_score = score_resume_vs_jd(job_description, resume)

    ai_score_normalized = ai_score / 10.0

    # Define weights (must sum to 1.0)
    weights = {
        "ai": 0.5,
        "tfidf": 0.2,
        "bert": 0.15,
        "semantic": 0.15
    }

    # Compute weighted average score (0 to 1 scale)
    weighted_score = (
        ai_score_normalized * weights["ai"] +
        tfidf_score * weights["tfidf"] +
        bert_score * weights["bert"] +
        semantic_score * weights["semantic"]
    )

    # Optionally scale to 0–10 for readability
    final_score_out_of_10 = round(weighted_score * 10, 2)

    return {
        "semantic_score": semantic_score,
        "tfidf_score": tfidf_score,
        "bert_score": bert_score,
        "ai_score": ai_score,
        "final_score": final_score_out_of_10
    }