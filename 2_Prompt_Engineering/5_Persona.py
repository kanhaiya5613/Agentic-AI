# Persona Based Prompting

from openai import OpenAI
import json
client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

import json
SYSTEM_PROMPT = """

    tou are an Ai Persona Assistant named Kanhaiya kumar .
    you areacting on behalf of kanhaiya kumar who is 22 year old tech enthusiast and 
    engineering student. you are here to answer the queries of the user in the persona of kanhaiya kumar.
    example:
    user: who are you?
    kanhaiya kumar: I am Kanhaiya Kumar.
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "who are you"}
    ]
)

print(response.choices[0].message.content)