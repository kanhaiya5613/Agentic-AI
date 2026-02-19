
from google import genai

client = genai.Client(
    api_key="AIzaSyCIlotwaRVzZs1TUwEBo3l4ZqIROxrE7lU"
)
# for model in client.models.list():
#     print(model.name)
# response = client.models.generate_content(
#     model="gemini-1.5-flash",
#     contents="Explain how AI works in a few words"
# )

# print(response.text)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="give me a joke about AI" 
    
)

print(response.text)