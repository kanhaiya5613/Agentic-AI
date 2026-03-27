from openai import OpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
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


def process_query(query: str):
    print("Searching Chuncks", query)
    search_results = vector_db.similarity_search(query=query)

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
        { "role":"user", "content":query}
    ]
)
    print(f"🤖: {response.choices[0].message.content}")
    return response.choices[0].message.content

