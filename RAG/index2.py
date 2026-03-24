from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

pdf_path = Path(__file__).parent / "Nodejs.pdf"

# Load this file in python program
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()
docs[0]

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
texts = text_splitter.split_documents(documents=docs)

print(f"Total pages: {len(docs)}")
print(f"Total chunks: {len(texts)}")
print(texts[0].page_content)