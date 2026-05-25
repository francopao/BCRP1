"""
Persistence Layer
=================
JSON-backed storage with a clean interface ready to swap to SQLite/Postgres.
All I/O goes through CardStore — never access files directly from UI code.

Streamlit Cloud note: the app directory is read-only, so we write to /tmp
which is always writable. Data resets on container restart (this is expected
for a cloud study app — SRS state is per-session unless you add a DB).
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Optional
from datetime import datetime

from core.card_model import Flashcard
from core.srs_engine import CardState, SRSEngine


# /tmp is always writable on Streamlit Cloud and local
_TMP = Path("/tmp/quant_memoria")
CARDS_FILE     = _TMP / "library.json"
STATES_FILE    = _TMP / "states.json"
ANALYTICS_FILE = _TMP / "analytics.json"


def _ensure_dirs():
    _TMP.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path) -> dict | list:
    if path.exists():
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def _save_json(path: Path, data: dict | list):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


class CardStore:
    """
    Unified data access object for cards, SRS states, and analytics.

    Usage
    -----
    store = CardStore()
    store.save_card(card)
    cards = store.all_cards()
    """

    def __init__(self):
        _ensure_dirs()
        self.engine = SRSEngine()

    # ── Cards ──────────────────────────────────

    def all_cards(self) -> list[Flashcard]:
        raw = _load_json(CARDS_FILE)
        return [Flashcard.from_dict(d) for d in raw.values()]

    def get_card(self, card_id: str) -> Optional[Flashcard]:
        raw = _load_json(CARDS_FILE)
        if card_id in raw:
            return Flashcard.from_dict(raw[card_id])
        return None

    def save_card(self, card: Flashcard):
        raw = _load_json(CARDS_FILE)
        raw[card.id] = card.to_dict()
        _save_json(CARDS_FILE, raw)

    def delete_card(self, card_id: str):
        raw = _load_json(CARDS_FILE)
        raw.pop(card_id, None)
        _save_json(CARDS_FILE, raw)

    def cards_by_domain(self, domain: str) -> list[Flashcard]:
        return [c for c in self.all_cards() if c.domain == domain]

    def cards_by_topic(self, topic: str) -> list[Flashcard]:
        return [c for c in self.all_cards() if c.topic == topic]

    # ── SRS States ─────────────────────────────

    def all_states(self) -> dict[str, CardState]:
        raw = _load_json(STATES_FILE)
        return {k: CardState.from_dict(v) for k, v in raw.items()}

    def get_state(self, card_id: str) -> CardState:
        raw = _load_json(STATES_FILE)
        if card_id in raw:
            return CardState.from_dict(raw[card_id])
        return CardState(card_id=card_id)

    def save_state(self, state: CardState):
        raw = _load_json(STATES_FILE)
        raw[state.card_id] = state.to_dict()
        _save_json(STATES_FILE, raw)

    def due_cards(self) -> list[Flashcard]:
        """Return all cards due for review today."""
        cards  = self.all_cards()
        states = self.all_states()
        due = []
        for card in cards:
            state = states.get(card.id, CardState(card_id=card.id))
            if self.engine.is_due(state):
                due.append(card)
        return due

    # ── Analytics ──────────────────────────────

    def log_review(self, card_id: str, rating: int, domain: str, topic: str):
        raw = _load_json(ANALYTICS_FILE)
        if "reviews" not in raw:
            raw["reviews"] = []
        raw["reviews"].append({
            "card_id"   : card_id,
            "rating"    : rating,
            "domain"    : domain,
            "topic"     : topic,
            "timestamp" : datetime.utcnow().isoformat(),
        })
        _save_json(ANALYTICS_FILE, raw)

    def get_analytics(self) -> dict:
        return _load_json(ANALYTICS_FILE)

    def mastery_by_topic(self) -> dict[str, float]:
        """Return mean mastery score per topic."""
        cards  = self.all_cards()
        states = self.all_states()
        topic_scores: dict[str, list[float]] = {}
        for card in cards:
            state = states.get(card.id, CardState(card_id=card.id))
            score = self.engine.mastery_score(state)
            topic_scores.setdefault(card.topic, []).append(score)
        return {t: round(sum(s)/len(s), 3) for t, s in topic_scores.items()}

    def streak_days(self) -> int:
        """Compute current study streak in days."""
        raw = self.get_analytics()
        reviews = raw.get("reviews", [])
        if not reviews:
            return 0
        dates = sorted({r["timestamp"][:10] for r in reviews}, reverse=True)
        streak = 1
        for i in range(1, len(dates)):
            d1 = datetime.fromisoformat(dates[i-1])
            d2 = datetime.fromisoformat(dates[i])
            if (d1 - d2).days == 1:
                streak += 1
            else:
                break
        return streak
