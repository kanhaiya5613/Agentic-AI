from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "give me a joke about AI"}
    ]
)
print(response.choices[0].message.content)