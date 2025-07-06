import os
import requests
from dotenv import load_dotenv

load_dotenv()  # ✅ Ensure .env gets loaded

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY is not loaded from .env file.")
else:
    print("✅ GROQ_API_KEY loaded:", GROQ_API_KEY[:10] + "..." + GROQ_API_KEY[-5:])  # Masked

def call_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "compound-beta-mini",  # ✅ This model exists per your last test
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        if "choices" not in data:
            print("⚠️ Groq response missing 'choices':", data)
            raise RuntimeError("Groq returned no result. Check prompt or limits.")
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print("❌ API request failed:", e)
        raise RuntimeError("Failed to connect to Groq API. Check your internet or key.")
    except Exception as e:
        print("❌ Unexpected Groq response:", res.text)
        raise
