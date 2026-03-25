from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

# Take user input
user_Query = input("Ask Something: ")

# Relevant chunks from the vector db
search_results = vector_db.similarity_search(query=user_Query)

context = "\n\n\n".join(
    [
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
        for result in search_results
    ]
)

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user query based on available context retrived from a PDF file along with page_contents and page number. 

you should only answer the user based on the following context and navigate the user to open right page number to know more.

Context: {context}
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content":SYSTEM_PROMPT},
        { "role":"user", "content":user_Query}
    ]
)

print(f"🤖: {response.choices[0].message.content}")