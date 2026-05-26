import os
from google import genai


def _client():
    key = os.getenv("GEMINI_API_KEY", "")
    return genai.Client(api_key=key)


async def ask_gemini(user_msg: str, history: list) -> str:
    try:
        client = _client()
        prompt = f"""You are GlucoBot, a professional diabetes-focused AI health assistant.
Give clear, concise answers (2-4 lines). Use simple language.
Always recommend consulting a doctor for serious medical concerns.

User: {user_msg}"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        return f"Sorry, I couldn't process that right now. Please try again. ({str(e)[:80]})"