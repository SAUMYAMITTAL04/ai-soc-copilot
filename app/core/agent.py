import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from litellm import completion

# 1. Expand the State (Give the AI memory of its actions)
class AgentState(TypedDict):
    log_data: str
    analysis: str
    is_threat: bool
    action_taken: str  # NEW: Records what the AI did

# 2. Node 1: The Analyst (Your existing logic)
def analyze_node(state: AgentState):
    prompt = f"""
    Analyze this network log. Return ONLY valid JSON.
    Log: {state['log_data']}
    Format: {{"is_threat": true/false, "analysis": "brief reason"}}
    """
    response = completion(
        model="gemini/gemini-2.5-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    
    raw = response.choices[0].message.content.replace("```json", "").replace("```", "")
    data = json.loads(raw)
    
    return {"analysis": data["analysis"], "is_threat": data["is_threat"]}

# 3. NEW Node 2: The Tactical Responder (SOAR)
def remediation_node(state: AgentState):
    log = state['log_data']
    action = "Awaiting Action"
    
    # The AI reads the context and executes a simulated counter-measure
    if "SSHD" in log and "failed" in log:
        action = "🛡️ ACTION TAKEN: Automatically updated Firewall to DROP attacker IP."
    elif "FORCEPOINT_DLP" in log:
        action = "🔒 ACTION TAKEN: Suspended Active Directory account to stop exfiltration."
    else:
        action = "⚠️ ACTION TAKEN: Alert escalated to Tier-2 Human Analyst."
        
    return {"action_taken": action}

# 4. The Brain's Router: Conditional Logic
def route_threat(state: AgentState):
    if state["is_threat"] == True:
        return "remediate"  # Go to Node 2
    return "end"            # Skip Node 2 and finish

# 5. Build the New Graph
workflow = StateGraph(AgentState)

workflow.add_node("analyze", analyze_node)
workflow.add_node("remediate", remediation_node)

workflow.set_entry_point("analyze")

# The AI decides its own path based on the 'route_threat' function
workflow.add_conditional_edges(
    "analyze",
    route_threat,
    {
        "remediate": "remediate",
        "end": END
    }
)
workflow.add_edge("remediate", END)

soc_copilot = workflow.compile()