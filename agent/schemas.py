# agent/schemas.py
# Pydantic schemas defining the rigorous research data structure for Composio

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, HttpUrl

class ApiSurface(BaseModel):
    protocols: List[str] = Field(description="Protocols used: REST, GraphQL, gRPC, Webhooks, CLI")
    breadth: str = Field(description="Breadth of API surface: High, Medium, Low, Local CLI")
    mcp_status: str = Field(description="Status in MCP ecosystem: Official, Community, Native, Local, None")
    spec_available: bool = Field(description="Whether public OpenAPI / Swagger / GraphQL schema is documented")

class Buildability(BaseModel):
    verdict: Literal[
        "Ready / Easy Win",
        "Gated / High Friction",
        "Blocked / Outreach Needed",
        "CLI / Script Wrapper"
    ] = Field(description="Feasibility verdict for agent toolkit development")
    blocker: str = Field(description="Primary blocker or friction point, or 'None'")

class Evidence(BaseModel):
    docs_url: str = Field(description="Primary documentation or developer portal URL")
    verification_notes: str = Field(description="Detailed verification trail and evidence")

class AppResearchResult(BaseModel):
    id: int = Field(description="Sequential ID from 1 to 100")
    name: str = Field(description="Name of the application")
    category: str = Field(description="One of the 10 target categories")
    website: str = Field(description="Main application website")
    description: str = Field(description="One-line functional description")
    auth_methods: List[str] = Field(description="Exhaustive list of supported auth methods")
    auth_primary: str = Field(description="Primary authentication pattern (OAuth2, API Key, Basic, etc.)")
    access_model: str = Field(description="Self-serve free/trial vs gated paid/admin/sales")
    is_self_serve: bool = Field(description="True if developer can get credentials without human/sales approval")
    api_surface: ApiSurface
    buildability: Buildability
    evidence: Evidence
    confidence_score: float = Field(default=1.0, description="Verification confidence score (0.0 to 1.0)")
    needs_human_review: bool = Field(default=False, description="Whether flagged for human-in-the-loop escalation")
