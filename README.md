# 🛡️ Enterprise AI SOC Command Center (Autonomous Tier-1 Copilot)

An autonomous, cloud-native SIEM/SOAR platform designed to eliminate alert fatigue and replace traditional, manual MSSP triage workflows. 

In a standard enterprise environment, security operations rely on disconnected tools (Forcepoint DLP, CrowdStrike EDR, Okta IAM) that generate thousands of daily alerts. This project introduces a **Tier-0 AI Copilot** that sits above the security stack. It ingests raw telemetry, utilizes an LLM to analyze context in real-time, filters out benign noise, and autonomously generates active SOAR countermeasures for verified threats.

## 🚀 Business Impact
* **Eliminates Tier-1 Bottlenecks:** Replaces expensive, manual alert triage with millisecond AI classification (True/False/Benign Positive).
* **Automates Active Defense:** Transitions security posture from passive monitoring to active SOAR (Security Orchestration, Automation, and Response).
* **Centralizes Intelligence:** Aggregates disconnected vendor logs into a single, highly visible command dashboard.

---

## 🏗️ System Architecture

1. **The Brain (FastAPI & LangGraph):** A decoupled microservice pipeline that receives incoming raw logs and utilizes Google Gemini to perform deep contextual analysis.
2. **The Vault (Neon PostgreSQL):** A serverless cloud database that persistently stores threat intelligence, keeping a permanent ledger of incident IDs, raw telemetry, AI analysis, and executed countermeasures.
3. **The Command Center (Streamlit):** A live, public-facing React-based dashboard featuring visual analytics, threat volume tracking, and real-time displays of active SOAR playbooks.
4. **The Adversary (Red Team Auto-Blaster):** A custom Python simulation script that continuously generates varied cyber-attacks (XSS, impossible travel, DLP exfiltration) to stress-test the API and populate the dashboard.

---

## 🛠️ Tech Stack

* **Backend Framework:** Python, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, Google Gemini API
* **Database:** Neon (Serverless PostgreSQL), SQLAlchemy, Pandas
* **Frontend/Visualization:** Streamlit
* **Deployment:** Render (API Host), Streamlit Community Cloud (Frontend)

---

## ⚙️ Core Features

* **Real-Time Telemetry Ingestion:** Processes high-volume log data via asynchronous API endpoints.
* **Autonomous Threat Triage:** Uses LLM reasoning to separate routine network traffic from critical security incidents.
* **SOAR Countermeasure Generation:** Automatically drafts remediation playbooks (e.g., "Suspended Active Directory account," "Quarantined Server IP") and logs them to the specific incident file.
* **Live Visual Analytics:** dynamic dashboarding that groups log classifications and active defense measures into instantly readable metrics.
* **Rate-Limit Resilience:** Includes custom error-handling and "sleep" states to gracefully manage upstream API quotas (429 Resource Exhausted handling).

---

## 🗄️ Database Schema (`threat_intel_logs`)

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Primary key, automated incident tracking number. |
| `raw_log` | String | The original telemetry from the security vendor. |
| `analysis` | String | The AI's contextual reasoning and payload breakdown. |
| `is_threat` | Boolean | True/False classification for dashboard routing. |
| `soar_action` | String | The automated countermeasure executed by the system. |

---

## 💻 Local Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/ai-soc-copilot.git](https://github.com/YOUR_GITHUB_USERNAME/ai-soc-copilot.git)
cd ai-soc-copilot
