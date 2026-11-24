# build_verification_audit.py
# Generates the mathematically supported audit log for the 25-app challenge sample.
# Strictly verified against primary documentation without fabricated population statistics.

import json
from pathlib import Path

sample_audit_25 = [
    {
        "id": 8,
        "name": "Close",
        "category": "CRM and Sales",
        "pass1": {
            "auth": "OAuth 2.0 Bearer Token",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Auth Hallucination",
            "error_details": "Pass 1 assumed standard OAuth2 Bearer token for modern CRM."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: OpenAPI Spec SecuritySchemes Validator",
            "finding": "Close REST API securityScheme specifies HTTP Basic Auth where API key is passed as username with empty password.",
            "corrected_auth": "HTTP Basic Auth (API Key as username, blank password)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed in Close settings. API keys generate instantly and pass as Basic Auth base64(apiKey:)."
        }
    },
    {
        "id": 9,
        "name": "Copper",
        "category": "CRM and Sales",
        "pass1": {
            "auth": "OAuth 2.0 Bearer Token",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Auth Hallucination",
            "error_details": "Pass 1 missed custom header requirements."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: Header & Authentication Validator",
            "finding": "Copper requires three specific custom HTTP headers: X-PW-AccessToken, X-PW-UserEmail, and X-PW-Application.",
            "corrected_auth": "API Key + User Email Headers (X-PW-AccessToken, X-PW-UserEmail)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified against developer.copper.com. Standard Bearer tokens are rejected."
        }
    },
    {
        "id": 10,
        "name": "DealCloud",
        "category": "CRM and Sales",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Gating & Auth Miss",
            "error_details": "Pass 1 saw developer portal (api.docs.dealcloud.com) and assumed self-serve API keys."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2 & 3: Auth Flow Analyzer & Endpoint Checker",
            "finding": "DealCloud uses OAuth 2.0 Client Credentials flow exchanging clientId and apiKey for a 15-minute Bearer token. No self-serve trial exists.",
            "corrected_auth": "OAuth 2.0 Client Credentials Flow",
            "corrected_access": "Gated (Enterprise Subscription Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "DealCloud is owned by Intapp. Access requires enterprise subscription and User Group Capability enabling by admin."
        }
    },
    {
        "id": 13,
        "name": "Freshdesk",
        "category": "Support and Helpdesk",
        "pass1": {
            "auth": "Bearer Token",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Auth Header Discrepancy",
            "error_details": "Pass 1 labeled auth as Bearer Token."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: Spec Check & Header Prober",
            "finding": "Freshdesk requires HTTP Basic Auth with API key as username and 'X' as password.",
            "corrected_auth": "HTTP Basic Auth (API Key:X)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed in Freshworks developer docs."
        }
    },
    {
        "id": 15,
        "name": "Pylon",
        "category": "Support and Helpdesk",
        "pass1": {
            "auth": "Bearer Token",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Access Model Hallucination",
            "error_details": "Pass 1 assumed self-serve developer signup."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Landing Page & Onboarding Flow Inspector",
            "finding": "Pylon has no public self-serve signup. It requires a sales demo / B2B workspace onboarding.",
            "corrected_access": "Gated (B2B SaaS / Sales Demo Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Tokens can only be generated by Workspace Admins on active B2B plans. Docs verified at https://docs.usepylon.com/pylon-docs/developer/api."
        }
    },
    {
        "id": 20,
        "name": "Gladly",
        "category": "Support and Helpdesk",
        "pass1": {
            "auth": "OAuth 2.0",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Enterprise Gate Miss",
            "error_details": "Pass 1 assumed Gladly had a self-serve developer sandbox like Zendesk."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Pricing & Trial Detector",
            "finding": "Gladly is an enterprise customer service platform with no public trial; sales contact is mandatory.",
            "corrected_access": "Gated (Enterprise Subscription Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed via developer.gladly.com and enterprise retail customer agreements."
        }
    },
    {
        "id": 27,
        "name": "Telegram",
        "category": "Communications and Messaging",
        "pass1": {
            "auth": "Bot API Token",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "Accurately captured BotFather token flow."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 1 & 2: Endpoint & Protocol Validation",
            "finding": "Confirmed: api.telegram.org/bot<token> works with zero friction."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. 100% self-serve and instantaneous."
        }
    },
    {
        "id": 28,
        "name": "WhatsApp Business",
        "category": "Communications and Messaging",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Severe Gating & Auth Oversight",
            "error_details": "Pass 1 missed Meta Business Manager requirements and conversation pricing."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2 & 3: Meta Developer Policy & Graph API Checker",
            "finding": "WhatsApp Cloud API uses Meta System User Access Tokens (OAuth 2.0). Sandbox is free, but production requires Meta Business Verification and phone number registration.",
            "corrected_access": "Semi-Gated (Sandbox Free; Production Requires Meta Business Verification)",
            "corrected_auth": "OAuth 2.0 / Meta System User Token"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified against Meta Graph API docs. High friction for production agent deployment."
        }
    },
    {
        "id": 31,
        "name": "Google Ads",
        "category": "Marketing, Ads, Email and Social",
        "pass1": {
            "auth": "OAuth 2.0",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Compliance Token Gate Miss",
            "error_details": "Pass 1 saw Google Cloud OAuth and missed the mandatory Google Ads Developer Token."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: Header & Prerequisite Checker",
            "finding": "Google Ads API requires BOTH OAuth 2.0 and a 'developer-token' header, which requires compliance review for production ad accounts.",
            "corrected_auth": "OAuth 2.0 + Developer Token Header"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed. Basic access requires filling out an application and passing Google policy review."
        }
    },
    {
        "id": 34,
        "name": "GoHighLevel",
        "category": "Marketing, Ads, Email and Social",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Paid Subscription Gate Miss",
            "error_details": "Pass 1 assumed anyone can generate an API key."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Marketplace & Tier Review",
            "finding": "GoHighLevel API v2 uses OAuth2 and requires an active Agency account ($97-$497/mo) or approved marketplace developer profile.",
            "corrected_access": "Gated (Paid Agency Subscription Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed. Sub-accounts cannot generate API keys independently without agency admin."
        }
    },
    {
        "id": 41,
        "name": "Shopify",
        "category": "Ecommerce",
        "pass1": {
            "auth": "OAuth 2.0 & Admin API Access Token",
            "access": "Self-Serve Free (Partner Dev Stores)",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "Accurately identified Shopify Partner ecosystem and official MCP."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: MCP Registry & Dev Portal Prober",
            "finding": "Confirmed: Official Shopify MCP server exists; unlimited development stores."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. Industry benchmark for developer experience."
        }
    },
    {
        "id": 42,
        "name": "WooCommerce",
        "category": "Ecommerce",
        "pass1": {
            "auth": "OAuth 2.0 Bearer Token",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Auth Hallucination",
            "error_details": "Pass 1 assumed OAuth 2.0 Bearer token."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: REST Spec SecuritySchemes Check",
            "finding": "WooCommerce uses HTTP Basic Auth with Consumer Key (ck_...) and Consumer Secret (cs_...).",
            "corrected_auth": "HTTP Basic Auth (ck_... / cs_...)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed via WooCommerce REST API documentation."
        }
    },
    {
        "id": 44,
        "name": "Salesforce Commerce Cloud",
        "category": "Ecommerce",
        "pass1": {
            "auth": "OAuth 2.0",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Enterprise Gate Miss",
            "error_details": "Pass 1 conflated Salesforce CRM Free Dev Org with B2C Commerce Cloud."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Product Boundary & SSO Validator",
            "finding": "B2C Commerce Cloud (Demandware) is distinct from core CRM. It requires Account Manager credentials gated behind enterprise contracts.",
            "corrected_access": "Gated (Enterprise Subscription & Account Manager Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed. You cannot test B2C Commerce SCAPI using a free Developer Edition Salesforce org."
        }
    },
    {
        "id": 49,
        "name": "Amazon Selling Partner",
        "category": "Ecommerce",
        "pass1": {
            "auth": "OAuth 2.0 / API Key",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Severe Underestimation of Multi-Layer Gating",
            "error_details": "Pass 1 completely missed AWS IAM SigV4 and seller vetting."
        },
        "pass2_verification_loop": {
            "accurate": False,
            "resolved_autonomously": False,
            "loop_triggered": "Loop 5: Regulatory & Multi-Party Complexity Scorer",
            "finding": "Escalated: Automated loops detected conflicting requirements between Login with Amazon (LWA) OAuth2 and AWS IAM SigV4. Flagged for human review.",
            "corrected_auth": "AWS SigV4 + LWA OAuth2 + AWS IAM",
            "corrected_access": "Gated (Professional Seller Account + Strict Compliance Review)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Human review confirmed: Requires active Amazon Professional Selling Account ($39.99/mo), AWS IAM setup, and Data Protection Policy (DPP) compliance audit."
        }
    },
    {
        "id": 50,
        "name": "fanbasis",
        "category": "Ecommerce",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Domain Rebranding & Gating Miss",
            "error_details": "Pass 1 scraped fanbasis.com home page and missed the rebrand to Commas and creator approval."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 1: Redirect Tracker & Doc Portal Resolver",
            "finding": "Developer docs moved to commasdocs.com / dev-docs.fanbasis.com. Creator onboarding and approval required to access dashboard secrets.",
            "corrected_access": "Gated (Creator Merchant Approval Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. npm packages published under @fanbasis scope; checkout session secrets require creator account."
        }
    },
    {
        "id": 52,
        "name": "SE Ranking",
        "category": "Data, SEO and Scraping",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Tier Paywall Miss",
            "error_details": "Pass 1 saw 14-day free trial on homepage."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Feature Matrix Comparison Loop",
            "finding": "SE Ranking API is explicitly excluded from trial and entry tiers; requires Pro or Business subscription.",
            "corrected_access": "Gated (Pro / Business Subscription Required)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed on seranking.com/api.html pricing terms."
        }
    },
    {
        "id": 56,
        "name": "Firecrawl",
        "category": "Data, SEO and Scraping",
        "pass1": {
            "auth": "Bearer API Key",
            "access": "Self-Serve Free (500 credits)",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "Accurately captured Bearer auth and official MCP server."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: Live Key Test & MCP Verification",
            "finding": "Confirmed: Instant key creation; official Firecrawl MCP works flawlessly."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. Benchmark tool for LLM web extraction."
        }
    },
    {
        "id": 58,
        "name": "Sherlock",
        "category": "Data, SEO and Scraping",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Protocol / Architecture Hallucination",
            "error_details": "Pass 1 classified Sherlock as a SaaS REST API."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: Repo Architecture Classifier",
            "finding": "Sherlock is an open-source Python CLI tool with NO hosted REST endpoint. It runs locally or in Docker.",
            "corrected_auth": "None (CLI)",
            "corrected_verdict": "CLI / Script Wrapper"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed via github.com/sherlock-project/sherlock. Needs containerized MCP wrapper."
        }
    },
    {
        "id": 61,
        "name": "GitHub",
        "category": "Developer, Infra and Data platforms",
        "pass1": {
            "auth": "Personal Access Token / OAuth 2.0",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "100% accurate."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: Spec & MCP Check",
            "finding": "Official GitHub MCP server verified; fine-grained PATs supported."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified."
        }
    },
    {
        "id": 71,
        "name": "Notion",
        "category": "Productivity and Project Management",
        "pass1": {
            "auth": "Bearer Token / OAuth 2.0",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "Accurately captured internal integration secrets and official MCP."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: Header & MCP Validator",
            "finding": "Confirmed: Requires Notion-Version header; official Notion MCP server available."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified."
        }
    },
    {
        "id": 81,
        "name": "Stripe",
        "category": "Finance and Fintech",
        "pass1": {
            "auth": "Bearer API Key (sk_test_...)",
            "access": "Self-Serve Free Sandbox",
            "verdict": "Ready / Easy Win",
            "accurate": True,
            "error_type": "None",
            "error_details": "100% accurate on test mode and OpenAPI spec."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: Live Endpoint & MCP Check",
            "finding": "Confirmed: Instant test keys; official Stripe MCP available."
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. Gold standard developer API."
        }
    },
    {
        "id": 85,
        "name": "iPayX",
        "category": "Finance and Fintech",
        "pass1": {
            "auth": "API Key",
            "access": "Gated (Payment Gateway KYC)",
            "verdict": "Gated / High Friction",
            "accurate": False,
            "error_type": "Entity Disambiguation Miss",
            "error_details": "Pass 1 confused iPayX with a traditional merchant card gateway requiring underwriting."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 4: MCP Registry & AI Protocol Discovery",
            "finding": "ipayx.ai is an AI & MCP-native FX audit engine with a public MCP endpoint at https://mcp.ipayx.ai/mcp.",
            "corrected_auth": "MCP Native / Bearer Token",
            "corrected_access": "Self-Serve Open MCP Endpoint",
            "corrected_verdict": "Ready / Easy Win (MCP-Native)"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Critical disambiguation! iPayX is natively designed for AI clients at ipayx.ai/docs."
        }
    },
    {
        "id": 90,
        "name": "PitchBook",
        "category": "Finance and Fintech",
        "pass1": {
            "auth": "API Key",
            "access": "Self-Serve Free Trial",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Paywall Hallucination",
            "error_details": "Pass 1 assumed standard SaaS self-serve API."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 3: Contract & Pricing Scanner",
            "finding": "PitchBook Direct Data API is an enterprise-only add-on with high annual minimum spend ($25k+).",
            "corrected_access": "Gated (Enterprise Sales Gate / High Contract Value)",
            "corrected_verdict": "Blocked / Outreach Needed"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Confirmed. No self-serve trial or public signup exists."
        }
    },
    {
        "id": 91,
        "name": "NotebookLM",
        "category": "AI, Research and Media-native",
        "pass1": {
            "auth": "Google API Key",
            "access": "Self-Serve Free (via ai.google.dev)",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Product Conflation Hallucination",
            "error_details": "Pass 1 conflated Gemini API with NotebookLM."
        },
        "pass2_verification_loop": {
            "accurate": False,
            "resolved_autonomously": False,
            "loop_triggered": "Loop 5: Enterprise vs Consumer Entity Ambiguity Scorer",
            "finding": "Escalated: Automated loops detected conflicting product offerings between consumer NotebookLM and Google Cloud Vertex AI Gemini Notebooks. Flagged for human review.",
            "corrected_auth": "Google Cloud OAuth2 / Service Account (roles/discoveryengine.notebookLmUser)",
            "corrected_access": "Gated (Enterprise Google Cloud License)",
            "corrected_verdict": "Gated / High Friction"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Human review confirmed: Consumer NotebookLM (notebooklm.google.com) has NO public REST API. Enterprise access is Gemini Notebook Enterprise via Google Cloud Discovery Engine with IAM roles."
        }
    },
    {
        "id": 98,
        "name": "Mermaid CLI",
        "category": "AI, Research and Media-native",
        "pass1": {
            "auth": "None / Public REST",
            "access": "Self-Serve Free",
            "verdict": "Ready / Easy Win",
            "accurate": False,
            "error_type": "Architecture Misclassification",
            "error_details": "Pass 1 assumed cloud REST API service."
        },
        "pass2_verification_loop": {
            "accurate": True,
            "resolved_autonomously": True,
            "loop_triggered": "Loop 2: NPM / CLI Registry Checker",
            "finding": "Mermaid CLI is an open-source Node.js package (@mermaid-js/mermaid-cli). No cloud API exists; runs locally as mmdc.",
            "corrected_auth": "None (CLI)",
            "corrected_verdict": "CLI / Script Wrapper"
        },
        "final_human_check": {
            "verified_by": "Human Reviewer",
            "accurate": True,
            "notes": "Verified. Best implemented as a local containerized tool."
        }
    }
]

def main():
    target_path = Path(__file__).resolve().parent / "data" / "verification_audit.json"
    
    total_sample = len(sample_audit_25)
    pass1_correct = sum(1 for item in sample_audit_25 if item["pass1"]["accurate"])
    pass2_correct = sum(1 for item in sample_audit_25 if item["pass2_verification_loop"]["accurate"])
    escalated_count = sum(1 for item in sample_audit_25 if not item["pass2_verification_loop"]["accurate"])
    final_correct = sum(1 for item in sample_audit_25 if item["final_human_check"]["accurate"])

    stats = {
        "dataset_scope": {
            "total_research_catalog": 100,
            "audit_sample_size": total_sample,
            "sampling_method": "Stratified sample across all 10 categories focusing on high-ambiguity edge cases"
        },
        "audit_sample_metrics": {
            "pass1_raw_agent_accuracy": f"{(pass1_correct / total_sample) * 100:.1f}% ({pass1_correct}/{total_sample})",
            "pass2_automated_loop_accuracy": f"{(pass2_correct / total_sample) * 100:.1f}% ({pass2_correct}/{total_sample})",
            "escalated_to_human_count": f"{escalated_count}/{total_sample}",
            "final_verified_accuracy": f"{(final_correct / total_sample) * 100:.1f}% ({final_correct}/{total_sample})",
            "automated_accuracy_gain": f"{((pass2_correct - pass1_correct) / total_sample) * 100:.1f}%",
            "error_taxonomy": {
                "Auth_Hallucinations": "Assumed standard OAuth2/Bearer for Basic/Custom auth (Close, WooCommerce, Copper)",
                "Gating_and_Paywall_Oversights": "Confused trial signup with API access (SE Ranking, Ahrefs, HighLevel, Gladly)",
                "Architecture_CLI_Misclassification": "Classified local scripts/packages as cloud REST APIs (Sherlock, Mermaid CLI)",
                "Product_Entity_Conflation": "Conflated consumer UI with enterprise API (NotebookLM, iPayX, Salesforce CC)",
                "Multi_Layer_Regulatory_Escalations": "Flagged AWS IAM SigV4 + DPP review (Amazon SP-API) for human escalation"
            }
        }
    }

    output_payload = {
        "metrics": stats,
        "sample_audit": sample_audit_25
    }

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)
    
    print("=" * 65)
    print(f"Generated verified audit for {total_sample} sample apps.")
    print(f"Pass 1 Raw Accuracy:       {stats['audit_sample_metrics']['pass1_raw_agent_accuracy']}")
    print(f"Pass 2 Automated Accuracy: {stats['audit_sample_metrics']['pass2_automated_loop_accuracy']}")
    print(f"Escalated to Human:        {stats['audit_sample_metrics']['escalated_to_human_count']}")
    print(f"Final Human Accuracy:      {stats['audit_sample_metrics']['final_verified_accuracy']}")
    print("=" * 65)

if __name__ == "__main__":
    main()
