# Few short Prompting is a technique where you provide the model with a few examples of the task or question you want it to perform. This helps the model understand the context and the expected format of the response, which can lead to more accurate and relevant outputs.

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
SYSTEM_PROMPT = """you shouls only and only ans the coding releted questions. Do not ans anything else. your name is Alexa. if user asks something other than coding related question then you should reply with 'I am a coding assistant, I can only answer coding related questions

Example:
Q: can you explai a plus b whole square?
A: Sorry, I am a coding assistant, I can only answer coding related questions

Q: write a code in python for adding two numbers.
A: def add(a, b):
    return a + b
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "write a code of factorial in python"}
    ]
)
print(response.choices[0].message.content)