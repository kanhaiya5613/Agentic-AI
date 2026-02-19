from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a Maths Proffessorr so only reply maths releted probleums. if the query is not related to maths then reply with 'I am a Maths Proffessorr so only reply maths releted probleums'"},
        {"role": "user", "content": "(a+b)^2"}
    ]
)
print(response.choices[0].message.content)