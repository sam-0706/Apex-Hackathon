import os
import json
import time
from functools import lru_cache
import openai  # Make sure you have: pip install openai
from dotenv import load_dotenv  # Make sure you have: pip install python-dotenv

# ─── LOAD ENV VARIABLES ────────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❗ ERROR: OPENAI_API_KEY not found. Check your .env file!")
    exit(1)

LLM_MODEL = "gpt-4o"

# ─── PROMPTS ───────────────────────────────────────────────────────────────
SYS_PROMPT = """\
You are a highly reliable recruiter AI system.

Your task is to strictly evaluate the match between a job description (JD) and a candidate’s resume.

Instructions:
- Carefully compare the JD and the resume for alignment on:
    • Required skills and technologies
    • Relevant work experience
    • Role responsibilities and domain fit
    • Educational or certification match
    • Location or work preferences (if specified)

Scoring:
- Provide only a **numeric score** between 0 and 10:
    • 0 = no fit at all
    • 10 = perfect match
    • Use decimal precision (e.g., 7.5).

Output Format:
- Strictly return **only** a JSON object like:
  { "score": 7.5 }

Important:
- Do not include any explanations, notes, or extra text.
- Do not apologize or say you cannot answer.
- Never skip the JSON response.

This JSON will be directly consumed by downstream systems that require clean, machine-readable output.
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

# ─── SCORING FUNCTION ──────────────────────────────────────────────────────
def ai_score(jd_txt: str, res_txt: str) -> float:
    t0 = time.time()
    try:
        resp = _client().chat.completions.create(
            model       = LLM_MODEL,
            messages    = [
                { "role": "system", "content": SYS_PROMPT },
                { "role": "user",   "content": USER_PROMPT_TMPL.format(jd=jd_txt, rs=res_txt) }
            ],
            max_tokens  = 30,
            temperature = 0.0,
        ).choices[0].message.content.strip()

        val = json.loads(resp)["score"]
        final_score = max(0.0, min(10.0, float(val))) / 10.0   # normalize 0–1
        print(f"[AI scorer] raw: {val}, normalized: {final_score:.3f}")
        return final_score

    except Exception as e:
        print(f"[AI scorer] fallback (error: {e}) → returning neutral 0.5")
        return 0.5  # fallback neutral score

    finally:
        print(f"[AI scorer] took {time.time() - t0:.1f}s")

# ─── DEMO TEST RUN ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Example JD and resume (replace with your own)
    jd_text = """\
Job Title: Generative AI Engineer
Location: Hyderabad, Telangana, India
Posted: 3 days ago
Applicants: Over 100 applicants

Workplace Type: On-site (Matches your job preferences)
Job Type: Full-time (Matches your job preferences)

About the Job
We are seeking a highly motivated and innovative Generative AI Engineer to join our team and drive the exploration of cutting-edge AI capabilities. You will be at the forefront of developing solutions using Generative AI technologies, primarily focusing on Large Language Models (LLMs) and foundation models, deployed on either AWS or Azure cloud platforms.

This role involves rapid prototyping, experimentation, and collaboration with various stakeholders to assess the feasibility and potential impact of GenAI solutions on our business challenges. If you are passionate about the potential of GenAI and enjoy hands-on building in a fast-paced environment, this is the role for you.

Responsibilities

Develop GenAI Solutions: Develop and rapidly iterate on GenAI solutions leveraging LLMs and other foundation models available on AWS and/or Azure platforms.

Cloud Platform Implementation: Utilize relevant cloud services (e.g., AWS SageMaker, Bedrock, Lambda, Step Functions; Azure Machine Learning, Azure OpenAI Service, Azure Functions) for model access, deployment, and data processing.

Explore GenAI Techniques: Experiment with and implement techniques like Retrieval-Augmented Generation (RAG), evaluating the feasibility of model fine-tuning or other adaptation methods for specific PoC requirements.

API Integration: Integrate GenAI models (via APIs from cloud providers, OpenAI, Hugging Face, etc.) into prototype applications and workflows.

Data Handling for AI: Prepare, manage, and process data required for GenAI tasks, such as data for RAG indexes, datasets for evaluating fine-tuning feasibility, or example data for few-shot prompting.

Documentation & Presentation: Clearly document PoC architectures, implementation details, findings, limitations, and results for both technical and non-technical audiences.

Requirements

Overall, 2–4 years of experience.

Expert in Python with advanced programming and concepts.

Solid understanding of Generative AI concepts, including LLMs, foundation models, prompt engineering, embeddings, and common architectures (e.g., RAG).

Demonstrable experience working with at least one major cloud platform (AWS or Azure).

Hands-on experience using cloud-based AI/ML services relevant to GenAI (e.g., AWS SageMaker, Bedrock; Azure Machine Learning, Azure OpenAI Service).

Experience interacting with APIs, particularly AI/ML model APIs.

Bachelor’s degree in Computer Science, AI, Data Science, or equivalent practical experience.

Company: ValueMomentum
Location: Hyderabad, Telangana, India (On-site)

Other Notes

Easy Apply option available.

You can Save this job posting or Apply directly.

Meet the hiring team: Nagamani Mallarapu, Talent Acquisition Associate (Job poster).

Explore Premium features for AI-powered advice, resume tailoring, and exclusive tools to assess fit, position yourself, and fast-track your job search.

"""

    resume_text = """\
Shivaji Chatterjee
 9706965211 | shivajichatterjee98@gmail.com | linkedin.com/in/shivaji-chatterjee-7ba0721b5
 Professional Summary
 Data Scientist and GenAI Developer with hands-on experience building scalable AI systems using Python,
 FastAPI, Neo4j, and Qdrant. Specialized in LLM-based chatbot development, Retrieval-Augmented
 Generation (RAG), semantic search, and prompt engineering. Designed and deployed knowledge graph
 pipelines and document intelligence tools leveraging OpenAI, Redis, and AWS Bedrock.
 Professional Experience
 Associate Data Scientist
 Datalabs AI Pvt Ltd
 Jul 2024– Present
 • Designed an LDA-powered query classifier that increased topic relevance by 35% for document classification.
 • Constructed a hybrid RAG system with Qdrant and Neo4j, reducing semantic query response time by 45%.
 Hyderabad
 • Launched the iframe-based Product Search Bot, deployed across 3 clients, increasing product discovery by 40%.
 • Developed FastAPI services to interpret OpenAI responses into JSON-based filters for Qdrant retrieval.
 • Built a feedback loop with Redis for capturing user reactions, improving recommendation performance by 25%.
 • Implemented a GraphRAG-style pipeline to persist entities and relationships in Parquet, accelerating Neo4j ingestion by
 3x.
 • Fine-tuned LLaMA prompt templates for academic paper graph extraction, enhancing accuracy by 28%.
 • Authored policy documentation for AI regulations in Europe, USA, and MENA to support enterprise compliance.
 • Created an interview automation tool using Azure TTS/STT and GPT-3.5 to generate and store Q&A sessions.
 • Deployed a resume parsing pipeline via AWS Bedrock Vision, achieving 98% accuracy in contact detail extraction.
 Data Science Intern
 Datalabs Corporation
 Oct 2023– Jun 2024
 Hyderabad
 • Automated document parsing workflows using OCR and FastAPI, reducing manual review effort by 60%.
 • Integrated a Gemini + GPT-3.5 chatbot to streamline internal knowledge retrieval and minimize resolution times.
 • Managed GitHub branching strategies to enhance code quality and reduce conflicts by 70%.
 Data Science Intern
 Rubix
 Feb 2023– Jun 2023
 Bangalore
 • Optimized pipelines for processing structured and unstructured datasets, reducing training time by 40%.
 • Built statistical models to address business-specific KPIs, leading to a 15% increase in forecast accuracy.
 Technical Skills
 • Languages: Python, C, C++, TypeScript, JavaScript
 • AI & ML:Scikit-learn, TensorFlow, FLAML, LDA, ANN, CNN, Prompt Engineering, LLMs (GPT, LLaMA, Gemini)
 • Frameworks: FastAPI, Flask, Streamlit, Next.js (React), RESTful APIs
 • Data & Storage: Qdrant, Neo4j, Redis, MySQL, Parquet, JSON
 • Tools: Docker, Git, GitHub, Postman, VSCode, RedisInsight
 • Web Development: HTML, CSS, Tailwind CSS, iframe Embedding
 • OCR & Vision: AWS Bedrock Vision APIs, Optical Character Recognition
 • Web Scraping: BeautifulSoup, Scrapy
Education
 Bachelor of Technology in Mechanical Engineering
 Girijananda Chowdhury Institute of Management and Technology, Tezpur, India
 Professional Development
 Aug 2016– Jul 2020
 Certified Data Scientist
 Datamites
 Nov 2022– Present
 • Completed a full-stack data science program covering ML algorithms, data analysis, and model deployment.
 • Practiced applied data science using Python, Scikit-learn, and statistical visualization tools.
 Certifications
 • Data Science Foundation– IABAC
 • Certified Data Scientist– NASSCOM
 Languages
 • English, Hindi, Bengali, Assamese
 Declaration
 • I hereby declare that the above information is true and correct to the best of my knowledge and belief."""

    print("Scoring JD vs. Resume...")
    score = ai_score(jd_text, resume_text)
    print(f"\nFinal AI Score (0–10): {round(score * 10, 2)}")
