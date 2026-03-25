from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

# 📄 Load PDF
pdf_path = Path(__file__).parent / "Nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# ✂️ Split into chunks (optimized)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents=docs)

print(f"Total chunks: {len(chunks)}")

# 🧠 Local Embeddings (NO RATE LIMIT 🚀)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🗄️ Store in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
    force_recreate=True   # 🔥 ADD THIS
)

print("✅ Indexing completed successfully!")