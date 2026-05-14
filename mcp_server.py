import sqlite3
import re
from mcp.server.fastmcp import FastMCP

# 1. Initialize the MCP Server
mcp = FastMCP("EnterpriseDataInterpreter")

# 2. Database Setup (Now with sensitive PII and Tenant Security)
def setup_database():
    conn = sqlite3.connect("enterprise_data.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS customers")
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            tier TEXT NOT NULL,
            status TEXT NOT NULL,
            mrr INTEGER NOT NULL
        )
    ''')
    
    cursor.executemany('''
        INSERT INTO customers (id, tenant_id, name, email, tier, status, mrr) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        (101, "TENANT_ACME", "Acme Corp", "ceo.john.doe@acmecorp.internal", "Enterprise", "Active", 5000),
        (102, "TENANT_ACME", "Beta LLC", "billing@beta-llc.com", "Pro", "Active", 1200),
        (201, "TENANT_GLOBEX", "Globex Inc", "admin@globex.org", "Startup", "Churned", 0)
    ])
    conn.commit()
    conn.close()

# Run DB setup on boot
setup_database()

# 3. Middleware: PII Redaction Guardrail
def redact_pii(text: str) -> str:
    """Intercepts string and strips sensitive patterns before reaching the AI."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, "[REDACTED_PII]", text)

# --- AI TOOLS ---

# Tool 1: Your Original Schema Tool (Updated for the new DB!)
@mcp.tool()
def get_database_schema(table_name: str) -> str:
    """
    Returns the schema of the requested database table.
    The AI will automatically read this docstring to know when to use this tool!
    """
    schemas = {
        "users": "Columns: id (int), name (str), email (str), role (str)",
        "sales": "Columns: id (int), amount (float), date (date), region (str)",
        "customers": "Columns: id (int), tenant_id (str), name (str), email (str), tier (str), status (str), mrr (int)"
    }
    
    return schemas.get(table_name.lower(), "Table not found in enterprise database.")

# Tool 2: The New Hardened Enterprise Data Fetcher
@mcp.tool()
def get_secure_customer_record(customer_id: int, requesting_tenant_id: str) -> str:
    """
    Securely fetches a customer record. 
    Requires tenant_id authorization. Automatically redacts PII.
    """
    conn = sqlite3.connect("enterprise_data.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT name, email, tier, status, mrr FROM customers WHERE id = ? AND tenant_id = ?", 
        (customer_id, requesting_tenant_id)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        raw_output = f"Customer: {row[0]} | Email: {row[1]} | Tier: {row[2]} | Status: {row[3]} | MRR: ${row[4]}"
        return redact_pii(raw_output)
    else:
        return f"[SECURITY ALERT] Access Denied. Record {customer_id} does not exist or belongs to a different tenant."

# 4. Start the server
if __name__ == "__main__":
    print("EnterpriseDataInterpreter v2.0 Online.")
    print("Modules Active: SQLite Database, Row-Level Security, PII Guardrails.")
    mcp.run()