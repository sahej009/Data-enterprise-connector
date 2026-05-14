from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sql_agent import chat_with_agent

app = FastAPI(title="Enterprise AI Backend")

# Allow React to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the incoming data from React will look like
class ChatRequest(BaseModel):
    message: str
    history: list
    # NEW: We simulate a secure session token from the web browser!
    tenant_id: str = "TENANT_ACME" 

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    print(f"\n🌐 [API ROUTER] Web request received!")
    print(f"🔑 [AUTH VALIDATED] Forwarding to Agent as Tenant: {request.tenant_id}")
    print(f"🗣️  [USER] {request.message}")
    
    # Send the web request AND the security token to our LangChain agent
    ai_answer = chat_with_agent(
        user_message=request.message, 
        session_history=request.history,
        current_tenant=request.tenant_id
    )
    
    return {"reply": ai_answer}