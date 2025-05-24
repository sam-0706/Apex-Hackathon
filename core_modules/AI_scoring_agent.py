import os
import json
import time
from functools import lru_cache
import openai  # pip install openai
from dotenv import load_dotenv  # pip install python-dotenv

# ─── ENV SETUP ─────────────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("❗ ERROR: OPENAI_API_KEY not found. Check your .env file!")

LLM_MODEL = "gpt-4o"

# ─── PROMPT SETUP ──────────────────────────────────────────────────────────
SYS_PROMPT = """\
You are an expert recruiter AI system.

Your task is to strictly evaluate how well a candidate’s resume matches the provided job description (JD).

Scoring Rubric:
- Score 9–10: Perfect fit. All required skills, experience, and qualifications clearly match. No major gaps.
- Score 7–8: Strong fit. Most major requirements are met; only minor gaps.
- Score 5–6: Moderate fit. Partial match; noticeable gaps in key areas.
- Score 3–4: Weak fit. Only a few overlaps; several major mismatches or missing qualifications.
- Score 0–2: No fit. Almost no alignment between resume and JD.

Scoring Rules:
- Be conservative and strict.
- If required skills, years of experience, or qualifications are missing or unclear, rate lower.
- Do not assume or guess matches based on vague descriptions.
- Apply penalties when a resume lacks clearly stated alignment to the JD.

Output Format:
Return only the JSON:
{ "score": N }

Where N is a numeric score between 0 and 10. You may use decimal precision (e.g., 7.5).

Important:
- Do not include explanations, comments, or extra text.
- Do not apologize or say you cannot answer.
- Always return the JSON response exactly as instructed.
"""

USER_PROMPT_TMPL = """\
Evaluate the following candidate match.

JOB DESCRIPTION:
\"\"\"{jd}\"\"\"

RESUME:
\"\"\"{rs}\"\"\"

Remember: only return a JSON like {{ "score": N }} where N is between 0 and 10.
"""

# ─── OPENAI CLIENT ─────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _client():
    return openai.OpenAI(api_key=OPENAI_API_KEY)

# ─── PUBLIC FUNCTION ───────────────────────────────────────────────────────
def score_resume_vs_jd(jd_txt: str, res_txt: str) -> float:
    """
    Compares a job description and a resume using GPT-4o.
    Returns:
        final_score: float (0–10)
    """
    t0 = time.time()
    try:
        resp = _client().chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": USER_PROMPT_TMPL.format(jd=jd_txt, rs=res_txt)}
            ],
            max_tokens=30,
            temperature=0.0,
        ).choices[0].message.content.strip()

        val = json.loads(resp)["score"]
        raw_score = float(val)
        normalized_score = max(0.0, min(10.0, raw_score)) / 10.0
        final_score = round(normalized_score * 10, 2)

    except Exception as e:
        print(f"[AI scorer] Fallback error: {e} → returning neutral 5.0")
        final_score = 5.0

    finally:
        print(f"[AI scorer] Total time: {time.time() - t0:.1f}s")

    return final_score


# ─── RUN AS STANDALONE SCRIPT ──────────────────────────────────────────────
# if __name__ == "__main__":
#     print("Scoring JD vs. Resume...")

#     jd_text = "Paste your JD here..."
#     resume_text = "Paste your resume here..."

#     final_score = score_resume_vs_jd(jd_text, resume_text)
#     print(f"\n✅ Final Score (0–10): {final_score}")
