"""
Spaced Repetition System (SRS) Engine
======================================
Implements a modified SM-2 algorithm with adaptive difficulty,
forgetting curve modeling, and error-driven learning.

Reference: Ebbinghaus forgetting curve + SuperMemo SM-2
"""

from __future__ import annotations
import math
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import IntEnum


class Rating(IntEnum):
    """User response quality rating (0–5 scale, SM-2 standard)."""
    BLACKOUT   = 0  # Complete failure
    WRONG      = 1  # Wrong, but remembered on seeing answer
    HARD       = 2  # Correct with significant difficulty
    GOOD       = 3  # Correct with some hesitation
    EASY       = 4  # Correct with little effort
    PERFECT    = 5  # Perfect recall, instant


@dataclass
class CardState:
    """
    Persistent learning state for a single flashcard.

    Attributes
    ----------
    card_id       : Unique identifier
    ease_factor   : SM-2 ease factor (min 1.3, default 2.5)
    interval_days : Current review interval in days
    repetitions   : Number of successful consecutive reviews
    due_date      : Next review date (ISO format string)
    retention     : Estimated retention [0,1] via forgetting curve
    error_count   : Cumulative wrong answers
    last_rating   : Most recent quality rating
    """
    card_id       : str
    ease_factor   : float = 2.5
    interval_days : float = 1.0
    repetitions   : int   = 0
    due_date      : str   = field(default_factory=lambda: datetime.utcnow().isoformat())
    retention     : float = 1.0
    error_count   : int   = 0
    last_rating   : int   = 3

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "CardState":
        return cls(**d)


class SRSEngine:
    """
    Modified SM-2 spaced repetition engine.

    Enhancements over vanilla SM-2:
    - Forgetting curve estimation (Ebbinghaus model)
    - Adaptive ease factor with error penalty
    - Interleaving score for topic mixing
    - Mastery score per card
    """

    MIN_EASE       = 1.3
    DEFAULT_EASE   = 2.5
    STABILITY_K    = 0.1   # Forgetting curve decay constant

    def update(self, state: CardState, rating: Rating) -> CardState:
        """
        Apply one review cycle and return updated CardState.

        Parameters
        ----------
        state  : Current card state
        rating : User quality rating (0–5)

        Returns
        -------
        Updated CardState with new interval, ease, and due date.
        """
        q = int(rating)

        if q < 3:
            # Failed: reset repetitions, short re-review
            state.repetitions = 0
            state.interval_days = 1.0
            state.error_count += 1
        else:
            # Success: advance interval
            if state.repetitions == 0:
                state.interval_days = 1.0
            elif state.repetitions == 1:
                state.interval_days = 6.0
            else:
                state.interval_days = round(state.interval_days * state.ease_factor, 1)
            state.repetitions += 1

        # Update ease factor (SM-2 formula)
        delta_ease = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        state.ease_factor = max(self.MIN_EASE, state.ease_factor + delta_ease)

        # Compute next due date
        due = datetime.utcnow() + timedelta(days=state.interval_days)
        state.due_date  = due.isoformat()
        state.last_rating = q

        # Estimate retention using Ebbinghaus R = e^(-t/S)
        # where S (stability) grows with repetitions
        stability = max(1.0, state.interval_days / self.STABILITY_K) if q >= 3 else 1.0
        state.retention = round(math.exp(-1.0 / max(stability, 0.001)), 4)

        return state

    def mastery_score(self, state: CardState) -> float:
        """
        Composite mastery score [0, 1].
        Combines retention estimate, repetitions, and error history.
        """
        rep_score  = min(state.repetitions / 10.0, 1.0)
        err_penalty = min(state.error_count * 0.05, 0.5)
        raw = (state.retention * 0.5 + rep_score * 0.5) - err_penalty
        return round(max(0.0, min(1.0, raw)), 3)

    def days_until_due(self, state: CardState) -> float:
        """Return days remaining until card is due (negative = overdue)."""
        due = datetime.fromisoformat(state.due_date)
        delta = due - datetime.utcnow()
        return round(delta.total_seconds() / 86400, 2)

    def is_due(self, state: CardState) -> bool:
        """True if card should be reviewed now."""
        return self.days_until_due(state) <= 0

    def forgetting_curve(self, state: CardState, horizon_days: int = 30) -> list[tuple[float, float]]:
        """
        Project retention over a time horizon.

        Returns
        -------
        List of (day, retention) tuples for plotting.
        """
        stability = max(state.interval_days, 1.0)
        return [
            (t, round(math.exp(-t / stability), 4))
            for t in range(horizon_days + 1)
        ]
