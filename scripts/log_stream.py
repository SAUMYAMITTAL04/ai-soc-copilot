import time
import random
import datetime
import requests

def generate_log():
    timestamp = datetime.datetime.now().isoformat() + "Z"
    event_types = ["FAILED_LOGIN", "DLP_ALERT", "SYSTEM_HEALTH"]
    chosen_type = random.choices(event_types, weights=[0.3, 0.2, 0.5])[0]

    if chosen_type == "FAILED_LOGIN":
        users = ["admin", "hr_exec", "j_doe", "s_mittal"]
        return f"[{timestamp}] [SSHD] - Password authentication failed for user {random.choice(users)}"
    elif chosen_type == "DLP_ALERT":
        size = random.randint(5, 2000)
        return f"[{timestamp}] [FORCEPOINT_DLP] - User transferred {size}MB via cloud storage"
    else:
        return f"[{timestamp}] [KERNEL] - Cron job completed successfully"

def main():
    print("🚀 Starting Live Enterprise Log Stream Simulator...")
    print("📡 Connecting directly to AI SOC Copilot...")
    print("Press Ctrl+C to stop.\n")

    # This is the exact door to your running AI brain!
    API_URL = "http://127.0.0.1:8080/analyze"

    try:
        while True:
            # 1. Generate the fake raw log
            raw_log = generate_log()
            print(f"💻 NETWORK EVENT: {raw_log}")

            # 2. Package it exactly how your FastAPI server expects it
            payload = {"log_data": raw_log}
            
            # 3. Send it over the network to the AI
            try:
                response = requests.post(API_URL, json=payload)
                
                # 4. Read the AI's mind and print the result
                if response.status_code == 200:
                    ai_result = response.json()
                    
                    if ai_result["threat_detected"]:
                        print(f"🚨 AI COPILOT ALERT: {ai_result['ai_analysis']}\n")
                    else:
                        print(f"✅ AI COPILOT: {ai_result['ai_analysis']}\n")
                else:
                    print(f"⚠️ Server Error: {response.status_code}\n")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Error: Could not connect to the AI. Is your Uvicorn server running in the other terminal?")

            # Wait 5 to 8 seconds before sending the next log so we don't hit Google's free-tier speed limits!
            time.sleep(15)

    except KeyboardInterrupt:
        print("\nStopping log stream.")

if __name__ == "__main__":
    main()