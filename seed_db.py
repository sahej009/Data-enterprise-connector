import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. The Connection String (Your VIP Pass)
DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/crm_data"

# 2. Connect to the Docker Engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# 3. Define our Enterprise Tables (The Folders)
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    department = Column(String)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    industry = Column(String)
    status = Column(String) # e.g., 'Active', 'Churned'

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    amount = Column(Float)
    date = Column(Date)

# 4. Build the empty tables in Postgres
print("Building tables...")
Base.metadata.create_all(engine)

# 5. Seed with Realistic Data (The Documents)
Session = sessionmaker(bind=engine)
session = Session()

# Check if we already have data to prevent duplicates if you run this twice
if session.query(Employee).count() == 0:
    print("Inserting dummy enterprise data...")
    
    # Add Employees
    e1 = Employee(name="Sarah Jenkins", role="Account Executive", department="Sales")
    e2 = Employee(name="Marcus Chen", role="Data Engineer", department="IT")
    session.add_all([e1, e2])

    # Add Clients
    c1 = Client(company_name="Acme Corp", industry="Manufacturing", status="Active")
    c2 = Client(company_name="Globex", industry="Logistics", status="Churned")
    c3 = Client(company_name="Initech", industry="Software", status="Active")
    session.add_all([c1, c2, c3])
    
    session.commit() # Save the clients to generate their IDs for the sales records

    # Add Sales
    s1 = Sale(client_id=c1.id, amount=15000.00, date=datetime.date(2025, 10, 15))
    s2 = Sale(client_id=c2.id, amount=8500.50, date=datetime.date(2025, 8, 22))
    s3 = Sale(client_id=c3.id, amount=42000.00, date=datetime.date(2026, 1, 10))
    session.add_all([s1, s2, s3])
    
    session.commit()
    print("Database successfully seeded! 🚀")
else:
    print("Data already exists. Ready to query! 🚀")
    
session.close()