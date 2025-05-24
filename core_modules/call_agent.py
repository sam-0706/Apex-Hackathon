### core/call_agent.py
import time
import requests
from fastapi import HTTPException

BLAND_API_URL = "https://api.bland.ai/v1/calls"

# Replace with your actual authorization token
HEADERS = {
    "Authorization": "org_d588f127eb7da49665573d3978a3b18d2f174d6e8f30b65fe4bfc131a55472899f2d036407c3cb575f2069",
    "Content-Type": "application/json"
}

def run_call_agent(phone_number: str) -> dict:
    call_payload = {
        "phone_number": phone_number,
        "task": (
            "You are Alex from HR at Meta. Call the candidate to discuss their recent application "
            "for the job position. Greet the candidate and ask the following details clearly, waiting "
            "for their response before proceeding to the next:\n\n"
            "1. Current location\n"
            "2. Current designation\n"
            "3. Notice period\n"
            "4. Current CTC\n"
            "5. Expected CTC\n\n"
            "End the call by saying 'All the best'."
        ),
        "voice": "june",
        "model": "base"
    }

    try:
        response = requests.post(BLAND_API_URL, json=call_payload, headers=HEADERS)
        response.raise_for_status()
        call_id = response.json().get("call_id")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error initiating call: {e}")

    for _ in range(30):
        try:
            status_response = requests.get(f"{BLAND_API_URL}/{call_id}", headers=HEADERS)
            status_response.raise_for_status()
            if status_response.json().get("queue_status") == "complete":
                break
            time.sleep(10)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error checking call status: {e}")
    else:
        raise HTTPException(status_code=500, detail="Call did not complete within expected time.")

    analyze_payload = {
        "goal": "Extract the following details from the call:",
        "questions": [
            ["What is the candidate's current location?", "string"],
            ["What is the candidate's current designation?", "string"],
            ["What is the candidate's notice period?", "string"],
            ["What is the candidate's current CTC?", "string"],
            ["What is the candidate's expected CTC?", "string"]
        ]
    }

    try:
        analyze_response = requests.post(f"{BLAND_API_URL}/{call_id}/analyze", json=analyze_payload, headers=HEADERS)
        analyze_response.raise_for_status()
        answers = analyze_response.json().get("answers", [])
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing call: {e}")

    return {
        "current_location": answers[0] if len(answers) > 0 else None,
        "current_designation": answers[1] if len(answers) > 1 else None,
        "notice_period": answers[2] if len(answers) > 2 else None,
        "current_ctc": answers[3] if len(answers) > 3 else None,
        "expected_ctc": answers[4] if len(answers) > 4 else None
    }

