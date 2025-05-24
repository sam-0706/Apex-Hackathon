from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
from .Ats_driver import score_resume

# Load environment variables from .env file
load_dotenv(override=True)
mongo_uri = os.getenv("MONGODB_URL")
client = MongoClient(mongo_uri,tls=True,tlsCAFile=certifi.where())
def getalljobs() :
    db = client["jobs"]
    collection = db["job_id_mapping"]
    documents = list(collection.find({}, {"_id": 0,"job_id": 1, "job_name": 1}))
    return documents

def get_resumes_by_job(job_id):
    db = client["jobs"]
    collection = db["job_id_mapping"]
    documents = list(collection.find({"job_id": job_id}, {"_id": 0}))  # Exclude _id

    # Sort resumes by final_score descending
    for doc in documents:
        if "resumes" in doc:
            doc["resumes"].sort(
                key=lambda x: x.get("score", {}).get("final_score", 0), reverse=True
            )

    return documents[0]["resumes"]


def add_job(job_id, job_description):
    db = client["jobs"]
    collection = db["job_id_mapping"]
    collection.update_one(
        {"job_id": job_id},  
        {"$set": {"job_description": job_description}},  
        upsert=True  
    )
    return {"message": "Job added successfully"}


def add_resume(job_id, new_resume, name):
    db = client["jobs"]
    collection = db["job_id_mapping"]
    doc = collection.find_one({"job_id": job_id})
    if doc:
        resumes = doc.get("resumes", [])
        resumes.append({"resume":new_resume,"name":name,"score": score_resume(doc.get("job_description", ""), new_resume)})
    else:
        resumes = [new_resume]
    collection.update_one(
        {"job_id": job_id},
        {"$set": {"resumes": resumes}},
        upsert=True
    )

    return {"message": "Resume added successfully"}
