import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(user_input):
    if not GEMINI_API_KEY:
        return "Error: API Key missing."
    try:
        # 2026 Ultra-Fast Stable Model
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents=user_input,
            config={
                "system_instruction": "You are Phantom, a witty and advanced AI assistant developed by Shibjyoti Roy."
            }
        )
        return response.text
    except Exception as e:
        return f"Brain Error: {str(e)}"