import requests
from typing import Dict
from config.config import API_KEY, LLM_MODEL, API_BASE_URL

class LLMService:
    def __init__(self):
        self.headers = {
            "Authorization": f'Bearer {API_KEY}',
        }
        
    def get_response(self, prompt: str) -> str:
        params = {
            "messages": [
                {
                    "role": 'user',
                    "content": prompt
                }
            ],
            "model": LLM_MODEL
        }
        
        response = requests.post(
            API_BASE_URL,
            headers=self.headers,
            json=params,
            stream=False
        )
        
        res = response.json()
        if 'choices' in res and len(res['choices']) > 0:
            return res['choices'][0]['message']['content'].strip()
        else:
            raise ValueError("Failed to get a valid response from the API.")