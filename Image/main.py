import os
import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Fetch image bytes
image_url = "https://images.pexels.com/photos/37423901/pexels-photo-37423901.jpeg"
image_response = httpx.get(image_url)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "Generate a caption for this image",
        types.Part.from_bytes(
            data=image_response.content,
            mime_type=image_response.headers.get("content-type", "image/jpeg"),
        ),
    ],
)

print("Response:", response.text)