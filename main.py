# main.py
# Command Line Interface for Composio 100-App Research & Verification Pipeline

import argparse
import json
import sys
import os
import http.server
import socketserver
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent.research_agent import ComposioAppResearcher
from agent.verification_engine import VerificationEngine

DATA_PATH = Path(__file__).resolve().parent / "data" / "apps_100.json"
AUDIT_PATH = Path(__file__).resolve().parent / "data" / "verification_audit.json"

def show_status():
    if not DATA_PATH.exists():
        print(f"Error: Dataset not found at {DATA_PATH}")
        return
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        apps = json.load(f)
    print("=" * 60)
    print(" COMPOSIO 100-APP RESEARCH PIPELINE STATUS")
    print("=" * 60)
    print(f" Total Applications Tracked: {len(apps)}")
    categories = set(a["category"] for a in apps)
    print(f" Target Categories: {len(categories)}")
    self_serve = sum(1 for a in apps if a["is_self_serve"])
    print(f" Self-Serve Feasibility: {self_serve}% ({self_serve}/{len(apps)})")
    ready = sum(1 for a in apps if "Ready" in a["buildability"]["verdict"])
    print(f" Ready for Agent Toolkits: {ready}% ({ready}/{len(apps)})")
    official_mcp = sum(1 for a in apps if "Official" in a["api_surface"]["mcp_status"])
    print(f" Official MCP Servers Found: {official_mcp}% ({official_mcp}/{len(apps)})")
    print("=" * 60)

def run_pipeline():
    print("Starting automated research pipeline...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        apps = json.load(f)
    agent = ComposioAppResearcher()
    results = agent.run_pass_1(apps)
    print(f"Pass 1 extraction complete across {len(results)} apps.")

def run_verify():
    print("Executing 5-loop verification engine across all 100 apps...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        apps = json.load(f)
    engine = VerificationEngine()
    
    verified_count = 0
    escalated_count = 0
    for app in apps:
        res = engine.verify_app(app)
        if res["verified"]:
            verified_count += 1
        if res["needs_human_escalation"]:
            escalated_count += 1
            
    print("-" * 60)
    print(f"Automated Verification Completed:")
    print(f"  Successfully Passed All 4 Automated Loops: {verified_count}/100")
    print(f"  Flagged for Human-in-the-Loop Escalation:  {escalated_count}/100")
    print("-" * 60)

def show_audit():
    if not AUDIT_PATH.exists():
        print(f"Audit log not found at {AUDIT_PATH}")
        return
    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        audit = json.load(f)
    metrics = audit["metrics"]
    print("=" * 65)
    print(" COMPOSIO RESEARCH ACCURACY VERIFICATION AUDIT")
    print("=" * 65)
    print(" OVERALL 100-APP ACCURACY TRAJECTORY:")
    pipe = metrics["overall_100_apps_pipeline"]
    print(f"   Pass 1 (Raw Scraper/Agent):     {pipe['pass1_raw_agent_accuracy']}")
    print(f"   Pass 2 (Verification Loops):    {pipe['pass2_verification_loop_accuracy']}  ({pipe['accuracy_lift_automated']} automated lift)")
    print(f"   Final (Human Escalation):       {pipe['final_verified_accuracy']}")
    print("\n STRESS-TEST CHALLENGE SAMPLE (25 High-Ambiguity Apps):")
    sample = metrics["stress_test_sample_25"]
    print(f"   Sample Pass 1 Accuracy:         {sample['pass1_accuracy']}")
    print(f"   Sample Pass 2 Accuracy:         {sample['pass2_accuracy']}")
    print(f"   Sample Final Accuracy:          {sample['final_human_accuracy']}")
    print("\n ERROR TAXONOMY RESOLVED BY LOOPS:")
    for err, desc in sample["error_taxonomy"].items():
        print(f"   - {err}: {desc}")
    print("=" * 65)

def serve_dashboard(port=8000):
    web_dir = Path(__file__).resolve().parent
    os.chdir(web_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving Composio Case Study & Dashboard at http://localhost:{port}/index.html")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def main():
    parser = argparse.ArgumentParser(description="Composio AI Product Ops 100-App Research Agent CLI")
    parser.add_argument("command", choices=["status", "run", "verify", "audit", "serve"], help="Command to execute")
    parser.add_argument("--port", type=int, default=8000, help="Port for dashboard web server")
    args = parser.parse_args()

    if args.command == "status":
        show_status()
    elif args.command == "run":
        run_pipeline()
    elif args.command == "verify":
        run_verify()
    elif args.command == "audit":
        show_audit()
    elif args.command == "serve":
        serve_dashboard(args.port)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        show_status()
    else:
        main()
