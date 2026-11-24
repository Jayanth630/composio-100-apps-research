# analyze_patterns.py
# Computes clusters, distribution stats, and strategic takeaways from data/apps_100.json

import json
from collections import Counter, defaultdict
from pathlib import Path

def main():
    data_path = Path("e:/Employee Management System/composio-research-agent/data/apps_100.json")
    with open(data_path, "r", encoding="utf-8") as f:
        apps = json.load(f)

    total = len(apps)
    print(f"Loaded {total} apps.\n")

    # 1. Auth Distribution
    auth_counter = Counter()
    for app in apps:
        primary = app.get("auth_primary", "Other")
        # Simplify broad categories
        if "OAuth2" in primary and "API Key" in primary:
            auth_counter["Hybrid (OAuth2 + API Key)"] += 1
        elif "OAuth2" in primary:
            auth_counter["OAuth 2.0"] += 1
        elif "API Key" in primary or "Bearer Token" in primary:
            auth_counter["API Key / Bearer Token"] += 1
        elif "Basic Auth" in primary:
            auth_counter["HTTP Basic Auth"] += 1
        elif "AWS SigV4" in primary or "HMAC" in primary:
            auth_counter["Cryptographic Signing (SigV4 / HMAC)"] += 1
        elif "None (CLI)" in primary:
            auth_counter["None / CLI Wrapper"] += 1
        elif "MCP" in primary:
            auth_counter["Native MCP Server"] += 1
        else:
            auth_counter[primary] += 1

    print("=== AUTH DISTRIBUTION ===")
    for k, v in auth_counter.most_common():
        print(f"  {k}: {v} ({v/total*100:.1f}%)")
    print()

    # 2. Self-Serve vs Gated
    self_serve_count = sum(1 for a in apps if a["is_self_serve"])
    gated_count = total - self_serve_count
    print("=== ACCESS MODEL ===")
    print(f"  Self-Serve (Free / Trial / Dev Sandbox): {self_serve_count} ({self_serve_count/total*100:.1f}%)")
    print(f"  Gated (Paid Tier / Admin / Sales Contact): {gated_count} ({gated_count/total*100:.1f}%)")
    print()

    # 3. Category Breakdown (Self-Serve vs Gated)
    cat_stats = defaultdict(lambda: {"total": 0, "self_serve": 0, "gated": 0, "ready": 0, "friction": 0, "blocked": 0, "cli": 0})
    for a in apps:
        cat = a["category"]
        cat_stats[cat]["total"] += 1
        if a["is_self_serve"]:
            cat_stats[cat]["self_serve"] += 1
        else:
            cat_stats[cat]["gated"] += 1

        v = a["buildability"]["verdict"]
        if "Ready" in v:
            cat_stats[cat]["ready"] += 1
        elif "High Friction" in v or "Gated" in v:
            cat_stats[cat]["friction"] += 1
        elif "Blocked" in v or "Outreach" in v:
            cat_stats[cat]["blocked"] += 1
        elif "CLI" in v:
            cat_stats[cat]["cli"] += 1

    print("=== CATEGORY BREAKDOWN (SELF-SERVE vs GATED & BUILDABILITY) ===")
    for cat, stats in sorted(cat_stats.items(), key=lambda x: x[1]["self_serve"], reverse=True):
        ss_pct = (stats["self_serve"] / stats["total"]) * 100
        print(f"  {cat}: {stats['self_serve']}/{stats['total']} Self-Serve ({ss_pct:.0f}%) | Ready: {stats['ready']}, Friction: {stats['friction']}, Blocked: {stats['blocked']}, CLI: {stats['cli']}")
    print()

    # 4. Buildability Verdicts
    verdict_counter = Counter()
    for a in apps:
        v = a["buildability"]["verdict"]
        if "Ready" in v:
            verdict_counter["Ready / Easy Win (Instant Toolkit)"] += 1
        elif "High Friction" in v or "Gated" in v:
            verdict_counter["Gated / High Friction (Enterprise / Paid / Admin)"] += 1
        elif "Blocked" in v or "Outreach" in v:
            verdict_counter["Blocked / Outreach Needed (Enterprise Wall)"] += 1
        elif "CLI" in v:
            verdict_counter["CLI / Script Wrapper (Local / Container)"] += 1
        else:
            verdict_counter[v] += 1

    print("=== BUILDABILITY VERDICTS ===")
    for k, v in verdict_counter.most_common():
        print(f"  {k}: {v} ({v/total*100:.1f}%)")
    print()

    # 5. MCP Ecosystem Status
    mcp_counter = Counter()
    for a in apps:
        m = a["api_surface"]["mcp_status"]
        if "Official" in m:
            mcp_counter["Official MCP Server"] += 1
        elif "Community" in m:
            mcp_counter["Community MCP Available"] += 1
        elif "Native" in m:
            mcp_counter["Native MCP Server"] += 1
        elif "Local" in m:
            mcp_counter["Local MCP Wrapper"] += 1
        elif "Composio" in m:
            mcp_counter["Composio Native / Community MCP"] += 1
        elif "In Development" in m or "Available via REST" in m:
            mcp_counter["REST Only (Composio Opportunity)"] += 1
        else:
            mcp_counter["No MCP / Gated"] += 1

    print("=== MCP STATUS ===")
    for k, v in mcp_counter.most_common():
        print(f"  {k}: {v} ({v/total*100:.1f}%)")
    print()

    # 6. Blocker Analysis
    blocker_categories = Counter()
    for a in apps:
        b = a["buildability"]["blocker"]
        if "None" in b:
            blocker_categories["Zero Blocker (Frictionless / Instant)"] += 1
        elif "enterprise" in b.lower() or "sales" in b.lower() or "contract" in b.lower():
            blocker_categories["Enterprise Contract / Sales-Gated"] += 1
        elif "paid" in b.lower() or "subscription" in b.lower() or "tier" in b.lower():
            blocker_categories["Paid Subscription Tier Required"] += 1
        elif "review" in b.lower() or "verification" in b.lower() or "compliance" in b.lower() or "vetting" in b.lower():
            blocker_categories["Compliance Review / Developer Vetting Required"] += 1
        elif "cli" in b.lower() or "local" in b.lower() or "docker" in b.lower():
            blocker_categories["No Hosted API (Local Process / CLI Only)"] += 1
        elif "header" in b.lower() or "multi-datacenter" in b.lower() or "dc" in b.lower():
            blocker_categories["Technical Routing / Multi-Header Complexity"] += 1
        else:
            blocker_categories["Admin Approval / Workspace Scope"] += 1

    print("=== TOP BLOCKER CLUSTERS ===")
    for k, v in blocker_categories.most_common():
        print(f"  {k}: {v} ({v/total*100:.1f}%)")

if __name__ == "__main__":
    main()
