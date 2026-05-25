"""
Flashcard Data Model & Financial Topic Taxonomy
================================================
Defines the full card schema and topic hierarchy for the
quantitative finance learning system.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
import uuid


# ──────────────────────────────────────────────
# Topic Taxonomy
# ──────────────────────────────────────────────

class Domain(str, Enum):
    FINANCIAL_ENGINEERING   = "Financial Engineering"
    PORTFOLIO_MANAGEMENT    = "Portfolio Management"
    INTEREST_RATE_MODELS    = "Interest Rate Models"
    FINANCIAL_ECONOMETRICS  = "Financial Econometrics"
    FINANCIAL_STABILITY     = "Financial Stability"


TOPIC_TREE: dict[str, list[str]] = {
    Domain.FINANCIAL_ENGINEERING: [
        "Black-Scholes Model",
        "Greeks & Sensitivities",
        "PDEs in Finance",
        "Martingales & Risk-Neutral Pricing",
        "Stochastic Calculus & Itô's Lemma",
        "Monte Carlo Methods",
        "Exotic Options",
        "Derivatives Pricing",
    ],
    Domain.PORTFOLIO_MANAGEMENT: [
        "Mean-Variance Optimization",
        "Capital Asset Pricing Model",
        "Factor Models",
        "Strategic Asset Allocation",
        "Risk Measures (VaR, CVaR)",
        "Portfolio Performance Attribution",
        "Robust Optimization",
        "Quantitative Trading Strategies",
    ],
    Domain.INTEREST_RATE_MODELS: [
        "Vasicek Model",
        "Cox-Ingersoll-Ross (CIR)",
        "Hull-White Model",
        "HJM Framework",
        "Yield Curve Construction",
        "Fixed Income Derivatives",
        "Swap Pricing",
        "Bond Mathematics",
    ],
    Domain.FINANCIAL_ECONOMETRICS: [
        "ARCH & GARCH Models",
        "Time Series Analysis (ARMA/ARIMA)",
        "Cointegration & Error Correction",
        "Volatility Modeling",
        "High-Frequency Data",
        "Panel Data Methods",
        "Structural Break Tests",
        "Causality & VAR Models",
    ],
    Domain.FINANCIAL_STABILITY: [
        "Macroprudential Policy",
        "Systemic Risk Measures",
        "Network Contagion Models",
        "Basel III/IV Framework",
        "Stress Testing Methodologies",
        "SIFI Identification",
        "Liquidity Risk",
        "Central Bank Toolkits",
    ],
}


# ──────────────────────────────────────────────
# Card Types
# ──────────────────────────────────────────────

class CardType(str, Enum):
    CONCEPT      = "Concept"          # Definitional / intuitive
    FORMULA      = "Formula"          # Mathematical expression
    DERIVATION   = "Derivation"       # Step-by-step math proof
    CODING       = "Coding"           # Python/MATLAB snippet
    ASSUMPTION   = "Assumption"       # Model assumptions & limits
    APPLICATION  = "Application"      # Real-world use case
    INTERVIEW    = "Interview"        # Quant interview style
    CENTRAL_BANK = "Central Bank"     # Policy / reasoning style


class DifficultyLevel(str, Enum):
    FOUNDATIONAL = "Foundational"
    INTERMEDIATE = "Intermediate"
    ADVANCED     = "Advanced"
    EXPERT       = "Expert"


# ──────────────────────────────────────────────
# Card Schema
# ──────────────────────────────────────────────

@dataclass
class Flashcard:
    """
    Core flashcard entity.

    Fields
    ------
    id           : UUID
    domain       : Top-level domain (e.g. Financial Engineering)
    topic        : Specific topic within domain
    card_type    : Pedagogical type
    difficulty   : Difficulty level
    front        : Question / prompt (supports LaTeX via $...$)
    back         : Answer / explanation
    latex_formula: Optional standalone LaTeX formula string
    intuition    : Economic/financial intuition paragraph
    derivation   : Step-by-step mathematical derivation
    code_snippet : Python code example
    assumptions  : Key model assumptions
    limitations  : Known limitations / critiques
    connections  : Related card IDs or topic names
    tags         : Free-form tags for search
    source       : Reference (book, paper, lecture)
    created_at   : ISO timestamp
    """
    id            : str = field(default_factory=lambda: str(uuid.uuid4()))
    domain        : str = Domain.FINANCIAL_ENGINEERING
    topic         : str = "Black-Scholes Model"
    card_type     : str = CardType.CONCEPT
    difficulty    : str = DifficultyLevel.INTERMEDIATE
    front         : str = ""
    back          : str = ""
    latex_formula : str = ""
    intuition     : str = ""
    derivation    : str = ""
    code_snippet  : str = ""
    assumptions   : str = ""
    limitations   : str = ""
    connections   : list[str] = field(default_factory=list)
    tags          : list[str] = field(default_factory=list)
    source        : str = ""
    created_at    : str = field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Flashcard":
        return cls(**d)
