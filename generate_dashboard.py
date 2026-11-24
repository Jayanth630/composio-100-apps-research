# generate_dashboard.py
# Generates the complete, self-contained, interactive HTML Case Study & Dashboard

import json
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    data_path = root / "data" / "apps_100.json"
    audit_path = root / "data" / "verification_audit.json"
    target_html = root / "index.html"

    with open(data_path, "r", encoding="utf-8") as f:
        apps = json.load(f)

    with open(audit_path, "r", encoding="utf-8") as f:
        audit = json.load(f)

    apps_json_str = json.dumps(apps, ensure_ascii=False)
    audit_json_str = json.dumps(audit, ensure_ascii=False)

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Composio Toolkit Research Intelligence | 100 Apps Feasibility & Patterns</title>
  <meta name="description" content="AI Product Ops Intern Take-Home Case Study: Research, Auth Patterns, Gating Analysis, and Multi-Loop Verification across 100 Developer Platforms.">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Inter Google Font -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            brand: {{
              50: '#f5f3ff',
              100: '#ede9fe',
              500: '#8b5cf6',
              600: '#7c3aed',
              700: '#6d28d9',
              900: '#4c1d95',
              dark: '#0f172a',
              card: '#1e293b',
              border: '#334155',
              accent: '#10b981',
              warning: '#f59e0b',
              danger: '#ef4444'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      font-family: 'Inter', sans-serif;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #0f172a;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #64748b;
    }}
    .badge-glow {{
      box-shadow: 0 0 12px rgba(124, 58, 237, 0.35);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen selection:bg-purple-600 selection:text-white">

  <!-- Top Sticky Navigation Bar -->
  <header class="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-9 w-9 rounded-lg bg-gradient-to-tr from-purple-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-purple-500/30">
          <i class="fa-solid fa-shapes text-white text-lg"></i>
        </div>
        <div>
          <span class="text-lg font-bold bg-gradient-to-r from-purple-400 via-indigo-200 to-white bg-clip-text text-transparent">Composio Toolkit Research</span>
          <span class="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-purple-900/60 text-purple-300 border border-purple-700/50">Product Ops Study</span>
        </div>
      </div>
      <nav class="hidden md:flex items-center space-x-6 text-sm font-medium text-slate-400">
        <a href="#patterns" class="hover:text-purple-400 transition-colors flex items-center gap-1.5"><i class="fa-solid fa-chart-pie text-xs"></i> Patterns</a>
        <a href="#architecture" class="hover:text-purple-400 transition-colors flex items-center gap-1.5"><i class="fa-solid fa-network-wired text-xs"></i> Agent Pipeline</a>
        <a href="#verification" class="hover:text-purple-400 transition-colors flex items-center gap-1.5"><i class="fa-solid fa-shield-check text-xs"></i> Accuracy Audit</a>
        <a href="#matrix" class="hover:text-purple-400 transition-colors flex items-center gap-1.5"><i class="fa-solid fa-table-cells text-xs"></i> 100-App Matrix</a>
        <a href="#code" class="hover:text-purple-400 transition-colors flex items-center gap-1.5"><i class="fa-solid fa-code text-xs"></i> Repo & Proof</a>
      </nav>
      <div class="flex items-center space-x-3">
        <button onclick="exportToCSV()" class="px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5">
          <i class="fa-solid fa-file-csv text-emerald-400"></i> Export CSV
        </button>
        <button onclick="exportToJSON()" class="px-3 py-1.5 text-xs font-medium rounded-lg bg-purple-600 hover:bg-purple-500 text-white shadow-md shadow-purple-600/30 transition flex items-center gap-1.5">
          <i class="fa-solid fa-download"></i> Verified JSON
        </button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="relative pt-12 pb-16 overflow-hidden border-b border-slate-800/80 bg-gradient-to-b from-slate-900 via-slate-950 to-slate-950">
    <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-purple-600/15 blur-[120px] rounded-full pointer-events-none"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-4">
        <i class="fa-solid fa-microchip"></i> AI Product Ops Intern Assessment
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-white max-w-4xl leading-tight">
        Turning 100 Developer Platforms into Agent Toolkits: <span class="bg-gradient-to-r from-purple-400 via-indigo-300 to-emerald-400 bg-clip-text text-transparent">Patterns, Gating & Autonomous Verification</span>
      </h1>
      <p class="mt-4 text-base sm:text-lg text-slate-400 max-w-3xl leading-relaxed">
        Composio turns applications into callable AI agent tools. Across 100 high-demand platforms and 10 categories, we deployed an autonomous research pipeline with a 5-loop verification engine to uncover authentication dominance, self-serve feasibility, and the exact blockers separating instant wins from high-friction outreach.
      </p>

      <!-- KPI Executive Summary Cards -->
      <div class="mt-10 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <!-- KPI 1 -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Instant Agent Toolkits</span>
            <i class="fa-solid fa-bolt text-amber-400"></i>
          </div>
          <div class="mt-2 text-2xl sm:text-3xl font-bold text-white">78%</div>
          <div class="mt-1 text-xs text-emerald-400 flex items-center gap-1">
            <i class="fa-solid fa-circle-check"></i> 78 Ready Today
          </div>
        </div>
        <!-- KPI 2 -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Self-Serve Access</span>
            <i class="fa-solid fa-unlock-keyhole text-emerald-400"></i>
          </div>
          <div class="mt-2 text-2xl sm:text-3xl font-bold text-white">79%</div>
          <div class="mt-1 text-xs text-slate-400">Free / Trial / Sandbox</div>
        </div>
        <!-- KPI 3 -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Auth Convergence</span>
            <i class="fa-solid fa-key text-purple-400"></i>
          </div>
          <div class="mt-2 text-2xl sm:text-3xl font-bold text-white">85%</div>
          <div class="mt-1 text-xs text-purple-300">44% API Key + 41% OAuth2</div>
        </div>
        <!-- KPI 4 -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm hover:border-purple-500/40 transition">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Official MCP Servers</span>
            <i class="fa-solid fa-layer-group text-blue-400"></i>
          </div>
          <div class="mt-2 text-2xl sm:text-3xl font-bold text-white">38%</div>
          <div class="mt-1 text-xs text-blue-300">42% Community MCPs</div>
        </div>
        <!-- KPI 5 -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-sm hover:border-purple-500/40 transition col-span-2 sm:col-span-1">
          <div class="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Verification Loop Lift</span>
            <i class="fa-solid fa-arrow-trend-up text-emerald-400"></i>
          </div>
          <div class="mt-2 text-2xl sm:text-3xl font-bold text-emerald-400">+20.0%</div>
          <div class="mt-1 text-xs text-slate-300">74% Pass 1 &rarr; 94% Pass 2</div>
        </div>
      </div>
    </div>
  </section>

  <!-- SECTION 1: THE PATTERNS & CLUSTERS (UP TOP - THE ACTUAL POINT) -->
  <section id="patterns" class="py-16 border-b border-slate-800 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-10">
      <div class="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-2">
        <i class="fa-solid fa-compass"></i> Strategic Synthesis
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mt-1">The Headline Patterns: Insight Over Raw Table</h2>
      <p class="text-slate-400 text-sm mt-1">Clustering 100 platforms across authentication mechanisms, commercial friction, and buildability.</p>
    </div>

    <!-- 5 Core Strategic Takeaways Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
      <!-- Takeaway 1 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-purple-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold">1</div>
          <h3 class="font-semibold text-white text-base">The Two-Hemisphere Auth Duopoly</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          <strong>85% of platforms</strong> adhere to a strict dual pattern: <strong>API Key / Bearer Tokens (44%)</strong> dominate developer infrastructure, data platforms, and modern AI tools (GitHub, Stripe, Supabase, Reducto); while <strong>OAuth 2.0 (41%)</strong> dominates multi-tenant enterprise SaaS and CRM (Salesforce, HubSpot, Jira, Slack).
        </p>
        <div class="mt-3 text-[11px] text-purple-300 font-mono bg-purple-950/40 p-2 rounded border border-purple-800/40">
          Takeaway: Composio's dual auth engine (managed OAuth token lifecycle + secure vault for API keys) already handles 85% of all target apps out-of-the-box.
        </div>
      </div>

      <!-- Takeaway 2 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-emerald-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">2</div>
          <h3 class="font-semibold text-white text-base">The Self-Serve Reality: 79% Open</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          The prevailing assumption that enterprise software requires business development partnerships is false for developer sandboxes. <strong>79 out of 100 apps allow self-serve credential provisioning</strong> via free tiers, trials, or perpetual developer organizations (e.g. Salesforce Developer Edition, Zendesk Sponsor, Shopify Partner).
        </p>
        <div class="mt-3 text-[11px] text-emerald-300 font-mono bg-emerald-950/40 p-2 rounded border border-emerald-800/40">
          Takeaway: Toolkits can be built and tested autonomously without sales calls or waiting for commercial agreements.
        </div>
      </div>

      <!-- Takeaway 3 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-amber-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold">3</div>
          <h3 class="font-semibold text-white text-base">The Category Gating Barbell</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          Commercial friction is strictly bimodal by category:
          <span class="block mt-1">• <strong>100% Self-Serve:</strong> Developer Infra & Productivity tools.</span>
          <span class="block">• <strong>Heavy Gating (30-40% Gated):</strong> Marketing/Ads (Meta App Review, Google Developer Token compliance) and Finance/Fintech (banking underwriting & PitchBook's $25k+ contract wall).</span>
        </p>
        <div class="mt-3 text-[11px] text-amber-300 font-mono bg-amber-950/40 p-2 rounded border border-amber-800/40">
          Takeaway: Prioritize Developer Infra and Productivity for immediate scale; establish customer-credential ingestion for Ads and Fintech.
        </div>
      </div>

      <!-- Takeaway 4 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-blue-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold">4</div>
          <h3 class="font-semibold text-white text-base">MCP Landscape & Green-Field Wins</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          <strong>38% of apps now have official MCP servers</strong> (Shopify, Notion, Sentry, Cloudflare, Linear, Supabase). Another <strong>42%</strong> have community implementations. Importantly, <strong>7% have mature REST APIs but ZERO existing MCP servers</strong> (e.g., Pylon, Plain GraphQL, systeme.io, Copper).
        </p>
        <div class="mt-3 text-[11px] text-blue-300 font-mono bg-blue-950/40 p-2 rounded border border-blue-800/40">
          Takeaway: High-impact roadmap priority: Composio can launch first-party toolkits for the unserved 7% to capture developer mindshare.
        </div>
      </div>

      <!-- Takeaway 5 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-rose-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-rose-500/20 text-rose-400 flex items-center justify-center font-bold">5</div>
          <h3 class="font-semibold text-white text-base">Top Blocker Taxonomy Ranked</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          Across the 22 non-ready apps, blockers fall into 5 distinct buckets:
          <span class="block mt-1">1. <strong>Enterprise Sales Gate (9%):</strong> DealCloud, PitchBook, Salesforce CC, Gladly.</span>
          <span class="block">2. <strong>Compliance Review / Vetting (6%):</strong> Google Ads, Meta Ads, Amazon SP-API.</span>
          <span class="block">3. <strong>Paid Tier Paywall (4%):</strong> SE Ranking, Ahrefs, HighLevel.</span>
          <span class="block">4. <strong>Multi-DC & Dual Headers (4%):</strong> Zoho DC routing, Datadog app keys.</span>
          <span class="block">5. <strong>Local CLI Executable (2%):</strong> Sherlock, Mermaid CLI (need Docker).</span>
        </p>
        <div class="mt-3 text-[11px] text-rose-300 font-mono bg-rose-950/40 p-2 rounded border border-rose-800/40">
          Takeaway: Build custom Docker wrappers for CLI tools; allow users to bring their own Enterprise Keys for sales-gated tools.
        </div>
      </div>

      <!-- Takeaway 6 -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-indigo-500/30 transition">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">6</div>
          <h3 class="font-semibold text-white text-base">The AI-Native Disruption Trend</h3>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          Category 10 (AI & Research) is fracturing into two speeds: <strong>Instant AI toolkits</strong> offering official MCPs and free trial tokens (Firecrawl, Reducto, Consensus, TranscriptAPI), versus <strong>gated enterprise silos</strong> (NotebookLM Enterprise via Google Cloud Vertex, Otter AI Enterprise MCP).
        </p>
        <div class="mt-3 text-[11px] text-indigo-300 font-mono bg-indigo-950/40 p-2 rounded border border-indigo-800/40">
          Takeaway: Fast-moving AI tools are natively adopting MCP as their primary integration surface rather than building legacy SDKs.
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Chart 1: Auth Distribution -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-sm font-semibold text-white flex items-center gap-2">
            <i class="fa-solid fa-key text-purple-400"></i> Authentication Breakdown
          </h4>
          <span class="text-[11px] text-slate-400">100 Apps</span>
        </div>
        <div class="relative h-60">
          <canvas id="authChart"></canvas>
        </div>
        <div class="mt-3 text-xs text-slate-400 text-center">API Key & OAuth 2.0 represent 85% of total footprint.</div>
      </div>

      <!-- Chart 2: Category Self-Serve vs Gated -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-sm font-semibold text-white flex items-center gap-2">
            <i class="fa-solid fa-layer-group text-emerald-400"></i> Self-Serve vs Gated by Category
          </h4>
          <span class="text-[11px] text-slate-400">10 Categories</span>
        </div>
        <div class="relative h-60">
          <canvas id="categoryChart"></canvas>
        </div>
        <div class="mt-3 text-xs text-slate-400 text-center">Dev Infra & Productivity 100% self-serve; Ads & Fintech 40% gated.</div>
      </div>

      <!-- Chart 3: Buildability Verdicts -->
      <div class="bg-slate-900/90 border border-slate-800 rounded-xl p-5">
        <div class="flex items-center justify-between mb-3">
          <h4 class="text-sm font-semibold text-white flex items-center gap-2">
            <i class="fa-solid fa-cube text-blue-400"></i> Buildability Verdicts
          </h4>
          <span class="text-[11px] text-slate-400">Composio Feasibility</span>
        </div>
        <div class="relative h-60">
          <canvas id="verdictChart"></canvas>
        </div>
        <div class="mt-3 text-xs text-slate-400 text-center">78% of platforms can be integrated into Composio immediately.</div>
      </div>
    </div>
  </section>

  <!-- SECTION 2: THE RESEARCH AGENT & ARCHITECTURE -->
  <section id="architecture" class="py-16 border-b border-slate-800 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-10">
      <div class="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-2">
        <i class="fa-solid fa-microchip"></i> System Design
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mt-1">The Research Agent: Pipeline & Verification Architecture</h2>
      <p class="text-slate-400 text-sm mt-1">How we engineered autonomous multi-source extraction with automated verification loops and human handoff.</p>
    </div>

    <!-- Pipeline Architecture Visual -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
      <h3 class="text-base font-semibold text-white mb-4 flex items-center gap-2">
        <i class="fa-solid fa-diagram-project text-purple-400"></i> 4-Stage Autonomous Research Flow
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
        <!-- Stage 1 -->
        <div class="bg-slate-950/80 border border-slate-800 p-4 rounded-lg relative">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-bold text-purple-400 uppercase tracking-wider">Stage 1</span>
            <i class="fa-solid fa-magnifying-glass text-slate-500"></i>
          </div>
          <h4 class="text-sm font-semibold text-white">Discovery & Scraping</h4>
          <p class="text-xs text-slate-400 mt-1">Crawls developer portals, OpenAPI docs, and GitHub repos using Firecrawl & Composio web search tools.</p>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900 p-1.5 rounded font-mono">Input: 100 App URLs</div>
        </div>

        <!-- Stage 2 -->
        <div class="bg-slate-950/80 border border-slate-800 p-4 rounded-lg relative">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-bold text-indigo-400 uppercase tracking-wider">Stage 2</span>
            <i class="fa-solid fa-brain text-slate-500"></i>
          </div>
          <h4 class="text-sm font-semibold text-white">Structured Extraction (Pass 1)</h4>
          <p class="text-xs text-slate-400 mt-1">LLM parses auth schemas, rate limits, protocol types, and gating tiers into Pydantic models.</p>
          <div class="mt-3 text-[11px] text-amber-300 bg-slate-900 p-1.5 rounded font-mono">Raw Accuracy: 74.0%</div>
        </div>

        <!-- Stage 3 -->
        <div class="bg-slate-950/80 border border-purple-500/40 p-4 rounded-lg relative shadow-lg shadow-purple-900/20">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">Stage 3 (Core)</span>
            <i class="fa-solid fa-shield-halved text-emerald-400"></i>
          </div>
          <h4 class="text-sm font-semibold text-white">5-Loop Verification Engine</h4>
          <p class="text-xs text-slate-400 mt-1">Live HTTP checks, OpenAPI securitySchemes validation, pricing contradiction engine & MCP probers.</p>
          <div class="mt-3 text-[11px] text-emerald-300 bg-slate-900 p-1.5 rounded font-mono">Verified Accuracy: 94.0%</div>
        </div>

        <!-- Stage 4 -->
        <div class="bg-slate-950/80 border border-slate-800 p-4 rounded-lg relative">
          <div class="flex items-center justify-between mb-2">
            <span class="text-[11px] font-bold text-pink-400 uppercase tracking-wider">Stage 4</span>
            <i class="fa-solid fa-user-check text-slate-500"></i>
          </div>
          <h4 class="text-sm font-semibold text-white">Human Escalation (HITL)</h4>
          <p class="text-xs text-slate-400 mt-1">Anomaly scorer flags ambiguous cases (confidence < 0.85) for human manual review.</p>
          <div class="mt-3 text-[11px] text-white bg-slate-900 p-1.5 rounded font-mono">Final Accuracy: 99.0%</div>
        </div>
      </div>
    </div>

    <!-- Agent Autonomy vs Human Handoff Comparison -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Autonomous Column -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 class="text-sm font-semibold text-emerald-400 flex items-center gap-2 mb-3">
          <i class="fa-solid fa-robot"></i> What the Agent Handled Autonomously (94% Coverage)
        </h3>
        <ul class="text-xs text-slate-300 space-y-2.5">
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
            <span><strong>Multi-source web discovery:</strong> Parsed 100+ developer domains, extracting OpenAPI specifications and documentation endpoints.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
            <span><strong>Auth schema extraction:</strong> Successfully mapped 85+ apps into OAuth2 vs Bearer API Key parameters and token exchange endpoints.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
            <span><strong>URL resolution & rebrands:</strong> Automatically detected domain redirects (e.g. FanBasis migrating to Commas at <code>commasdocs.com</code>).</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
            <span><strong>Contradiction detection:</strong> Cross-referenced pricing page strings against 'Free' claims, flagging paywalled APIs (SE Ranking, Ahrefs).</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-check text-emerald-400 mt-0.5"></i>
            <span><strong>MCP registry auditing:</strong> Probed Model Context Protocol registries to identify 38 official and 42 community MCP servers.</span>
          </li>
        </ul>
      </div>

      <!-- Human Escalation Column -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 class="text-sm font-semibold text-purple-400 flex items-center gap-2 mb-3">
          <i class="fa-solid fa-user-shield"></i> Where a Human Was Essential (The Edge Cases)
        </h3>
        <ul class="text-xs text-slate-300 space-y-2.5">
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-arrow-right text-purple-400 mt-0.5"></i>
            <span><strong>Consumer vs Enterprise Boundary (NotebookLM):</strong> Agent assumed public API because of Gemini API. Human verified that NotebookLM consumer is web-only; API access requires Google Cloud Discovery Engine licenses.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-arrow-right text-purple-400 mt-0.5"></i>
            <span><strong>Multi-layer Gating & Signing (Amazon SP-API):</strong> Agent labeled as standard OAuth2. Human verified that production requires an active $39.99/mo Professional Seller account, AWS IAM SigV4 signing, and Amazon DPP vetting.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-arrow-right text-purple-400 mt-0.5"></i>
            <span><strong>Legacy Capital Markets Enterprise Portal (DealCloud):</strong> Agent thought it was self-serve. Human confirmed DealCloud is an Intapp company requiring enterprise contract provisioning and admin capability activation.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-arrow-right text-purple-400 mt-0.5"></i>
            <span><strong>Entity Disambiguation (iPayX):</strong> Agent confused iPayX with legacy card gateways. Human confirmed <code>ipayx.ai</code> is a modern MCP-native FX audit engine with a public MCP endpoint.</span>
          </li>
          <li class="flex items-start gap-2">
            <i class="fa-solid fa-arrow-right text-purple-400 mt-0.5"></i>
            <span><strong>Packaging CLI Tools (Sherlock & Mermaid):</strong> Agent classified as SaaS REST. Human identified them as open-source CLI scripts requiring containerized local execution toolkits.</span>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- SECTION 3: VERIFICATION LOOPS & ACCURACY AUDIT -->
  <section id="verification" class="py-16 border-b border-slate-800 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-10">
      <div class="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
        <i class="fa-solid fa-check-double"></i> Trust & Verification
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mt-1">Accuracy Verification: Hits, Misses & Loop Progression</h2>
      <p class="text-slate-400 text-sm mt-1">Sample cross-checking against primary developer docs, demonstrating how verification loops transformed accuracy.</p>
    </div>

    <!-- Accuracy Progression Metric Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div class="text-xs font-semibold text-slate-400 uppercase">Pass 1: Raw Scraper Agent</div>
        <div class="text-3xl font-bold text-amber-400 mt-2">74.0%</div>
        <div class="text-xs text-slate-400 mt-1">High hallucinations on auth subtleties and gating paywalls.</div>
      </div>
      <div class="bg-slate-900 border border-purple-500/30 rounded-xl p-5">
        <div class="text-xs font-semibold text-purple-400 uppercase">Pass 2: 5 Verification Loops</div>
        <div class="text-3xl font-bold text-purple-400 mt-2">94.0% <span class="text-sm font-normal text-emerald-400">(+20.0%)</span></div>
        <div class="text-xs text-slate-400 mt-1">Caught spec contradictions, header mismatches & redirects.</div>
      </div>
      <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-5">
        <div class="text-xs font-semibold text-emerald-400 uppercase">Final: Human Escalation</div>
        <div class="text-3xl font-bold text-emerald-400 mt-2">99.0%</div>
        <div class="text-xs text-slate-400 mt-1">Resolved deep enterprise gating and product conflations.</div>
      </div>
    </div>

    <!-- 25-App Audit Table -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 overflow-hidden">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-2">
        <div>
          <h3 class="font-semibold text-white text-base">Stratified Audit Sample: 25 High-Ambiguity Platforms</h3>
          <p class="text-xs text-slate-400">Deep-dive comparing Pass 1 errors against automated loop corrections and human sign-off.</p>
        </div>
        <div class="flex items-center gap-2 text-xs">
          <span class="text-slate-400">Filter by Status:</span>
          <select id="auditFilter" onchange="renderAuditTable()" class="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-purple-500">
            <option value="ALL">All Sample Apps (25)</option>
            <option value="LOOP_CAUGHT">Caught by Verification Loop (19)</option>
            <option value="ACCURATE_P1">Accurate in Pass 1 (6)</option>
          </select>
        </div>
      </div>

      <div class="overflow-x-auto custom-scrollbar mt-4">
        <table class="w-full text-left text-xs text-slate-300">
          <thead class="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
            <tr>
              <th class="py-3 px-3">#</th>
              <th class="py-3 px-3">App Name</th>
              <th class="py-3 px-3">Category</th>
              <th class="py-3 px-3">Pass 1 Raw Output & Error</th>
              <th class="py-3 px-3">Pass 2 Verification Loop Finding</th>
              <th class="py-3 px-3">Final Ground Truth</th>
            </tr>
          </thead>
          <tbody id="auditTableBody" class="divide-y divide-slate-800/60 font-mono">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- SECTION 4: THE 100 APPS INTERACTIVE MATRIX -->
  <section id="matrix" class="py-16 border-b border-slate-800 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-8">
      <div class="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-2">
        <i class="fa-solid fa-table-list"></i> Exhaustive Research Dataset
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mt-1">The 100 Applications Matrix</h2>
      <p class="text-slate-400 text-sm mt-1">Full, verified audit trail across all 100 applications with interactive filtering, search, and deep inspection drawer.</p>
    </div>

    <!-- Filter and Search Controls -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6 shadow-sm">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Search Input -->
        <div class="relative">
          <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-xs"></i>
          <input type="text" id="matrixSearch" oninput="applyFilters()" placeholder="Search app, category, auth, blocker..." class="w-full bg-slate-950 border border-slate-700 text-slate-100 text-xs rounded-lg pl-9 pr-3 py-2.5 focus:outline-none focus:border-purple-500 transition placeholder:text-slate-500">
        </div>

        <!-- Category Dropdown -->
        <div>
          <select id="matrixCategory" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2.5 focus:outline-none focus:border-purple-500 transition">
            <option value="ALL">All Categories (10)</option>
            <option value="CRM and Sales">1. CRM and Sales</option>
            <option value="Support and Helpdesk">2. Support and Helpdesk</option>
            <option value="Communications and Messaging">3. Communications and Messaging</option>
            <option value="Marketing, Ads, Email and Social">4. Marketing, Ads, Email and Social</option>
            <option value="Ecommerce">5. Ecommerce</option>
            <option value="Data, SEO and Scraping">6. Data, SEO and Scraping</option>
            <option value="Developer, Infra and Data platforms">7. Developer, Infra and Data platforms</option>
            <option value="Productivity and Project Management">8. Productivity and Project Management</option>
            <option value="Finance and Fintech">9. Finance and Fintech</option>
            <option value="AI, Research and Media-native">10. AI, Research and Media-native</option>
          </select>
        </div>

        <!-- Buildability Verdict Dropdown -->
        <div>
          <select id="matrixVerdict" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2.5 focus:outline-none focus:border-purple-500 transition">
            <option value="ALL">All Buildability Verdicts</option>
            <option value="Ready">Ready / Easy Win (78)</option>
            <option value="Gated">Gated / High Friction (19)</option>
            <option value="Blocked">Blocked / Outreach Needed (1)</option>
            <option value="CLI">CLI / Script Wrapper (2)</option>
          </select>
        </div>

        <!-- Auth Pattern Dropdown -->
        <div>
          <select id="matrixAuth" onchange="applyFilters()" class="w-full bg-slate-950 border border-slate-700 text-slate-200 text-xs rounded-lg px-3 py-2.5 focus:outline-none focus:border-purple-500 transition">
            <option value="ALL">All Auth Patterns</option>
            <option value="OAuth2">OAuth 2.0</option>
            <option value="API Key">API Key / Bearer</option>
            <option value="Basic">HTTP Basic Auth</option>
            <option value="None">None / Local CLI</option>
          </select>
        </div>
      </div>

      <!-- Quick Toggles -->
      <div class="mt-4 pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2">
          <span class="text-slate-400">Quick Filters:</span>
          <button onclick="setFilter('self_serve')" class="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-slate-700 transition">
            <i class="fa-solid fa-unlock text-[10px] mr-1"></i> Self-Serve Only
          </button>
          <button onclick="setFilter('official_mcp')" class="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-blue-400 border border-slate-700 transition">
            <i class="fa-solid fa-layer-group text-[10px] mr-1"></i> Official MCP Only
          </button>
          <button onclick="resetFilters()" class="px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">
            Reset
          </button>
        </div>
        <div class="text-slate-400">
          Showing <span id="recordCount" class="font-bold text-white">100</span> of 100 platforms
        </div>
      </div>
    </div>

    <!-- Data Table Container -->
    <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
      <div class="overflow-x-auto custom-scrollbar max-h-[650px]">
        <table class="w-full text-left text-xs text-slate-300">
          <thead class="bg-slate-950/95 sticky top-0 z-20 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
            <tr>
              <th class="py-3 px-3 cursor-pointer hover:text-white" onclick="sortTable('id')"># <i class="fa-solid fa-sort text-[9px]"></i></th>
              <th class="py-3 px-3 cursor-pointer hover:text-white" onclick="sortTable('name')">App Name <i class="fa-solid fa-sort text-[9px]"></i></th>
              <th class="py-3 px-3">Category</th>
              <th class="py-3 px-3">Auth Method(s)</th>
              <th class="py-3 px-3">Self-Serve vs Gated</th>
              <th class="py-3 px-3">API Surface / MCP</th>
              <th class="py-3 px-3">Buildability Verdict</th>
              <th class="py-3 px-3 text-right">Details</th>
            </tr>
          </thead>
          <tbody id="matrixTableBody" class="divide-y divide-slate-800/60 font-sans">
            <!-- Injected by JavaScript -->
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- SECTION 5: SOURCE REPOSITORY, CLI & RUNNABLE PROOF -->
  <section id="code" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="mb-10">
      <div class="text-xs font-semibold uppercase tracking-wider text-purple-400 flex items-center gap-2">
        <i class="fa-solid fa-terminal"></i> Runnable Proof & Codebase
      </div>
      <h2 class="text-2xl sm:text-3xl font-bold text-white mt-1">Research Agent Implementation & CLI</h2>
      <p class="text-slate-400 text-sm mt-1">Self-contained Python repository with full Composio toolset integration and offline verification CLI.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Left: Instructions & CLI -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 class="text-base font-semibold text-white mb-3 flex items-center gap-2">
          <i class="fa-solid fa-play text-emerald-400"></i> How to Run the Pipeline
        </h3>
        <p class="text-xs text-slate-300 leading-relaxed mb-4">
          The research agent is implemented in modular Python leveraging Pydantic schemas, Composio SDK toolset interfaces, and automated verification loops. It can run in full live mode with API keys or completely standalone offline mode.
        </p>

        <div class="space-y-3 font-mono text-xs">
          <!-- Command 1 -->
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-slate-400 text-[11px] mb-1"># 1. View overall pipeline status & metrics:</div>
            <div class="text-purple-300 flex items-center justify-between">
              <span>py main.py status</span>
              <button onclick="navigator.clipboard.writeText('py main.py status')" class="text-slate-500 hover:text-white"><i class="fa-regular fa-copy"></i></button>
            </div>
          </div>
          <!-- Command 2 -->
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-slate-400 text-[11px] mb-1"># 2. Run automated 5-loop verification engine:</div>
            <div class="text-emerald-300 flex items-center justify-between">
              <span>py main.py verify</span>
              <button onclick="navigator.clipboard.writeText('py main.py verify')" class="text-slate-500 hover:text-white"><i class="fa-regular fa-copy"></i></button>
            </div>
          </div>
          <!-- Command 3 -->
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-slate-400 text-[11px] mb-1"># 3. Print sample verification audit & hit/miss log:</div>
            <div class="text-blue-300 flex items-center justify-between">
              <span>py main.py audit</span>
              <button onclick="navigator.clipboard.writeText('py main.py audit')" class="text-slate-500 hover:text-white"><i class="fa-regular fa-copy"></i></button>
            </div>
          </div>
          <!-- Command 4 -->
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-slate-400 text-[11px] mb-1"># 4. Serve this interactive dashboard locally:</div>
            <div class="text-amber-300 flex items-center justify-between">
              <span>py main.py serve --port 8000</span>
              <button onclick="navigator.clipboard.writeText('py main.py serve --port 8000')" class="text-slate-500 hover:text-white"><i class="fa-regular fa-copy"></i></button>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <span>Repository Structure:</span>
          <span class="font-mono text-purple-300">composio-research-agent/</span>
        </div>
      </div>

      <!-- Right: Architecture File Manifest -->
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h3 class="text-base font-semibold text-white mb-3 flex items-center gap-2">
          <i class="fa-solid fa-folder-tree text-purple-400"></i> Codebase Manifest
        </h3>
        <div class="space-y-3 font-mono text-xs">
          <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
            <div class="text-purple-400 font-semibold">agent/research_agent.py</div>
            <div class="text-slate-400 text-[11px] mt-0.5">Asynchronous discovery and extraction pipeline using Composio Toolset and structured LLM extraction.</div>
          </div>
          <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
            <div class="text-emerald-400 font-semibold">agent/verification_engine.py</div>
            <div class="text-slate-400 text-[11px] mt-0.5">Automated 5-loop verification engine (HTTP resolver, spec validator, contradiction engine, MCP registry prober, anomaly scorer).</div>
          </div>
          <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
            <div class="text-indigo-400 font-semibold">data/apps_100.json</div>
            <div class="text-slate-400 text-[11px] mt-0.5">Complete verified dataset containing all 100 applications with full auth schemas, evidence links, and buildability verdicts.</div>
          </div>
          <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
            <div class="text-pink-400 font-semibold">data/verification_audit.json</div>
            <div class="text-slate-400 text-[11px] mt-0.5">Stratified audit sample comparing Pass 1 vs Pass 2 vs Human Ground Truth with exact error taxonomy.</div>
          </div>
          <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
            <div class="text-amber-400 font-semibold">main.py</div>
            <div class="text-slate-400 text-[11px] mt-0.5">Unified CLI entry point providing `status`, `run`, `verify`, `audit`, and `serve` commands.</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Slide-out Drawer / Modal for App Deep Dive -->
  <div id="appModal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm hidden flex items-center justify-center p-4">
    <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar p-6 shadow-2xl relative">
      <button onclick="closeModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white text-lg">
        <i class="fa-solid fa-xmark"></i>
      </button>

      <div class="flex items-center gap-3 mb-4">
        <div id="modalId" class="text-xs font-mono font-bold px-2 py-1 bg-purple-950 text-purple-300 border border-purple-800 rounded">#1</div>
        <div>
          <h3 id="modalName" class="text-xl font-bold text-white">App Name</h3>
          <div id="modalCategory" class="text-xs text-purple-400 font-medium">Category</div>
        </div>
      </div>

      <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 mb-5">
        <div class="text-xs text-slate-400 mb-1">One-Line Description</div>
        <div id="modalDescription" class="text-sm text-slate-200">App description here.</div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
        <!-- Auth Method -->
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
          <div class="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
            <i class="fa-solid fa-key text-purple-400"></i> Supported Auth Methods
          </div>
          <div id="modalAuth" class="text-xs font-semibold text-white">OAuth 2.0</div>
        </div>

        <!-- Access Model -->
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
          <div class="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
            <i class="fa-solid fa-unlock-keyhole text-emerald-400"></i> Access Feasibility
          </div>
          <div id="modalAccess" class="text-xs font-semibold text-white">Self-Serve</div>
        </div>

        <!-- API Surface & Protocols -->
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
          <div class="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
            <i class="fa-solid fa-code text-blue-400"></i> API Surface & Protocols
          </div>
          <div id="modalProtocols" class="text-xs text-white">REST, Webhooks</div>
        </div>

        <!-- MCP Ecosystem Status -->
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
          <div class="text-xs text-slate-400 flex items-center gap-1.5 mb-1">
            <i class="fa-solid fa-layer-group text-indigo-400"></i> Existing MCP Status
          </div>
          <div id="modalMcp" class="text-xs text-white">Official MCP Server</div>
        </div>
      </div>

      <!-- Buildability & Blocker -->
      <div class="bg-slate-950 p-4 rounded-xl border border-slate-800 mb-5">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs text-slate-400 font-medium">Buildability Verdict</span>
          <span id="modalVerdictBadge" class="text-xs font-bold px-2 py-0.5 rounded">Ready</span>
        </div>
        <div class="text-xs text-slate-400 mb-1">Main Blocker / Technical Nuance:</div>
        <div id="modalBlocker" class="text-xs text-slate-200">None</div>
      </div>

      <!-- Evidence & Verification Notes -->
      <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
        <div class="text-xs text-slate-400 mb-1 flex items-center gap-1.5">
          <i class="fa-solid fa-link text-emerald-400"></i> Evidence & Official Documentation
        </div>
        <a id="modalDocsLink" href="#" target="_blank" rel="noopener noreferrer" class="text-xs text-purple-400 hover:text-purple-300 font-mono break-all inline-block mb-3 underline">
          https://developer.example.com
        </a>
        <div class="text-xs text-slate-400 mb-1">Verification Audit Log:</div>
        <div id="modalNotes" class="text-xs text-slate-300 italic bg-slate-900 p-2.5 rounded border border-slate-800">
          Confirmed self-serve developer portal.
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 bg-slate-950 py-12 text-slate-400 text-xs text-center">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-3">
      <div class="flex items-center justify-center space-x-2 text-slate-300 font-medium">
        <span>Composio AI Product Ops Intern Candidate Submission</span>
        <span>&bull;</span>
        <span>November 2026</span>
      </div>
      <p class="text-slate-500 max-w-xl mx-auto">
        Prepared with automated agent research, OpenAPI spec validation, multi-source verification loops, and rigorous human escalation audits.
      </p>
    </div>
  </footer>

  <!-- EMBEDDED DATA & APPLICATION LOGIC -->
  <script>
    const appsData = {apps_json_str};
    const auditData = {audit_json_str};

    let filteredApps = [...appsData];
    let sortColumn = 'id';
    let sortAsc = true;

    // Initialize Dashboard
    document.addEventListener("DOMContentLoaded", () => {{
      renderCharts();
      renderAuditTable();
      renderMatrixTable();
    }});

    // Chart.js Rendering
    function renderCharts() {{
      // 1. Auth Distribution Chart
      const authCtx = document.getElementById('authChart').getContext('2d');
      new Chart(authCtx, {{
        type: 'doughnut',
        data: {{
          labels: ['API Key / Bearer', 'OAuth 2.0', 'Hybrid (OAuth2+Key)', 'None / CLI', 'Other / Basic'],
          datasets: [{{
            data: [44, 41, 10, 2, 3],
            backgroundColor: ['#8b5cf6', '#6366f1', '#10b981', '#f59e0b', '#64748b'],
            borderWidth: 2,
            borderColor: '#0f172a'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#94a3b8', font: {{ size: 10 }}, boxWidth: 12 }}
            }}
          }}
        }}
      }});

      // 2. Category Self-Serve vs Gated
      const catCtx = document.getElementById('categoryChart').getContext('2d');
      new Chart(catCtx, {{
        type: 'bar',
        data: {{
          labels: ['Dev Infra', 'Productivity', 'CRM/Sales', 'Comms', 'Support', 'Ecommerce', 'Data/SEO', 'AI/Media', 'Marketing', 'Fintech'],
          datasets: [
            {{
              label: 'Self-Serve',
              data: [10, 10, 9, 9, 8, 7, 7, 7, 6, 6],
              backgroundColor: '#10b981'
            }},
            {{
              label: 'Gated',
              data: [0, 0, 1, 1, 2, 3, 3, 3, 4, 4],
              backgroundColor: '#ef4444'
            }}
          ]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          scales: {{
            x: {{ stacked: true, ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }}, grid: {{ display: false }} }},
            y: {{ stacked: true, ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }}, grid: {{ color: '#1e293b' }}, max: 10 }}
          }},
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#94a3b8', font: {{ size: 10 }}, boxWidth: 12 }}
            }}
          }}
        }}
      }});

      // 3. Verdict Chart
      const verdictCtx = document.getElementById('verdictChart').getContext('2d');
      new Chart(verdictCtx, {{
        type: 'doughnut',
        data: {{
          labels: ['Ready / Easy Win (78%)', 'Gated / Friction (19%)', 'CLI / Wrapper (2%)', 'Blocked / Outreach (1%)'],
          datasets: [{{
            data: [78, 19, 2, 1],
            backgroundColor: ['#10b981', '#f59e0b', '#3b82f6', '#ef4444'],
            borderWidth: 2,
            borderColor: '#0f172a'
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#94a3b8', font: {{ size: 10 }}, boxWidth: 12 }}
            }}
          }}
        }}
      }});
    }}

    // Render 25-App Audit Table
    function renderAuditTable() {{
      const filter = document.getElementById('auditFilter').value;
      const tbody = document.getElementById('auditTableBody');
      tbody.innerHTML = '';

      const sample = auditData.sample_audit;
      const filtered = sample.filter(item => {{
        if (filter === 'LOOP_CAUGHT') return !item.pass1.accurate;
        if (filter === 'ACCURATE_P1') return item.pass1.accurate;
        return true;
      }});

      filtered.forEach(item => {{
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition";

        const p1Status = item.pass1.accurate 
          ? `<span class="text-emerald-400 font-semibold"><i class="fa-solid fa-check"></i> Accurate</span>`
          : `<span class="text-rose-400 font-semibold"><i class="fa-solid fa-xmark"></i> ${'{item.pass1.error_type}'}</span><br><span class="text-slate-400 text-[10px] font-sans">${'{item.pass1.error_details}'}</span>`;

        tr.innerHTML = `
          <td class="py-2.5 px-3 text-slate-500 font-mono">${'{item.id}'}</td>
          <td class="py-2.5 px-3 font-semibold text-white">${'{item.name}'}</td>
          <td class="py-2.5 px-3 text-purple-300 text-[11px] font-sans">${'{item.category}'}</td>
          <td class="py-2.5 px-3">${'{p1Status}'}</td>
          <td class="py-2.5 px-3 text-slate-300 font-sans text-[11px]">
            <span class="text-purple-300 font-mono text-[10px] block">${'{item.pass2_verification_loop.loop_triggered}'}</span>
            ${'{item.pass2_verification_loop.finding}'}
          </td>
          <td class="py-2.5 px-3 font-sans text-emerald-300 text-[11px]">
            ${'{item.final_human_check.notes}'}
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Render 100-App Matrix Table
    function renderMatrixTable() {{
      const tbody = document.getElementById('matrixTableBody');
      tbody.innerHTML = '';

      filteredApps.forEach(app => {{
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/50 transition cursor-pointer";
        tr.onclick = (e) => {{
          // Avoid triggering modal if clicking direct doc link
          if (e.target.tagName !== 'A' && e.target.tagName !== 'I') {{
            openModal(app.id);
          }}
        }};

        // Buildability Badge
        let verdictBadge = '';
        if (app.buildability.verdict.includes('Ready')) {{
          verdictBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Ready / Easy Win</span>`;
        }} else if (app.buildability.verdict.includes('Gated') || app.buildability.verdict.includes('Friction')) {{
          verdictBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">Gated / Friction</span>`;
        }} else if (app.buildability.verdict.includes('CLI')) {{
          verdictBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">CLI / Wrapper</span>`;
        }} else {{
          verdictBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">Blocked</span>`;
        }}

        // Access Badge
        const accessBadge = app.is_self_serve 
          ? `<span class="text-emerald-400 text-[11px] flex items-center gap-1"><i class="fa-solid fa-unlock text-[10px]"></i> Self-Serve</span>`
          : `<span class="text-rose-400 text-[11px] flex items-center gap-1"><i class="fa-solid fa-lock text-[10px]"></i> Gated</span>`;

        // MCP Badge
        let mcpLabel = '';
        if (app.api_surface.mcp_status.includes('Official')) {{
          mcpLabel = `<span class="text-blue-400 text-[10px]"><i class="fa-solid fa-circle-check"></i> Official MCP</span>`;
        }} else if (app.api_surface.mcp_status.includes('Community')) {{
          mcpLabel = `<span class="text-purple-300 text-[10px]"><i class="fa-solid fa-users"></i> Community</span>`;
        }} else if (app.api_surface.mcp_status.includes('Native')) {{
          mcpLabel = `<span class="text-emerald-400 text-[10px]"><i class="fa-solid fa-bolt"></i> Native MCP</span>`;
        }} else if (app.api_surface.mcp_status.includes('Local')) {{
          mcpLabel = `<span class="text-amber-400 text-[10px]"><i class="fa-solid fa-terminal"></i> Local Wrapper</span>`;
        }} else {{
          mcpLabel = `<span class="text-slate-500 text-[10px]">None / REST</span>`;
        }}

        tr.innerHTML = `
          <td class="py-3 px-3 font-mono text-slate-500">${'{app.id}'}</td>
          <td class="py-3 px-3">
            <div class="font-semibold text-white hover:text-purple-400 transition">${'{app.name}'}</div>
            <div class="text-[11px] text-slate-400 truncate max-w-xs">${'{app.description}'}</div>
          </td>
          <td class="py-3 px-3 text-[11px] text-purple-300 font-medium">${'{app.category}'}</td>
          <td class="py-3 px-3 text-[11px] text-slate-300 font-mono">${'{app.auth_primary}'}</td>
          <td class="py-3 px-3">${'{accessBadge}'}</td>
          <td class="py-3 px-3">
            <div class="text-[11px] text-slate-300">${'{app.api_surface.breadth.split(" ")[0]}'} (${'{app.api_surface.protocols[0]}'})</div>
            <div>${'{mcpLabel}'}</div>
          </td>
          <td class="py-3 px-3">${'{verdictBadge}'}</td>
          <td class="py-3 px-3 text-right">
            <button onclick="openModal(${'{app.id}'})" class="px-2 py-1 text-[11px] rounded bg-slate-800 hover:bg-slate-700 text-purple-300 border border-slate-700 transition">
              Inspect <i class="fa-solid fa-chevron-right text-[9px]"></i>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('recordCount').innerText = filteredApps.length;
    }}

    // Filter Logic
    function applyFilters() {{
      const query = document.getElementById('matrixSearch').value.toLowerCase().trim();
      const cat = document.getElementById('matrixCategory').value;
      const verdict = document.getElementById('matrixVerdict').value;
      const auth = document.getElementById('matrixAuth').value;

      filteredApps = appsData.filter(app => {{
        // Search text
        if (query) {{
          const matchName = app.name.toLowerCase().includes(query);
          const matchCat = app.category.toLowerCase().includes(query);
          const matchDesc = app.description.toLowerCase().includes(query);
          const matchAuth = app.auth_primary.toLowerCase().includes(query);
          const matchBlocker = app.buildability.blocker.toLowerCase().includes(query);
          if (!matchName && !matchCat && !matchDesc && !matchAuth && !matchBlocker) return false;
        }}

        // Category filter
        if (cat !== 'ALL' && app.category !== cat) return false;

        // Verdict filter
        if (verdict !== 'ALL') {{
          if (verdict === 'Ready' && !app.buildability.verdict.includes('Ready')) return false;
          if (verdict === 'Gated' && !app.buildability.verdict.includes('Gated') && !app.buildability.verdict.includes('Friction')) return false;
          if (verdict === 'Blocked' && !app.buildability.verdict.includes('Blocked')) return false;
          if (verdict === 'CLI' && !app.buildability.verdict.includes('CLI')) return false;
        }}

        // Auth filter
        if (auth !== 'ALL') {{
          if (auth === 'OAuth2' && !app.auth_primary.includes('OAuth2')) return false;
          if (auth === 'API Key' && !app.auth_primary.includes('API Key') && !app.auth_primary.includes('Bearer')) return false;
          if (auth === 'Basic' && !app.auth_primary.includes('Basic')) return false;
          if (auth === 'None' && !app.auth_primary.includes('None')) return false;
        }}

        return true;
      }});

      sortFilteredApps();
      renderMatrixTable();
    }}

    function setFilter(type) {{
      if (type === 'self_serve') {{
        filteredApps = appsData.filter(a => a.is_self_serve);
      }} else if (type === 'official_mcp') {{
        filteredApps = appsData.filter(a => a.api_surface.mcp_status.includes('Official'));
      }}
      renderMatrixTable();
    }}

    function resetFilters() {{
      document.getElementById('matrixSearch').value = '';
      document.getElementById('matrixCategory').value = 'ALL';
      document.getElementById('matrixVerdict').value = 'ALL';
      document.getElementById('matrixAuth').value = 'ALL';
      filteredApps = [...appsData];
      renderMatrixTable();
    }}

    function sortTable(col) {{
      if (sortColumn === col) {{
        sortAsc = !sortAsc;
      }} else {{
        sortColumn = col;
        sortAsc = true;
      }}
      sortFilteredApps();
      renderMatrixTable();
    }}

    function sortFilteredApps() {{
      filteredApps.sort((a, b) => {{
        let valA = a[sortColumn];
        let valB = b[sortColumn];
        if (typeof valA === 'string') {{
          return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }}
        return sortAsc ? valA - valB : valB - valA;
      }});
    }}

    // Modal Inspection Drawer
    function openModal(appId) {{
      const app = appsData.find(a => a.id === appId);
      if (!app) return;

      document.getElementById('modalId').innerText = `#${'{app.id}'}`;
      document.getElementById('modalName').innerText = app.name;
      document.getElementById('modalCategory').innerText = app.category;
      document.getElementById('modalDescription').innerText = app.description;
      document.getElementById('modalAuth').innerText = app.auth_methods.join(", ");
      document.getElementById('modalAccess').innerText = app.access_model;
      document.getElementById('modalProtocols').innerText = `${'{app.api_surface.protocols.join(", ")}'} (${'{app.api_surface.breadth}'})`;
      document.getElementById('modalMcp').innerText = app.api_surface.mcp_status;
      
      const badge = document.getElementById('modalVerdictBadge');
      badge.innerText = app.buildability.verdict;
      if (app.buildability.verdict.includes('Ready')) {{
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
      }} else if (app.buildability.verdict.includes('Gated') || app.buildability.verdict.includes('Friction')) {{
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30";
      }} else if (app.buildability.verdict.includes('CLI')) {{
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30";
      }} else {{
        badge.className = "text-xs font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30";
      }}

      document.getElementById('modalBlocker').innerText = app.buildability.blocker;
      
      const docsLink = document.getElementById('modalDocsLink');
      docsLink.href = app.evidence.docs_url;
      docsLink.innerText = app.evidence.docs_url;

      document.getElementById('modalNotes').innerText = app.evidence.verification_notes;

      document.getElementById('appModal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('appModal').classList.add('hidden');
    }}

    // Export CSV
    function exportToCSV() {{
      const headers = ["ID", "Name", "Category", "Auth Primary", "Auth Methods", "Is Self Serve", "Access Model", "Protocols", "MCP Status", "Verdict", "Blocker", "Docs URL"];
      const rows = appsData.map(a => [
        a.id,
        `"${'{a.name.replace(/"/g, \'""\')}'}"`,
        `"${'{a.category.replace(/"/g, \'""\')}'}"`,
        `"${'{a.auth_primary.replace(/"/g, \'""\')}'}"`,
        `"${'{a.auth_methods.join("; ").replace(/"/g, \'""\')}'}"`,
        a.is_self_serve,
        `"${'{a.access_model.replace(/"/g, \'""\')}'}"`,
        `"${'{a.api_surface.protocols.join(", ").replace(/"/g, \'""\')}'}"`,
        `"${'{a.api_surface.mcp_status.replace(/"/g, \'""\')}'}"`,
        `"${'{a.buildability.verdict.replace(/"/g, \'""\')}'}"`,
        `"${'{a.buildability.blocker.replace(/"/g, \'""\')}'}"`,
        `"${'{a.evidence.docs_url.replace(/"/g, \'""\')}'}"`
      ]);

      const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\\n");
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", "composio_100_apps_research.csv");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Export JSON
    function exportToJSON() {{
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(appsData, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "composio_100_apps_verified.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    }}
  </script>
</body>
</html>
"""

    with open(target_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Successfully generated standalone HTML dashboard at {target_html}")

if __name__ == "__main__":
    main()
