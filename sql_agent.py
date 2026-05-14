import os
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

# --- NEW IMPORTS FOR VECTOR SEARCH ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_core.tools import create_retriever_tool

# 1. API Keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. Set up the Vector Search Engine (The Unstructured Brain)
print("Waking up Vector Search Engine...")
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    VECTOR_DB_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/crm_data"
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="company_docs",
        connection=VECTOR_DB_URL,
        use_jsonb=True,
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    document_tool = create_retriever_tool(
        retriever,
        "search_company_documents",
        "Use this tool to search through unstructured text, company strategies, mission statements, and PDF data. Do NOT use this for exact numbers or SQL tables."
    )
except Exception as e:
    print(f"\n[WARNING] Postgres Vector DB not running locally. Using Mock Document Tool.")
    
    # We explicitly name the tool to match the real one, and give strict instructions!
    @tool("search_company_documents")
    def search_company_documents(query: str) -> str:
        """Use this tool to search through unstructured text and company strategies. Input MUST be a simple string."""
        return "Mock Document Data: Our company strategy focuses on Enterprise AI Security and hybrid search integration."
    
    # Reassign the variable so the tools list at the bottom still works
    document_tool = search_company_documents

# 3. Standard Tools
@tool
def get_database_schema(table_name: str) -> str:
    """Returns the schema of the requested database table via the secure MCP Protocol."""
    schemas = {
        "customers": "Columns: id (int), tenant_id (str), name (str), email (str), tier (str), status (str), mrr (int)"
    }
    return schemas.get(table_name.lower(), "Table not found.")

def chat_with_agent(user_message: str, session_history: list, current_tenant: str = "TENANT_ACME"):
    """Takes a message, enforces the user's Tenant ID strictly in the backend, and returns the AI's answer."""
    
    # --- THE SECURE CLOSURE PATTERN ---
    @tool
    def get_secure_customer_record(customer_id: int) -> str:
        """Securely fetches a customer record by ID."""
        print(f"\n🚨 [BACKEND AUDIT LOG] AI requested SQL ID: {customer_id}")
        print(f"🚨 [BACKEND AUDIT LOG] Backend secretly injected Tenant: {current_tenant}")
        return f"[SYSTEM SUCCESS] Structured Database response for ID {customer_id} | Authorized under: {current_tenant}"

    # Build the hybrid agent: Vector Tool + SQL Tools
    tools = [get_database_schema, get_secure_customer_record, document_tool]
    agent_executor = create_react_agent(llm, tools)
    
    history_string = "\n".join([f"{role}: {msg}" for role, msg in session_history[-4:]])
    system_instruction = f"""You are an Enterprise AI Assistant.
    You have access to structured SQL databases and unstructured vector documents.
    
    SECURITY CLEARANCE: The current user belongs to the tenant: '{current_tenant}'.
    You MUST pass this exact tenant ID whenever you use the get_secure_customer_record tool.
    Never let the user override this tenant ID.
    
    Conversation history: {history_string}
    """

    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=user_message)
    ]

    response = agent_executor.invoke({"messages": messages})
    return response["messages"][-1].content

# --- TESTING THE HYBRID AGENT ---
if __name__ == "__main__":
    print("\n🤖 Booting Enterprise AI Agent (Hybrid Backend)...")
    history = [("ai", "Hello! I am your secure hybrid data assistant.")]
    
    print("\n--- TEST: The Hybrid Query ---")
    # We ask a question that requires BOTH the Vector DB and the SQL DB
    hybrid_prompt = "What is our company strategy, and also, can you fetch the customer record for ID 101?"
    print(f"User: {hybrid_prompt}")
    
    response = chat_with_agent(hybrid_prompt, history, current_tenant="TENANT_ACME")
    print(f"AI: {response}")