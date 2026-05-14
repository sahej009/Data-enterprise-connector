from sqlalchemy import create_engine, text

# 1. Connect as the Admin one last time
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/crm_data"
engine = create_engine(DATABASE_URL)

# 2. Execute the security commands
with engine.connect() as conn:
    # We need autocommit to create users in PostgreSQL
    conn.execution_options(isolation_level="AUTOCOMMIT")
    
    # Create the restricted user
    conn.execute(text("CREATE USER ai_reader WITH PASSWORD 'readonlypassword';"))
    
    # Grant them permission to ONLY read data
    conn.execute(text("GRANT SELECT ON ALL TABLES IN SCHEMA public TO ai_reader;"))
    
    print("Security update complete: Read-only user 'ai_reader' created! 🛡️")