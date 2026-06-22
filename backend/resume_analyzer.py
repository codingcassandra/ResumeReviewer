import json
import re
from urllib import response
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return None

    return None



def normalize(skill):
    return (
        skill.strip()
        .lower()
        .replace("language", "")
        .replace("programming", "")
        .strip()
    )



def extract_resume_skills(text):
    """
    Extract skills directly from resume text so single-letter skills like 'C' are not lost.
    """
    tokens = re.split(r"[\n,•\-|/() ]+", text)

    skills = []
    for t in tokens:
        t = t.strip()
        if not t:
            continue

        if len(t) <= 30:
            skills.append(t.lower())

    return list(set(skills))



def extract_job_skills(job_text):
    return [
        line.strip().lstrip("-•* ").strip()
        for line in job_text.splitlines()
        if line.strip()
    ]


def analyze_match(resume_text, job_description):

    resume_text = resume_text[:4000]
    job_description = job_description[:4000]

    prompt = f"""
You are an expert ATS (Applicant Tracking System).

Extract and compare skills from resume vs job description.

Return ONLY valid JSON.

Return this EXACT format:

{{
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "verdict": "Strong Match | Moderate Match | Weak Match",
  "recommendation": "string"
}}

RULES:
- matched_skills must only include skills found in BOTH resume and job description
- missing_skills must only include skills in job description but NOT in resume
- DO NOT hallucinate skills

RECOMMENDATION RULES:
- MUST be EXACTLY 3 sentences
- Sentence 1: skill gap summary
- Sentence 2: ONE project idea
- Sentence 3: ONE specific course/certification (Coursera/Udemy/AWS/etc.)

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

    content = response.choices[0].message.content

    parsed = extract_json(content)

    if not parsed:
        return {
            "overall_match_score": 0,
            "skill_match_score": 0,
            "verdict": "Error",
            "matched_skills": [],
            "missing_skills": [],
            "recommendation": "Failed to parse AI response.",
            "raw_output": content
        }


    resume_skills = extract_resume_skills(resume_text)

    job_skills = [
        normalize(s)
        for s in extract_job_skills(job_description)
    ]

    resume_skills = [normalize(s) for s in resume_skills]

    job_skills = list(set(job_skills))
    resume_skills = list(set(resume_skills))


    matched_skills = [s for s in job_skills if s in resume_skills]
    missing_skills = [s for s in job_skills if s not in resume_skills]


    if len(job_skills) > 0:
        score = round((len(matched_skills) / len(job_skills)) * 100)
    else:
        score = 0


    if score >= 75:
        verdict = "Strong Match"
    elif score >= 50:
        verdict = "Moderate Match"
    else:
        verdict = "Weak Match"


    return {
        "overall_match_score": score,
        "skill_match_score": score,
        "verdict": verdict,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendation": parsed.get(
            "recommendation",
            "No recommendation provided."
        )
    }