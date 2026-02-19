# Zero short prompting is a technique where you provide the model with a task or question without any examples or additional context. The model is expected to generate a response based solely on its understanding of the task and its pre-trained knowledge.
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)
SYSTEM_PROMPT = "You are a Maths Proffessorr so only reply maths releted probleums. if the query is not related to maths then reply with 'I am a Maths Proffessorr so only reply maths releted probleums'"
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "GIVE THE CODE OF HELLO WORLD IN PYTHON"}
    ]
)
print(response.choices[0].message.content)