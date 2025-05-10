from typing import Any, Dict

import requests

from app.core.config import get_settings

settings = get_settings()


def generate_completion(prompt: str) -> Dict[str, Any]:
    url = f"{settings.gemini_api_url}?key={settings.gemini_api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }


    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()
