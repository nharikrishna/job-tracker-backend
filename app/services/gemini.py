import re
import json

import pdfplumber

from app.external import gemini


def build_prompt(resume_text: str, jd_text: str) -> str:
    return f"""
You are a resume matching assistant. Compare the following resume and job description.

Return:
1. A match score out of 100
2. Suggested keywords or areas for improvement
3. A short remark or summary comment on how well the resume aligns with the job

Respond only in this **pure JSON** format (no markdown or code blocks):

{{
  "score": <int>,
  "suggested_keywords": [<string>, ...],
  "remarks": <string>
}}

Resume:
{resume_text}

Job Description:
{jd_text}
""".strip()


def extract_text(file) -> str:
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def run_resume_matching(resume_file, jd_file) -> tuple[int, list[str], str]:
    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    result = generate_resume_match(resume_text, jd_text)
    score = result.get("score", 0)
    suggestions = result.get("suggested_keywords", [])
    remarks = result.get("remarks", "")
    return score, suggestions, remarks


def parse_response(response: dict) -> dict:
    try:
        raw_text = response["candidates"][0]["content"]["parts"][0]["text"]
        clean_text = raw_text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text.removeprefix("```json").strip()

        if clean_text.endswith("```"):
            clean_text = clean_text.removesuffix("```").strip()

        return json.loads(clean_text)
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        raise ValueError("Failed to parse Gemini response") from e



def generate_resume_match(resume_text: str, jd_text: str) -> dict:
    prompt = build_prompt(resume_text, jd_text)
    response = gemini.generate_completion(prompt)
    return parse_response(response)
