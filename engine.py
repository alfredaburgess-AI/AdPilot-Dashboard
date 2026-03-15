"""
engine.py — AI Recommendation & Scoring Engine for AdPilot AI.

Analyses real campaign data (ROAS, CTR) to generate actionable
recommendations and projects dynamic forecast impact.
"""

import pandas as pd


# ──────────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────────

ROAS_LOW_THRESHOLD = 2.0   # below this → recommend budget reduction
ROAS_HIGH_THRESHOLD = 4.0  # above this → recommend budget increase
CTR_LOW_THRESHOLD = 1.5    # below this → recommend creative refresh
BUDGET_INCREASE_PCT = 0.15  # 15% increase for high performers
BUDGET_REDUCE_PCT = 0.30    # 30% reduction for underperformers
EXPECTED_ROAS_LIFT = 0.20   # 20% ROAS uplift from increased budget
WASTED_SPEND_RECOVERY = 0.50  # recover 50% of reduced budget as savings

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
#  Data-driven Recommendations
# ──────────────────────────────────────────────

def analyze_campaigns(campaigns_df: pd.DataFrame) -> list[dict]:
    """
    Analyse every campaign's ROAS and CTR to produce targeted recommendations.

    Rules
    ─────
    • ROAS < 2.0  →  "Reduce Budget" (High priority)
    • ROAS > 4.0  →  "Increase Budget by 15%" (Opportunity)
    • CTR  < 1.5% →  "Refresh Creative" (Medium priority)

    Returns a list of recommendation dicts, one per triggered rule.
    Returns an empty list if the DataFrame is empty or missing required columns.
    """
    if campaigns_df.empty:
        return []

    required = {"roas", "ctr", "spend", "name", "platform"}
    if not required.issubset(campaigns_df.columns):
        return []

    recs: list[dict] = []
    avg_roas = campaigns_df["roas"].mean()

    for _, row in campaigns_df.iterrows():
        name = row["name"]
        platform = row["platform"]
        roas = row["roas"]
        ctr = row["ctr"]
        spend = row["spend"]

        # ── Low ROAS → cut budget ──
        if roas < ROAS_LOW_THRESHOLD:
            savings = spend * BUDGET_REDUCE_PCT
            recs.append({
                "title": f"Reduce Budget for '{name}'",
                "body": (
                    f"ROAS is {roas}× (below {ROAS_LOW_THRESHOLD}× threshold). "
                    f"Cutting spend by {int(BUDGET_REDUCE_PCT*100)}% on {platform} "
                    f"saves ~${savings:,.0f}/mo and redirects budget to "
                    f"higher-performing campaigns."
                ),
                "impact": "High",
                "perf": f"−${savings:,.0f} wasted spend",
                "campaign": name,
                "action": "reduce",
                "spend_delta": -savings,
                "roas": roas,
            })

        # ── High ROAS → increase budget ──
        elif roas > ROAS_HIGH_THRESHOLD:
            extra_spend = spend * BUDGET_INCREASE_PCT
            projected_revenue = extra_spend * roas * EXPECTED_ROAS_LIFT
            recs.append({
                "title": f"Increase Budget by 15% for '{name}'",
                "body": (
                    f"ROAS is {roas}× (above {ROAS_HIGH_THRESHOLD}× threshold). "
                    f"Adding ${extra_spend:,.0f}/mo on {platform} could generate "
                    f"~${projected_revenue:,.0f} in additional revenue."
                ),
                "impact": "Opportunity",
                "perf": f"+${projected_revenue:,.0f} revenue",
                "campaign": name,
                "action": "increase",
                "spend_delta": extra_spend,
                "revenue_delta": projected_revenue,
                "roas": roas,
            })

        # ── Low CTR → creative refresh ──
        if ctr < CTR_LOW_THRESHOLD:
            recs.append({
                "title": f"Refresh Creative for '{name}'",
                "body": (
                    f"CTR is {ctr}% (below {CTR_LOW_THRESHOLD}% benchmark). "
                    f"Testing new headlines or video on {platform} typically "
                    f"lifts CTR by 40–60%, improving conversion efficiency."
                ),
                "impact": "Medium",
                "perf": f"+{ctr * 0.5:.1f}% CTR uplift",
                "campaign": name,
                "action": "refresh_creative",
                "roas": roas,
            })

    # Sort: High first, then Medium, then Opportunity
    priority = {"High": 0, "Medium": 1, "Opportunity": 2}
    recs.sort(key=lambda r: (priority.get(r["impact"], 9), -r.get("roas", 0)))

    return recs


# ──────────────────────────────────────────────
#  Campaign scoring
# ──────────────────────────────────────────────

def score_campaign(row: pd.Series) -> float:
    """
    Compute a composite campaign score on a 0–100 scale.

    Weights: ROAS 50%, CTR 25%, Conv Rate 25%.
    Normalised against reasonable ceilings (ROAS 10×, CTR 6%, Conv 15%).
    Negative / missing values are clamped to 0.
    """
    roas_val = max(float(row.get("roas", 0)), 0)
    ctr_val  = max(float(row.get("ctr", 0)), 0)
    conv_val = max(float(row.get("conv_rate", 0)), 0)

    roas_score = min(roas_val / 10.0, 1.0) * 50
    ctr_score  = min(ctr_val  / 6.0,  1.0) * 25
    conv_score = min(conv_val / 15.0, 1.0) * 25
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
    if avg_roas == 0:
        above_pct = 0
    else:
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
#  Dynamic Forecast Impact
# ──────────────────────────────────────────────

def compute_forecast_impact(recommendations: list[dict]) -> dict:
    """
    Calculate projected impact from the generated recommendations.

    • additional_revenue:   sum of revenue_delta from "increase" actions
    • reduced_wasted_spend: sum of |spend_delta| from "reduce" actions
    • net_monthly_gain:     total of both
    """
    additional_revenue = 0.0
    reduced_wasted_spend = 0.0

    for rec in recommendations:
        action = rec.get("action", "")
        if action == "increase":
            additional_revenue += rec.get("revenue_delta", 0)
        elif action == "reduce":
            reduced_wasted_spend += abs(rec.get("spend_delta", 0))

    # Apply wasted-spend recovery factor
    recovered = reduced_wasted_spend * WASTED_SPEND_RECOVERY
    net_gain = additional_revenue + recovered

    return {
        "additional_revenue":   round(additional_revenue),
        "reduced_wasted_spend": round(reduced_wasted_spend),
        "net_monthly_gain":     round(net_gain),
    }
