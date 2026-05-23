from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn

# Import our AI brain and our Database vault
from app.core.agent import soc_copilot
from app.database import SessionLocal, SecurityLog

app = FastAPI(
    title="AI SOC Copilot API",
    description="Autonomous Agent for Security Log Triage",
    version="1.0.0"
)

# 1. Database Connection Manager (Opens and closes the vault safely)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. What an incoming log looks like
class LogInput(BaseModel):
    log_data: str

@app.get("/")
async def root_status():
    return {
        "status": "online",
        "message": "SOC Copilot Engine is running!",
        "agent_ready": True,
        "database_connected": True # Database is officially live!
    }

# 3. The Upgraded Intelligence Endpoint
@app.post("/analyze")
async def analyze_log_endpoint(request: LogInput, db: Session = Depends(get_db)):
    
    # A. Pass the raw log to LangGraph to think about
    initial_state = {"log_data": request.log_data, "analysis": "", "is_threat": False}
    result = soc_copilot.invoke(initial_state)
    
    # B. Write the AI's final decision permanently into our SQLite Database
    db_log = SecurityLog(
        raw_log=request.log_data,
        analysis=result["analysis"],
        is_threat=result["is_threat"]
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log) # Refreshes to grab the new automatic ID number
    
    # C. Send the final package back to the user
    final_action = result.get("action_taken", "✅ None Required - Routine Event")

    return {
        "incident_id": db_log.id, # We now have an official tracking number!
        "threat_detected": result["is_threat"],
        "ai_analysis": result["analysis"],
        "soar_action": final_action
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)