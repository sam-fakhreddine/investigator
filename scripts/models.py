#!/usr/bin/env python3
"""
models.py — Pydantic schema for investigation.json.

Single source of truth for the investigation data model.
Used by:
  - json_to_md.py  (validation before rendering)
  - gen_schema.py  (generates templates/investigation_schema.json)

The generated JSON schema is embedded in templates/agent_persona.md so agents
receive the exact schema spec, not a prose description.

Validation layers:
  1. Structural — field types, required fields, extra="forbid" (schema compliance)
  2. Scalar constraints — Annotated types enforce trust boundary rules on individual
     values (no embedded newlines, safe URL schemes, no heading-prefix on concept names)
  3. Cross-field — @model_validator(mode="after") checks citation grounding: sources
     must exist when findings exist; no duplicate URLs; coverage ratio
"""

from datetime import datetime
from typing import Annotated, Literal, Optional, Union
from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    field_validator,
    model_validator,
)



def _no_newlines(v: str) -> str:
    """Reject strings that embed newlines — they break blockquote / table rendering."""
    if "\n" in v or "\r" in v:
        raise ValueError("must not contain newlines (single-line field)")
    return v


def _safe_url(v: str) -> str:
    """Only https:// or http:// schemes are allowed — other schemes are silently
    dropped by the renderer so we reject them at validation time."""
    if not (v.startswith("https://") or v.startswith("http://")):
        raise ValueError(f"URL must start with https:// or http://, got {v!r}")
    return v


def _no_hash_prefix(v: str) -> str:
    """Concept names must not start with '#' — they render as headings in the glossary."""
    if v.startswith("#"):
        raise ValueError("concept name must not start with '#' (renders as heading)")
    return v


def _non_empty(v: str) -> str:
    if not v.strip():
        raise ValueError("must not be empty or whitespace-only")
    return v


def _iso_date(v: str) -> str:
    """Reject date strings that are not YYYY-MM-DD — free-form dates are unprocessable."""
    try:
        datetime.strptime(v, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got {v!r}")
    return v


SingleLineStr = Annotated[str, AfterValidator(_no_newlines), AfterValidator(_non_empty)]
BulletStr = Annotated[str, AfterValidator(_no_newlines), AfterValidator(_non_empty)]
SafeUrlStr = Annotated[str, AfterValidator(_safe_url)]
ConceptNameStr = Annotated[str, AfterValidator(_no_hash_prefix), AfterValidator(_no_newlines), AfterValidator(_non_empty)]



class QuickReference(BaseModel):
    title: str = "Quick Reference"
    columns: list[str]
    rows: list[list[str]]
    notes: Optional[str] = None


SourceTier = Literal["official_doc", "user_guide", "blog", "community"]


class Source(BaseModel):
    title: SingleLineStr
    url: SafeUrlStr
    tier: Optional[SourceTier] = Field(
        default=None,
        description=(
            "Source authority tier. "
            "official_doc = API/SDK/service reference docs; "
            "user_guide = official user guides and tutorials; "
            "blog = vendor or third-party blog posts; "
            "community = Stack Overflow, GitHub issues, forums. "
            "Prefer official_doc > user_guide > blog > community. "
            "Findings backed only by blog or community sources should be hedged."
        ),
    )


class Concept(BaseModel):
    name: ConceptNameStr
    description: str


class EngineeringLeadershipBrief(BaseModel):
    """Engineering leadership brief — outcome-focused, no implementation detail."""
    headline: SingleLineStr = Field(description="One sentence, outcome-focused, no filler.")
    so_what: str = Field(description="Risk, cost, or strategic implication in 1-2 sentences.")
    bullets: list[BulletStr] = Field(
        min_length=1,
        description="3-5 hard-hitting points focused on impact, risk, or decision triggers.",
    )
    action_required: Optional[SingleLineStr] = Field(
        default=None,
        description="A concrete decision or next step, or null.",
    )

    model_config = {"extra": "forbid"}


class PONextSteps(BaseModel):
    po_action: str = Field(
        description="What the PO/EM needs to decide or kick off — specific and actionable."
    )
    work_to_assign: list[BulletStr] = Field(
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
    headline: SingleLineStr = Field(
        description="Plain English, zero jargon. What is this issue in one sentence?"
    )
    so_what: str = Field(
        description="What this means for users or the product in 1-2 sentences. No technical terms."
    )
    bullets: list[BulletStr] = Field(
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
    date: Annotated[str, AfterValidator(_iso_date)]
    status: Literal["Complete", "In Progress", "Superseded"]
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


    @model_validator(mode="after")
    def sources_present_when_findings_exist(self) -> "Investigation":
        """If there are key findings, there must be at least one source.
        An investigation without citations is unverifiable."""
        if self.key_findings and not self.sources:
            raise ValueError(
                "key_findings are present but sources is empty — "
                "every finding must be grounded in at least one cited source"
            )
        return self

    @model_validator(mode="after")
    def no_duplicate_source_urls(self) -> "Investigation":
        """Duplicate source URLs indicate copy-paste errors or hallucinated citations."""
        seen: set[str] = set()
        dupes: list[str] = []
        for src in self.sources:
            url = src.url
            if url in seen:
                dupes.append(url)
            seen.add(url)
        if dupes:
            raise ValueError(
                f"duplicate source URLs detected (each source must be unique): {dupes}"
            )
        return self

    @model_validator(mode="after")
    def citation_coverage_ratio(self) -> "Investigation":
        """Require at least one source per three key findings.
        This catches investigations where an agent generates many findings
        from a single citation or from memory."""
        n_findings = len(self.key_findings)
        n_sources = len(self.sources)
        required = max(1, n_findings // 3)
        if n_findings > 0 and n_sources < required:
            raise ValueError(
                f"citation coverage too low: {n_findings} findings require at least "
                f"{required} sources, but only {n_sources} provided"
            )
        return self
