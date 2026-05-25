"""
Analytics Engine
================
Computes learning metrics: forgetting curves, mastery heatmaps,
retention scores, study consistency, and weak topic identification.
"""

from __future__ import annotations
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Any

from core.store import CardStore
from core.srs_engine import SRSEngine, CardState


class AnalyticsEngine:
    """Derives learning insights from raw review history and card states."""

    def __init__(self):
        self.store  = CardStore()
        self.engine = SRSEngine()

    # ── Summary Stats ─────────────────────────────────────────────────

    def summary(self) -> dict[str, Any]:
        """High-level dashboard stats."""
        cards   = self.store.all_cards()
        states  = self.store.all_states()
        due     = self.store.due_cards()
        reviews = self.store.get_analytics().get("reviews", [])

        mastery_scores = []
        for card in cards:
            state = states.get(card.id, CardState(card_id=card.id))
            mastery_scores.append(self.engine.mastery_score(state))

        mean_mastery = round(sum(mastery_scores) / max(len(mastery_scores), 1), 3)

        total_reviews  = len(reviews)
        correct_reviews = sum(1 for r in reviews if r["rating"] >= 3)
        accuracy = round(correct_reviews / max(total_reviews, 1), 3)

        return {
            "total_cards"   : len(cards),
            "due_today"     : len(due),
            "mean_mastery"  : mean_mastery,
            "total_reviews" : total_reviews,
            "accuracy"      : accuracy,
            "streak_days"   : self.store.streak_days(),
        }

    # ── Topic Heatmap ─────────────────────────────────────────────────

    def topic_mastery_heatmap(self) -> list[dict]:
        """Return mastery by (domain, topic) for heatmap rendering."""
        cards  = self.store.all_cards()
        states = self.store.all_states()
        bucket: dict[tuple, list[float]] = defaultdict(list)

        for card in cards:
            state = states.get(card.id, CardState(card_id=card.id))
            score = self.engine.mastery_score(state)
            bucket[(card.domain, card.topic)].append(score)

        return [
            {
                "domain" : domain,
                "topic"  : topic,
                "mastery": round(sum(scores) / len(scores), 3),
                "count"  : len(scores),
            }
            for (domain, topic), scores in bucket.items()
        ]

    # ── Weak Topics ───────────────────────────────────────────────────

    def weak_topics(self, n: int = 5) -> list[dict]:
        """Return top-N topics with lowest mastery scores."""
        heatmap = self.topic_mastery_heatmap()
        return sorted(heatmap, key=lambda x: x["mastery"])[:n]

    def strong_topics(self, n: int = 5) -> list[dict]:
        """Return top-N topics with highest mastery scores."""
        heatmap = self.topic_mastery_heatmap()
        return sorted(heatmap, key=lambda x: x["mastery"], reverse=True)[:n]

    # ── Review Timeline ───────────────────────────────────────────────

    def reviews_per_day(self, days: int = 30) -> list[dict]:
        """Return review counts by day for the past N days."""
        reviews = self.store.get_analytics().get("reviews", [])
        today   = datetime.utcnow().date()
        counts: dict[str, int] = {}

        for i in range(days):
            d = (today - timedelta(days=i)).isoformat()
            counts[d] = 0

        for r in reviews:
            day = r["timestamp"][:10]
            if day in counts:
                counts[day] += 1

        return [{"date": k, "count": v} for k, v in sorted(counts.items())]

    # ── Accuracy by Domain ────────────────────────────────────────────

    def accuracy_by_domain(self) -> dict[str, float]:
        """Return review accuracy (rating≥3) per domain."""
        reviews = self.store.get_analytics().get("reviews", [])
        domain_stats: dict[str, list[int]] = defaultdict(list)
        for r in reviews:
            domain_stats[r.get("domain", "Unknown")].append(int(r["rating"] >= 3))
        return {
            d: round(sum(s) / max(len(s), 1), 3)
            for d, s in domain_stats.items()
        }

    # ── Forgetting Curve Projection ───────────────────────────────────

    def projected_forgetting_curves(self, card_ids: list[str] | None = None) -> list[dict]:
        """
        Return forgetting curve data for cards.
        If card_ids is None, uses all due or recently reviewed cards.
        """
        states  = self.store.all_states()
        cards   = self.store.all_cards()
        if card_ids:
            card_map = {c.id: c for c in cards}
            targets  = [card_map[cid] for cid in card_ids if cid in card_map]
        else:
            targets = cards[:10]  # Sample for display

        curves = []
        for card in targets:
            state = states.get(card.id, CardState(card_id=card.id))
            curve = self.engine.forgetting_curve(state, horizon_days=30)
            curves.append({
                "card_id" : card.id,
                "topic"   : card.topic,
                "front"   : card.front[:60],
                "curve"   : curve,
            })
        return curves
