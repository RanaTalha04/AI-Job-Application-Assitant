import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "models/gemini-flash-latest"


def generate_email(resume_text, jd_text):
    prompt = f"""
You are a personal assistant that applies for jobs ON MY BEHALF.

Candidate name: Muhammad Talha

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

STRICT RULES:
- NO markdown
- NO ```json
- NO explanations
- Output ONLY raw JSON
- Subject must NOT be empty
- Extract job title & company from JD

Return JSON in THIS EXACT FORMAT:

{{
  "subject": "Application for <Job Title> | Muhammad Talha",
  "body": "Full professional email ready to send",
  "resume_suggestions": [
    "Suggestion 1",
    "Suggestion 2"
  ]
}}
"""

    response = client.models.generate_content(model=MODEL, contents=prompt)

    raw = response.text.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # hard fallback so subject is NEVER empty
        data = {
            "subject": "Job Application | Muhammad Talha",
            "body": raw,
            "resume_suggestions": [],
        }

    # Hard guarantees
    if not data.get("subject"):
        data["subject"] = "Job Application | Muhammad Talha"

    data.setdefault("body", "")
    data.setdefault("resume_suggestions", [])

    return data
