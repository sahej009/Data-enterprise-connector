from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document

# 1. Connect to our database as the ADMIN (since we are writing new data)
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/crm_data"

# 2. Load the "Math Engine" (Embedding Model)
print("Loading embedding model... (this might take a few seconds to download on the first run)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3. Create our mock unstructured text document
company_strategy = """
Initech Corporate Strategy 2026:
Our primary objective this year is to transition our software products into the cloud.
We are focusing heavily on AI-driven analytics to help our manufacturing and logistics clients.
"""

docs = [Document(page_content=company_strategy, metadata={"source": "Strategy_2026.pdf"})]

# 4. Connect to the Vector Store and upload the document
print("Connecting to vector database and uploading document...")
vector_store = PGVector(
    embeddings=embeddings,
    collection_name="company_docs",
    connection=DATABASE_URL,
    use_jsonb=True,
)

vector_store.add_documents(docs)

print("Success! Unstructured text has been converted to vectors and saved to PostgreSQL! 🎯")