import requests

import os
from dotenv import  load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")





def generate_prediction(
    glucose,
    haemoglobin,
    cholesterol
):

    prompt = f"""
    Patient Report:

    Glucose: {glucose}
    Haemoglobin: {haemoglobin}
    Cholesterol: {cholesterol}

    Predict possible health condition.
    Give short medical remark.
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]