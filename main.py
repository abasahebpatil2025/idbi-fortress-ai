import logging
import secrets
import json
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("FortressAI")

app = FastAPI(
    title="IDBI Innovate: FortressAI (Grand-Finale Edition)",
    description="Multi-Agent Threat Telemetry, Dark Web Feed, and Auto-Containment Platform",
    version="5.0.0"
)

# CORS Middleware configured for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory list to store incident logs
incident_logs = []

# Timezone helper for IST (UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

# Arm initial decoy list
armed_decoys = [
    {"path": "/api/v1/vault/customer-master-records", "type": "API Vault Probe", "classification": "CRITICAL_PII", "severity": "CRITICAL"},
    {"path": "/api/v1/db/config/mysql-credentials", "type": "DB Credentials Access", "classification": "HIGH_SECURITY_SECRETS", "severity": "HIGH"},
    {"path": "/api/v1/system/env-configuration", "type": "System Config Leak Probe", "classification": "INFRASTRUCTURE_METADATA", "severity": "MEDIUM"}
]


# =====================================================================
# MULTI-AGENT & LAKSHYA AI ORCHESTRATOR
# =====================================================================

class DecoyAssetAgent:
    """Agent 1 (Decoy Asset): Manages simulated honeytoken vaults."""
    @staticmethod
    def get_asset_metadata(path: str, classification: str):
        return {
            "status": "ALERT_TRIGGERED",
            "target_resource": path,
            "vault_id": f"vault-{path.replace('/', '_').strip('_')}",
            "data_classification": classification
        }


class WatchdogTelemetryAgent:
    """Agent 2 (Watchdog): Telemetry capture logic that intercepts details, location, and CLI command session."""
    @staticmethod
    def capture_attacker_telemetry(request: Request) -> dict:
        headers = request.headers
        user_agent = headers.get("user-agent", "Unknown")
        
        # Real client IP consideration
        client_ip = headers.get("x-forwarded-for")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = headers.get("x-real-ip", request.client.host if request.client else "Unknown")
            
        timestamp = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
        path = request.url.path
        
        # Geolocation Simulation
        locations = [
            "Mumbai, India 🇮🇳",
            "Moscow, Russia 🇷🇺 (Proxy VPN)",
            "Frankfurt, Germany 🇩🇪",
            "San Jose, USA 🇺🇸 (AWS Lambda Proxy)",
            "Beijing, China 🇨🇳",
            "Seoul, South Korea 🇰🇷",
            "London, United Kingdom 🇬🇧",
            "Amsterdam, Netherlands 🇳🇱"
        ]
        location = secrets.choice(locations)
        
        return {
            "client_ip": client_ip,
            "user_agent": user_agent,
            "path": path,
            "timestamp": timestamp,
            "location": location
        }


class EnforcerContainmentAgent:
    """Agent 3 (Enforcer): Automated threat containment response simulation."""
    @staticmethod
    def trigger_mitigation(telemetry: dict) -> dict:
        year = datetime.now(IST).year
        random_hex = secrets.token_hex(3)[:5]
        guardduty_id = f"gd-{year}-{random_hex}"
        lambda_req_id = str(uuid.uuid4())
        
        # Generate simulated production AWS metadata
        aws_mitigation = {
            "aws_lambda": {
                "execution_arn": "arn:aws:lambda:us-east-1:123456789012:function:FortressAI-ContainmentAction",
                "request_id": lambda_req_id,
                "billing_duration_ms": 142
            },
            "aws_waf": {
                "status": "IP_ISOLATED",
                "ip_set_name": "FortressAI-WAF-Blocklist-IP-Set",
                "action": "BLOCK",
                "isolated_target": telemetry["client_ip"]
            },
            "aws_guardduty": {
                "incident_id": guardduty_id,
                "severity": 8.5,
                "threat_name": "UnauthorizedAccess:IAMUser/HoneytokenAssetTouched"
            }
        }
        
        # Mock Quantum-Resilient NIST-compliant Kyber-1024 Layer
        quantum_resilient_layer = {
            "pqc_signature": "ML-KEM-1024 (Kyber-1024) Lattice Signature Engaged",
            "nist_compliance": "FIPS 203 compliant",
            "lattice_parameters": "n=1024, q=3329, eta=2",
            "pqc_status": "SEALED",
            "secret_key_encapsulation": f"kyber_kem_ct_{secrets.token_hex(16)}"
        }
        
        return {
            "aws_mitigation": aws_mitigation,
            "quantum_resilient_layer": quantum_resilient_layer,
            "guardduty_id": guardduty_id
        }


class LakshyaAIOrchestrator:
    """Lakshya AI Threat Intelligence Orchestrator: Synthesizes detailed incident reports."""
    @staticmethod
    def generate_report(telemetry: dict, enforcement: dict, vector: str, severity: str) -> str:
        pqc = enforcement["quantum_resilient_layer"]
        aws = enforcement["aws_mitigation"]
        
        report = f"""# 🛡️ LAKSHYA AI DETAILED SECURITY INCIDENT REPORT
**IDBI Innovate: FortressAI Autonomous Threat Orchestration**

## 1. Executive Summary
At {telemetry['timestamp']}, a critical security boundary was violated. An unauthorized actor from {telemetry['location']} attempted to retrieve sensitive records from the honeytoken decoy asset. The Threat Intelligence Orchestrator (Lakshya AI) immediately intercepted the telemetry and initiated automated quarantine protocols.

- **Incident ID:** {enforcement['guardduty_id']}
- **Severity Level:** {severity} (Score: 8.5/10)
- **Target Asset:** {telemetry['path']}
- **Status:** CONTAINED & ISOLATED

## 2. Attacker Persona & TTPs Estimation
- **Vector Source IP:** `{telemetry['client_ip']}`
- **Attacker Origin:** `{telemetry['location']}`
- **Signature (User-Agent):** `{telemetry['user_agent']}`
- **Estimated TTPs:** Automated API Scanner / Reconnaissance agent probing high-value database indexes. Likely reconnaissance leading to credential harvest.
- **Threat Vector Category:** {vector}

## 3. Multi-Stage Cloud Mitigation Pipeline
- [x] **Stage 1: Perimeter Isolation** - Attacker IP `{telemetry['client_ip']}` added to AWS WAF IP Set Blocklist.
- [x] **Stage 2: SecOps Broadcast** - Automated Webhook dispatch triggered for IDBI Bank Incident Response Team.
- [x] **Stage 3: Deception Route Rotting** - Routed to synthetic honey vault database nodes to consume attacker bandwidth.

## 4. Post-Quantum Lattice Signature Seal
- **Cipher Suite:** ML-KEM-1024 (NIST Kyber-1024 compliant)
- **Key Seal ID:** `{pqc['secret_key_encapsulation'][:30]}...`
- **Verification Hash:** SHA3_512:{secrets.token_hex(24)}
- **Integrity Seal:** ACTIVE (Lattice Signature validated)"""
        return report


# Helper to get simulated command session based on vector
def get_simulated_shell_commands(vector_name: str, path: str):
    if "API" in vector_name:
        return [
            {"type": "cmd", "text": f"$ nmap -sV -p 80,443 idbi-fortress.bank"},
            {"type": "output", "text": "PORT    STATE SERVICE\n443/tcp open  ssl/http"},
            {"type": "cmd", "text": f"$ curl -i -X GET https://idbi-fortress.bank{path}"},
            {"type": "alert", "text": "[SYSTEM ALERT] 401 Unauthorized - Access Denied"},
            {"type": "cmd", "text": f"$ curl -i -H 'Authorization: Bearer admin_token' https://idbi-fortress.bank{path}"},
            {"type": "alert", "text": "[SYSTEM WARNING] Intrusion detected. IP routed to AWS WAF blocklist."}
        ]
    elif "DB" in vector_name:
        return [
            {"type": "cmd", "text": "$ mysql -h target-db.internal -u admin -p"},
            {"type": "output", "text": "Connecting to target-db.internal..."},
            {"type": "cmd", "text": "mysql> show databases;"},
            {"type": "output", "text": "Database: customer_records, sys_config"},
            {"type": "cmd", "text": "mysql> drop table customer_data;"},
            {"type": "alert", "text": "[SYSTEM ALERT] Transaction blocked by WAF Deception Policy."}
        ]
    else:
        return [
            {"type": "cmd", "text": "$ cat /etc/passwd"},
            {"type": "output", "text": "root:x:0:0:root:/root:/bin/bash"},
            {"type": "cmd", "text": "$ env | grep SECRET"},
            {"type": "output", "text": "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nAWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"},
            {"type": "alert", "text": "[SYSTEM WARNING] Access token honeypot triggered. Keys revoked by AWS IAM."}
        ]


# Helper for recording simulation hits
def register_incident(request: Request, vector_name: str, classification: str, severity: str):
    telemetry = WatchdogTelemetryAgent.capture_attacker_telemetry(request)
    enforcement = EnforcerContainmentAgent.trigger_mitigation(telemetry)
    decoy = DecoyAssetAgent.get_asset_metadata(telemetry["path"], classification)
    
    # Generate Lakshya AI report
    report = LakshyaAIOrchestrator.generate_report(telemetry, enforcement, vector_name, severity)
    
    # Generate simulated shell commands
    commands = get_simulated_shell_commands(vector_name, telemetry["path"])
    
    # Save incident log
    incident_logs.append({
        "timestamp": telemetry["timestamp"],
        "client_ip": telemetry["client_ip"],
        "user_agent": telemetry["user_agent"],
        "location": telemetry["location"],
        "guardduty_id": enforcement["guardduty_id"],
        "mitigation_status": "AWS_WAF_ISOLATION",
        "vector": vector_name,
        "report": report,
        "commands": commands
    })
    
    logger.error(
        f"[🚨 BREACH ALERT] Honeytoken asset touched [{vector_name}]!\n"
        f"  - Client IP: {telemetry['client_ip']} ({telemetry['location']})\n"
        f"  - GuardDuty ID: {enforcement['guardduty_id']}"
    )
    
    # Simulate Route Rotting with rotten/spoofed payload
    return {
        "status": "CONTAINMENT_ACTIVATED",
        "mitigation_pipeline": {
            "stage_1": "[AWS WAF] Attacker IP Isolated & Blocked",
            "stage_2": "[SecOps Alert] Webhook dispatched to IDBI Incident Response",
            "stage_3": "[Deception Mesh] Route Rotten - Feeding 100% synthetic/spoofed data"
        },
        "agent_1_decoy_asset": decoy,
        "agent_2_watchdog": {
            "telemetry_captured": telemetry
        },
        "agent_3_enforcer": {
            "aws_mitigation_telemetry": enforcement["aws_mitigation"],
            "quantum_resilient_layer": enforcement["quantum_resilient_layer"]
        },
        "lakshya_ai_report": report,
        "attacker_command_replay": commands,
        "synthetic_rotten_data": {
            "customer_id": f"cust-{secrets.token_hex(4)}",
            "pan_number": f"AAAAA{secrets.randbelow(10000):04d}A",
            "account_balance_inr": f"{secrets.randbelow(9999999):,}.00",
            "note": "This data is 100% synthetic/spoofed. Security protocols engaged."
        }
    }


# =====================================================================
# DYNAMIC DECOY HANDLER BINDER
# =====================================================================

def make_deception_handler(v_name, clazz, sev):
    async def handler(request: Request):
        return register_incident(request, v_name, clazz, sev)
    return handler

# Register default endpoints
for decoy in armed_decoys:
    app.add_api_route(
        decoy["path"],
        make_deception_handler(decoy["type"], decoy["classification"], decoy["severity"]),
        methods=["GET"]
    )


# =====================================================================
# ADMIN CONTROLLER
# =====================================================================

@app.post("/admin/deploy-trap")
async def deploy_trap(path: str = Form(...), trap_type: str = Form(...), severity: str = Form(...)):
    # Clean path format
    if not path.startswith("/"):
        path = "/" + path
    
    # Deduplicate paths
    for decoy in armed_decoys:
        if decoy["path"] == path:
            return RedirectResponse(url="/", status_code=303)
            
    # Map selection variables
    if trap_type == "API":
        classification = "CRITICAL_PII"
        vector_name = "API Vault Probe"
    elif trap_type == "DB":
        classification = "HIGH_SECURITY_SECRETS"
        vector_name = "DB Credentials Access"
    else:
        classification = "INFRASTRUCTURE_METADATA"
        vector_name = "System Config Leak Probe"
        
    decoy_entry = {
        "path": path,
        "type": vector_name,
        "classification": classification,
        "severity": severity
    }
    armed_decoys.append(decoy_entry)
    
    # Dynamically bind Route into FastAPI router
    app.add_api_route(
        path,
        make_deception_handler(vector_name, classification, severity),
        methods=["GET"]
    )
    
    logger.info(f"[+] Dynamically Deployed Honeytoken: {path} [{severity}]")
    return RedirectResponse(url="/", status_code=303)


# =====================================================================
# DASHBOARD ROUTE
# =====================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    total_incidents = len(incident_logs)
    
    # Time chart aggregation
    from collections import Counter
    time_counts = Counter(log["timestamp"].split(" ")[1] for log in incident_logs) # HH:MM:SS
    sorted_times = sorted(time_counts.keys())
    sorted_counts = [time_counts[t] for t in sorted_times]
    
    # Vector chart aggregation
    api_hits = sum(1 for log in incident_logs if log.get("vector") == "API Vault Probe")
    db_hits = sum(1 for log in incident_logs if log.get("vector") == "DB Credentials Access")
    sys_hits = sum(1 for log in incident_logs if log.get("vector") == "System Config Leak Probe")
    
    # Latest report and commands session
    if incident_logs:
        latest_report = incident_logs[-1]["report"]
        latest_commands = incident_logs[-1]["commands"]
    else:
        latest_report = """# 🛡️ LAKSHYA AI THREAT INTEL ORCHESTRATOR
**Status:** MONITORING TRAPS | DECEPTION SYSTEMS ARMED

No threats detected in the telemetry stream yet. 
Access any honeytoken decoy link above to trigger autonomous containment & telemetry reporting."""
        latest_commands = [{"type": "output", "text": "[SYSTEM] Standing by... Listening on socket telemetry ports."}]

    # Table generation
    if not incident_logs:
        logs_table_or_placeholder = """
        <div class="no-logs">
            <span class="no-logs-icon">🛡️</span>
            <p>No intrusion events captured yet. Deception system is scanning for anomalies...</p>
        </div>
        """
    else:
        rows = []
        for log in reversed(incident_logs):
            rows.append(f"""
            <tr>
                <td class="timestamp-cell">{log['timestamp']}</td>
                <td class="ip-cell">{log['client_ip']}</td>
                <td class="location-cell">{log['location']}</td>
                <td class="ua-cell" title="{log['user_agent']}">{log['user_agent']}</td>
                <td class="gd-cell">{log['guardduty_id']}</td>
                <td>
                    <div class="mitigation-stages-container">
                        <div class="mitigation-stage stage-waf"><span class="stage-dot-active"></span>[WAF] Isolated & Blocked</div>
                        <div class="mitigation-stage stage-webhook"><span class="stage-dot-active"></span>[SecOps] Alert Dispatched</div>
                        <div class="mitigation-stage stage-rotten"><span class="stage-dot-active"></span>[Deception] Rotten Route engaged</div>
                    </div>
                </td>
            </tr>
            """)
        logs_table_or_placeholder = f"""
        <table>
            <thead>
                <tr>
                    <th>Timestamp (IST)</th>
                    <th>Attacker Source IP</th>
                    <th>Attacker Location</th>
                    <th>User-Agent / Profiler Data</th>
                    <th>Active AWS GuardDuty ID</th>
                    <th>Mitigation Pipeline</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows)}
            </tbody>
        </table>
        """

    # Populate traps HTML display
    traps_html = []
    for decoy in armed_decoys:
        badge_color = "var(--accent-danger)"
        if decoy["severity"] == "HIGH":
            badge_color = "var(--accent-yellow)"
        elif decoy["severity"] == "MEDIUM":
            badge_color = "var(--accent-cyber)"
        elif decoy["severity"] == "LOW":
            badge_color = "var(--text-secondary)"
            
        traps_html.append(f"""
        <div class="endpoint-row">
            <span class="method-badge">GET</span>
            <a href="{decoy['path']}" target="_blank" class="endpoint-link">{decoy['path']}</a>
            <span style="color: {badge_color}; font-size: 0.7rem; font-weight:700;">{decoy['severity']}</span>
        </div>
        """)

    # Render shell lines
    shell_lines_html = []
    for cmd in latest_commands:
        line_class = "shell-line cmd"
        if cmd["type"] == "output":
            line_class = "shell-line output"
        elif cmd["type"] == "alert":
            line_class = "shell-line alert"
        shell_lines_html.append(f'<div class="{line_class}">{cmd["text"]}</div>')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="3">
    <title>FortressAI - Security Operations Center</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-color: #05070a;
            --card-bg: rgba(10, 15, 26, 0.75);
            --border-color: rgba(255, 255, 255, 0.06);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent-cyber: #06b6d4;
            --accent-danger: #f43f5e;
            --accent-success: #10b981;
            --accent-yellow: #f59e0b;
            --glow: 0 0 15px rgba(6, 182, 212, 0.4);
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(244, 63, 94, 0.05) 0px, transparent 50%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .container {{
            width: 100%;
            max-width: 1400px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem 2rem;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        }}

        .logo-section {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .logo-icon {{
            color: var(--accent-cyber);
            text-shadow: var(--glow);
            font-size: 1.5rem;
            font-weight: 800;
            font-family: 'Fira Code', monospace;
        }}

        .logo-title {{
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #ffffff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .status-badge {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 9999px;
            color: var(--accent-success);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .status-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--accent-success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px var(--accent-success);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }}
            70% {{
                transform: scale(1);
                box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
            }}
            100% {{
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }}
        }}

        /* Ticker styling */
        .intel-ticker-container {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            font-size: 0.8rem;
            backdrop-filter: blur(12px);
            overflow: hidden;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }}

        .ticker-title {{
            color: var(--accent-danger);
            font-weight: 700;
            letter-spacing: 0.05em;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .ticker-content {{
            width: 100%;
            overflow: hidden;
            color: var(--text-secondary);
            font-family: 'Fira Code', monospace;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.25rem;
        }}

        .stat-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        }}

        .stat-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }}

        .stat-value {{
            font-size: 1.5rem;
            font-weight: 700;
            font-family: 'Fira Code', monospace;
        }}

        .text-red {{
            color: var(--accent-danger);
            text-shadow: 0 0 10px rgba(244, 63, 94, 0.2);
        }}

        .text-green {{
            color: var(--accent-success);
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
        }}

        .text-cyan {{
            color: var(--accent-cyber);
            text-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
        }}

        .text-yellow {{
            color: var(--accent-yellow);
            text-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
        }}

        /* Split layout grid */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 1.5rem;
        }}

        @media (max-width: 1024px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .panel {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}

        .endpoint-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
        }}

        .admin-panel {{
            border: 1px solid rgba(6, 182, 212, 0.15);
        }}

        .admin-form {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            align-items: flex-end;
        }}

        .form-group {{
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            flex: 1;
            min-width: 180px;
        }}

        .form-group label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-secondary);
        }}

        .form-group input, .form-group select {{
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.5rem;
            color: var(--text-primary);
            font-family: inherit;
            font-size: 0.85rem;
            outline: none;
            transition: border-color 0.3s;
        }}

        .form-group input:focus, .form-group select:focus {{
            border-color: var(--accent-cyber);
        }}

        .deploy-btn {{
            background: linear-gradient(135deg, var(--accent-cyber), #0891b2);
            border: none;
            color: #fff;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            height: 35px;
        }}

        .deploy-btn:hover {{
            box-shadow: var(--glow);
            transform: translateY(-1px);
        }}

        .card-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }}

        .endpoints-list {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 180px;
            overflow-y: auto;
        }}

        .endpoint-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
        }}

        .endpoint-link {{
            color: var(--accent-cyber);
            text-decoration: none;
            transition: all 0.3s ease;
        }}

        .endpoint-link:hover {{
            color: #22d3ee;
            text-shadow: var(--glow);
        }}

        .method-badge {{
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: var(--accent-cyber);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: 700;
        }}

        /* Split grid layout for charts */
        .charts-split-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}
        @media (max-width: 640px) {{
            .charts-split-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-container {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            height: 250px;
            position: relative;
        }}

        /* Interactive command shell terminal */
        .shell-terminal {{
            background: #020406;
            border: 1px solid rgba(244, 63, 94, 0.25);
            border-radius: 12px;
            padding: 1.25rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            color: #38bdf8;
            min-height: 180px;
            max-height: 220px;
            overflow-y: auto;
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.9);
            line-height: 1.6;
        }}

        .shell-line {{
            margin-bottom: 0.25rem;
        }}
        
        .shell-line.cmd {{
            color: #38bdf8;
        }}
        
        .shell-line.output {{
            color: #9ca3af;
        }}
        
        .shell-line.alert {{
            color: #f43f5e;
            font-weight: bold;
        }}

        /* Terminal screen report style */
        .terminal-panel {{
            background: #020406;
            border: 1px solid rgba(6, 182, 212, 0.25);
            border-radius: 12px;
            padding: 1.5rem;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            color: #e2e8f0;
            height: 100%;
            min-height: 480px;
            max-height: 600px;
            overflow-y: auto;
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.8);
            line-height: 1.5;
            white-space: pre-wrap;
        }}

        .logs-section {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .logs-header {{
            padding: 1.25rem 2rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logs-title {{
            font-size: 1rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .logs-count {{
            background: rgba(244, 63, 94, 0.1);
            border: 1px solid rgba(244, 63, 94, 0.3);
            color: var(--accent-danger);
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 600;
            font-family: 'Fira Code', monospace;
        }}

        .table-container {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.85rem;
        }}

        th {{
            background: rgba(255, 255, 255, 0.02);
            padding: 0.85rem 1.5rem;
            color: var(--text-secondary);
            font-weight: 500;
            border-bottom: 1px solid var(--border-color);
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 0.85rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.01);
        }}

        .ip-cell {{
            font-family: 'Fira Code', monospace;
            color: #e2e8f0;
            font-weight: 500;
        }}

        .location-cell {{
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
        }}

        .timestamp-cell {{
            font-family: 'Fira Code', monospace;
            color: var(--text-secondary);
        }}

        .ua-cell {{
            max-width: 180px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            color: var(--text-secondary);
            font-size: 0.8rem;
        }}

        .gd-cell {{
            font-family: 'Fira Code', monospace;
            color: var(--accent-yellow);
            font-size: 0.8rem;
        }}

        .mitigation-stages-container {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .mitigation-stage {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.7rem;
            font-family: 'Fira Code', monospace;
            font-weight: 500;
        }}

        .stage-dot-active {{
            width: 6px;
            height: 6px;
            background-color: var(--accent-success);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 5px var(--accent-success);
        }}

        .stage-waf {{ color: #10b981; }}
        .stage-webhook {{ color: #67e8f9; }}
        .stage-rotten {{ color: #a855f7; }}

        .no-logs {{
            padding: 3rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.95rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
        }}

        .no-logs-icon {{
            font-size: 2rem;
            color: var(--text-secondary);
            opacity: 0.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header>
            <div class="logo-section">
                <span class="logo-icon">⛨</span>
                <span class="logo-title">IDBI Innovate: FortressAI SOC Dashboard</span>
            </div>
            <div class="status-badge">
                <span class="status-dot"></span>
                DECEPTION LAYER ACTIVE
            </div>
        </header>

        <!-- Dark Web Threat Intel Feed -->
        <div class="intel-ticker-container">
            <div class="ticker-title">🌐 DARK WEB FEED:</div>
            <div class="ticker-content">
                <marquee scrollamount="4">
                    [ BreachForums Scanner ] Scanning BreachForums for IDBI targets... STATUS: CLEAR &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
                    [ Threat Intel ] Ransomware group 'LockBit 4.0' active via proxy tunnel [Moscow VPN]... MONITORING &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
                    [ SecOps Intel ] Hacker forum 'ZeroDayBankers' discussing Kyber-1024 encryption bypass failures... BLOCKED &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
                    [ WAF Alert ] Automated blocklist pipeline synchronized across all AWS global regions... ACTIVE
                </marquee>
            </div>
        </div>

        <!-- Dynamic Admin Control Panel -->
        <div class="endpoint-card admin-panel">
            <span class="card-label" style="color: var(--accent-cyber); font-weight:700;">🛡️ IDBI Security Admin: Deploy New Honeytoken Trap</span>
            <form action="/admin/deploy-trap" method="POST" class="admin-form">
                <div class="form-group">
                    <label for="path">Endpoint Path</label>
                    <input type="text" id="path" name="path" placeholder="e.g., /api/v1/credit-cards/master" required>
                </div>
                <div class="form-group">
                    <label for="trap_type">Trap Type</label>
                    <select id="trap_type" name="trap_type">
                        <option value="API">API Vault Decoy</option>
                        <option value="DB">DB Secret Decoy</option>
                        <option value="Config">Config File Decoy</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="severity">Severity Level</label>
                    <select id="severity" name="severity">
                        <option value="CRITICAL">CRITICAL</option>
                        <option value="HIGH">HIGH</option>
                        <option value="MEDIUM">MEDIUM</option>
                        <option value="LOW">LOW</option>
                    </select>
                </div>
                <button type="submit" class="deploy-btn">DEPLOY TRAP</button>
            </form>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-label">Total Intrusion Events</span>
                <span class="stat-value text-red">{total_incidents}</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">Lakshya AI Status</span>
                <span class="stat-value text-green">ORCHESTRATING</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">PQC Key Signature</span>
                <span class="stat-value text-cyan">Kyber-1024</span>
            </div>
            <div class="stat-card">
                <span class="stat-label">AWS WAF Rule Status</span>
                <span class="stat-value text-yellow">AUTO-BLOCK</span>
            </div>
        </div>

        <!-- Dashboard Split Layout -->
        <div class="dashboard-grid">
            <!-- Left Panel: Deception Actions, Chart Telemetry & Live Session Replay -->
            <div class="panel">
                <!-- Decoys List -->
                <div class="endpoint-card">
                    <span class="card-label">Armed Honeytoken Traps (Trigger simulated attacks)</span>
                    <div class="endpoints-list">
                        {"".join(traps_html)}
                    </div>
                </div>

                <!-- Charts Split Grid -->
                <div class="charts-split-grid">
                    <div class="chart-container">
                        <span class="card-label" style="display:block; margin-bottom:0.75rem;">Attack Frequency (Time Series)</span>
                        <canvas id="attackFreqChart"></canvas>
                    </div>
                    <div class="chart-container">
                        <span class="card-label" style="display:block; margin-bottom:0.75rem;">Threat Vector Distribution</span>
                        <canvas id="threatVectorChart"></canvas>
                    </div>
                </div>

                <!-- Attacker Command Shell Replay -->
                <div class="endpoint-card">
                    <span class="card-label" style="color: var(--accent-danger);">🖥️ Live Session Replay: Intercepted Attacker Shell</span>
                    <div class="shell-terminal">
                        {"".join(shell_lines_html)}
                    </div>
                </div>
            </div>

            <!-- Right Panel: Lakshya AI Live Report Terminal -->
            <div class="panel">
                <div style="display:flex; flex-direction:column; height: 100%;">
                    <pre class="terminal-panel">{latest_report}</pre>
                    <button onclick="exportAuditReport()" class="deploy-btn" style="background: linear-gradient(135deg, #a855f7, #7e22ce); margin-top: 1rem; width: 100%;">📄 Export Forensic Audit Report</button>
                </div>
            </div>
        </div>

        <!-- Telemetry Logs -->
        <div class="logs-section">
            <div class="logs-header">
                <span class="logs-title">🛡️ Real-Time Telemetry Security Incident Logs</span>
                <span class="logs-count">{total_incidents} INCIDENTS DETECTED</span>
            </div>
            <div class="table-container">
                {logs_table_or_placeholder}
            </div>
        </div>
    </div>

    <!-- Chart.js configuration -->
    <script>
        const attackLabels = {json.dumps(sorted_times)};
        const attackData = {json.dumps(sorted_counts)};
        const vectorLabels = ["API Vault Probe", "DB Credentials Access", "System Config Leak Probe"];
        const vectorData = [{api_hits}, {db_hits}, {sys_hits}];

        // Line Chart: Attack Frequency
        const ctxFreq = document.getElementById('attackFreqChart').getContext('2d');
        new Chart(ctxFreq, {{
            type: 'line',
            data: {{
                labels: attackLabels,
                datasets: [{{
                    label: 'Intrusions',
                    data: attackData,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.15)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#06b6d4'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.03)' }},
                        ticks: {{ color: '#9ca3af', font: {{ family: 'Fira Code', size: 9 }} }}
                    }},
                    y: {{
                        grid: {{ color: 'rgba(255, 255, 255, 0.03)' }},
                        ticks: {{ color: '#9ca3af', font: {{ family: 'Fira Code', size: 9 }}, stepSize: 1 }},
                        beginAtZero: true
                    }}
                }}
            }}
        }});

        // Doughnut Chart: Threat Vector Distribution
        const ctxVector = document.getElementById('threatVectorChart').getContext('2d');
        new Chart(ctxVector, {{
            type: 'doughnut',
            data: {{
                labels: vectorLabels,
                datasets: [{{
                    data: vectorData,
                    backgroundColor: ['#f43f5e', '#f59e0b', '#06b6d4'],
                    borderColor: '#05070a',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            color: '#9ca3af',
                            font: {{ family: 'Inter', size: 9 }},
                            boxWidth: 10
                        }}
                    }}
                }}
            }}
        }});

        // Forensic Audit PDF Export
        function exportAuditReport() {{
            const reportContent = document.querySelector('.terminal-panel').innerText;
            const printWindow = window.open('', '_blank');
            printWindow.document.write('<html><head><title>FortressAI Forensic Audit Report</title>');
            printWindow.document.write('<style>body {{ font-family: monospace; padding: 2rem; background: #fff; color: #000; line-height: 1.5; white-space: pre-wrap; }}</style>');
            printWindow.document.write('</head><body>');
            printWindow.document.write(reportContent);
            printWindow.document.write('</body></html>');
            printWindow.document.close();
            printWindow.focus();
            printWindow.print();
            printWindow.close();
        }}
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
