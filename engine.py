"""
engine.py — AI Recommendation & Scoring Engine for AdPilot AI.

Encapsulates the "intelligence" layer: campaign scoring, winner
detection, recommendation generation, and forecast impact calculations.
"""

import random
import pandas as pd


# ──────────────────────────────────────────────
#  Recommendation Pool
# ──────────────────────────────────────────────

RECOMMENDATION_POOL = [
    {
        "title": "Shift 20% of Meta budget to Google Search",
        "body": (
            "Three Meta ad sets deliver ROAS below 1.6×. Reallocating to "
            "Google Search compounds top-funnel efficiency."
        ),
        "impact": "High",
        "perf": "+0.8× ROAS",
    },
    {
        "title": "Launch lookalike audience for top campaign",
        "body": (
            "Best campaign is at 93% audience saturation. A 1% lookalike "
            "unlocks ~2.3 M new qualified users."
        ),
        "impact": "High",
        "perf": "+2.3 M reach",
    },
    {
        "title": "Switch TikTok to Target CPA at $14",
        "body": (
            "Manual CPC creates off-peak spend waste. Target CPA aligns "
            "bidding with your conversion economics."
        ),
        "impact": "High",
        "perf": "−18% CPA",
    },
    {
        "title": "Apply dayparting to Google Search",
        "body": (
            "68% of purchases happen weekday mornings. +20% bid boost "
            "9 AM–3 PM improves cost-per-conversion."
        ),
        "impact": "Medium",
        "perf": "+1.2% Conv.",
    },
    {
        "title": "Refresh LinkedIn creative with video",
        "body": (
            "LinkedIn CTR is 0.9% vs 1.4% benchmark. Short-form video "
            "from Meta could lift engagement 40–60%."
        ),
        "impact": "Medium",
        "perf": "+0.5% CTR",
    },
    {
        "title": "Activate frequency capping on retargeting",
        "body": (
            "Ad frequency is at 8.4×/user/week. Capping at 5× could "
            "recover 22% CTR drop and reduce CPM."
        ),
        "impact": "Opportunity",
        "perf": "−14% CPM",
    },
]

IMPACT_COLORS = {
    "High":        "#f43f5e",
    "Medium":      "#f59e0b",
    "Opportunity": "#26d9b0",
}

IMPACT_ICONS = {
    "High":        "🔴",
    "Medium":      "🟡",
    "Opportunity": "🟢",
}


# ──────────────────────────────────────────────
#  Recommendation selection
# ──────────────────────────────────────────────

def pick_recommendations(n: int = 3) -> list[dict]:
    """Return *n* random, non-repeating recommendations."""
    pool = list(RECOMMENDATION_POOL)
    random.shuffle(pool)
    return pool[:n]


# ──────────────────────────────────────────────
#  Campaign scoring
# ──────────────────────────────────────────────

def score_campaign(row: pd.Series) -> float:
    """
    Compute a composite campaign score on a 0–100 scale.

    Weights: ROAS 50%, CTR 25%, Conv Rate 25%.
    Normalised against reasonable ceilings (ROAS 10×, CTR 6%, Conv 15%).
    """
    roas_score = min(row["roas"] / 10.0, 1.0) * 50
    ctr_score  = min(row["ctr"]  / 6.0,  1.0) * 25
    conv_score = min(row["conv_rate"] / 15.0, 1.0) * 25
    return round(roas_score + ctr_score + conv_score, 1)


def get_winner(campaigns_df: pd.DataFrame) -> dict:
    """
    Identify the top-performing campaign by ROAS and return a summary dict.

    Keys: name, platform, roas, ctr, conv_rate, spend, impressions,
          above_avg_pct, score.
    """
    if campaigns_df.empty:
        return {}
    best = campaigns_df.loc[campaigns_df["roas"].idxmax()]
    avg_roas = campaigns_df["roas"].mean()
    above_pct = round((best["roas"] - avg_roas) / avg_roas * 100)
    return {
        "name":          best["name"],
        "platform":      best["platform"],
        "roas":          best["roas"],
        "ctr":           best["ctr"],
        "conv_rate":     best["conv_rate"],
        "spend":         best["spend"],
        "impressions":   best["impressions"],
        "above_avg_pct": above_pct,
        "score":         score_campaign(best),
    }


# ──────────────────────────────────────────────
#  Forecast impact
# ──────────────────────────────────────────────

def compute_forecast_impact() -> dict:
    """Return projected gains from applying all recommendations."""
    return {
        "additional_revenue":   18_400,
        "reduced_wasted_spend":  6_200,
        "net_monthly_gain":     24_600,
    }
