import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role":"user",
        "content":[
            { "type":"text","text":"Generate a caption for this image in anout 50 words"},
            {"type":"image_url","image_url":{"url":"https://images.pexels.com/photos/4974920/pexels-photo-4974920.jpeg"}}
        ]}
    ]
)
print("Response:- ", response.choices[0].message.content)