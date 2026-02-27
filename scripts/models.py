#!/usr/bin/env python3
"""
models.py — Pydantic schema for investigation.json.

Single source of truth for the investigation data model.
Used by:
  - json_to_md.py  (validation before rendering)
  - gen_schema.py  (generates templates/investigation_schema.json)

The generated JSON schema is embedded in templates/agent_persona.md so agents
receive the exact schema spec, not a prose description.
"""

from typing import Optional, Union
from pydantic import BaseModel, Field, field_validator


class QuickReference(BaseModel):
    title: str = "Quick Reference"
    columns: list[str]
    rows: list[list[str]]
    notes: Optional[str] = None


class Source(BaseModel):
    title: str
    url: str


class Concept(BaseModel):
    name: str
    description: str


class EngineeringLeadershipBrief(BaseModel):
    """Engineering leadership brief — outcome-focused, no implementation detail."""
    headline: str = Field(description="One sentence, outcome-focused, no filler.")
    so_what: str = Field(description="Risk, cost, or strategic implication in 1-2 sentences.")
    bullets: list[str] = Field(
        min_length=1,
        description="3-5 hard-hitting points focused on impact, risk, or decision triggers.",
    )
    action_required: Optional[str] = Field(
        default=None,
        description="A concrete decision or next step, or null.",
    )

    model_config = {"extra": "forbid"}


class PONextSteps(BaseModel):
    po_action: str = Field(
        description="What the PO/EM needs to decide or kick off — specific and actionable."
    )
    work_to_assign: list[str] = Field(
        min_length=1,
        description="Discrete work items the PO/EM will hand to engineers. Must be a list.",
    )
    leadership_input: Optional[str] = Field(
        default=None,
        description="What architects or senior ICs need to weigh in on, or null.",
    )

    model_config = {"extra": "forbid"}


class ProductOwnerBrief(BaseModel):
    """Product owner brief — plain English, zero jargon, actionable next steps."""
    headline: str = Field(
        description="Plain English, zero jargon. What is this issue in one sentence?"
    )
    so_what: str = Field(
        description="What this means for users or the product in 1-2 sentences. No technical terms."
    )
    bullets: list[str] = Field(
        min_length=1,
        description="3-5 bullets a non-engineer can understand and act on.",
    )
    risk_level: str = Field(
        description="One of: Low, Medium, High, Critical. Use the highest level warranted."
    )
    next_steps: PONextSteps
    questions_to_ask_engineering: list[str] = Field(
        default_factory=list,
        description="1-3 questions the PO can bring into an engineering conversation.",
    )

    model_config = {"extra": "forbid"}

    @field_validator("risk_level")
    @classmethod
    def valid_risk(cls, v: str) -> str:
        allowed = {"Low", "Medium", "High", "Critical"}
        if v not in allowed:
            raise ValueError(f"must be one of {sorted(allowed)}, got {v!r}")
        return v


class AudienceBriefs(BaseModel):
    engineering_leadership: Optional[EngineeringLeadershipBrief] = None
    product_owner: Optional[ProductOwnerBrief] = None

    model_config = {"extra": "forbid"}


class Investigation(BaseModel):
    topic: str
    date: str
    status: str
    question: str
    context: str
    quick_reference: Optional[QuickReference] = None
    key_findings: list[Union[str, dict]] = Field(default_factory=list)
    concepts: list[Concept] = Field(default_factory=list)
    tensions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    audience_briefs: Optional[AudienceBriefs] = None

    model_config = {"extra": "allow"}
