
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Force reload settings from .env
load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

if not api_key:
    raise ValueError("Gemini API key missing!")

print("Selected model:", model, flush=True)
print("Initializing client...", flush=True)

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=60000,
        retry_options=types.HttpRetryOptions(
            attempts=1
        )
    )
)

print("Sending request...", flush=True)

try:
    response = client.models.generate_content(
        model=model,
        contents="Say HELLO in one word."
    )

    print("\nSUCCESS!", flush=True)
    print("Response:", response.text, flush=True)

except Exception as e:
    print("\nREQUEST FAILED:", repr(e), flush=True)
