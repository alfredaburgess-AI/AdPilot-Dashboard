"""
data.py — Simulated data layer for AdPilot AI Dashboard.

All campaign, platform, budget, and forecast data lives here so it can
be swapped for real API calls later without touching the UI or engine.
"""

import random
import pandas as pd


# ──────────────────────────────────────────────
#  Campaigns
# ──────────────────────────────────────────────

SEED_CAMPAIGNS = [
    {"id": 1, "name": "Summer Retargeting Pro", "platform": "Google Ads",
     "spend": 18_400, "impressions": "2.8M", "ctr": 4.21, "conv_rate": 11.3,
     "roas": 7.4, "status": "Active"},
    {"id": 2, "name": "Brand Awareness Q1", "platform": "Meta Ads",
     "spend": 14_200, "impressions": "3.1M", "ctr": 3.85, "conv_rate": 9.6,
     "roas": 5.9, "status": "Active"},
    {"id": 3, "name": "Product Launch — Apex", "platform": "Google Ads",
     "spend": 11_800, "impressions": "1.9M", "ctr": 3.44, "conv_rate": 8.8,
     "roas": 5.1, "status": "Active"},
    {"id": 4, "name": "Spring Sale Blitz", "platform": "TikTok",
     "spend": 9_600, "impressions": "2.2M", "ctr": 2.98, "conv_rate": 7.4,
     "roas": 4.3, "status": "Active"},
    {"id": 5, "name": "Lead Gen — Enterprise", "platform": "LinkedIn",
     "spend": 8_100, "impressions": "0.6M", "ctr": 1.14, "conv_rate": 6.1,
     "roas": 3.2, "status": "Active"},
    {"id": 6, "name": "Competitor Conquest", "platform": "Google Ads",
     "spend": 7_400, "impressions": "1.2M", "ctr": 2.61, "conv_rate": 5.8,
     "roas": 2.8, "status": "Active"},
    {"id": 7, "name": "Holiday Remarketing", "platform": "Meta Ads",
     "spend": 6_200, "impressions": "1.4M", "ctr": 1.92, "conv_rate": 4.2,
     "roas": 1.9, "status": "Paused"},
    {"id": 8, "name": "B2B Nurture Sequence", "platform": "LinkedIn",
     "spend": 5_100, "impressions": "0.4M", "ctr": 0.88, "conv_rate": 3.1,
     "roas": 1.4, "status": "Paused"},
]


def get_campaigns() -> pd.DataFrame:
    """Return the seed campaign list as a DataFrame."""
    return pd.DataFrame(SEED_CAMPAIGNS)


# ──────────────────────────────────────────────
#  Platform budgets
# ──────────────────────────────────────────────

PLATFORM_BUDGETS = [
    {"name": "Google Ads",   "spend": 34_600, "color": "#4285F4",
     "change": "+11.2%", "up": True,  "campaigns": 9, "cpa": "$8.20"},
    {"name": "Meta Ads",     "spend": 22_800, "color": "#1877F2",
     "change": "+3.4%",  "up": True,  "campaigns": 7, "cpa": "$11.40"},
    {"name": "TikTok Ads",   "spend": 16_400, "color": "#69C9D0",
     "change": "+14.7%", "up": True,  "campaigns": 5, "cpa": "$9.80"},
    {"name": "LinkedIn Ads", "spend": 10_400, "color": "#0A66C2",
     "change": "−2.1%",  "up": False, "campaigns": 3, "cpa": "$24.60"},
]

PLATFORM_COLORS = {
    "Google Ads": "#4285F4",
    "Meta Ads":   "#1877F2",
    "TikTok":     "#69C9D0",
    "LinkedIn":   "#0A66C2",
}


def get_platform_budgets() -> list[dict]:
    """Return per-platform budget metadata."""
    return [dict(p) for p in PLATFORM_BUDGETS]


# ──────────────────────────────────────────────
#  Data sources
# ──────────────────────────────────────────────

DATA_SOURCES = [
    {"name": "Google Ads API",        "icon": "🔵", "color": "#4285F4",
     "records": "9 campaigns", "sync": "2 min ago"},
    {"name": "Meta Ads API",          "icon": "🟦", "color": "#1877F2",
     "records": "7 campaigns", "sync": "2 min ago"},
    {"name": "LinkedIn Campaign Mgr", "icon": "🟩", "color": "#0A66C2",
     "records": "3 campaigns", "sync": "4 min ago"},
    {"name": "TikTok Ads Manager",    "icon": "⬛", "color": "#69C9D0",
     "records": "5 campaigns", "sync": "2 min ago"},
]


def get_data_sources() -> list[dict]:
    """Return data-source card metadata."""
    return [dict(ds) for ds in DATA_SOURCES]


# ──────────────────────────────────────────────
#  Forecast actions
# ──────────────────────────────────────────────

FORECAST_ACTIONS = [
    {"action": "Increase Google Ads Budget by 15%",
     "icon": "🟢", "metric": "+12% conversions",   "confidence": 92},
    {"action": "Reduce Underperforming Meta Campaigns",
     "icon": "🟢", "metric": "−18% CPA",            "confidence": 87},
    {"action": "Enable Dayparting on Search Campaigns",
     "icon": "🟢", "metric": "+9% ROAS",             "confidence": 84},
    {"action": "Switch TikTok to Target CPA Bidding",
     "icon": "🟡", "metric": "−14% wasted spend",    "confidence": 79},
    {"action": "Launch Lookalike Audiences on Meta",
     "icon": "🟡", "metric": "+22% impressions",     "confidence": 76},
    {"action": "A/B Test Landing Page Headlines",
     "icon": "🟡", "metric": "+7% conv. rate",       "confidence": 68},
]


def get_forecast_actions() -> list[dict]:
    """Return forecast / optimization action rows."""
    return [dict(f) for f in FORECAST_ACTIONS]


# ──────────────────────────────────────────────
#  12-week trend data
# ──────────────────────────────────────────────

TREND_WEEKS = [f"W{i}" for i in range(1, 13)]
TREND_ROAS  = [3.8, 4.0, 3.9, 4.2, 4.1, 4.5, 4.3, 4.6, 4.5, 4.7, 4.8, 4.82]
TREND_CTR   = [2.8, 3.0, 2.9, 3.1, 3.2, 3.4, 3.3, 3.5, 3.5, 3.6, 3.6, 3.67]
TREND_CONV  = [7.2, 7.8, 7.5, 8.1, 7.9, 8.4, 8.2, 8.5, 8.3, 8.1, 8.2, 8.14]


def get_trend_data() -> dict:
    """Return 12-week trend series as a dict of lists."""
    return {
        "weeks": list(TREND_WEEKS),
        "roas":  list(TREND_ROAS),
        "ctr":   list(TREND_CTR),
        "conv":  list(TREND_CONV),
    }


# ──────────────────────────────────────────────
#  Sparkline helper
# ──────────────────────────────────────────────

def generate_sparkline(base: float, noise: float, count: int = 16) -> list[float]:
    """Generate a gentle upward-trending sparkline array with random noise."""
    return [
        round(base + (i / count) * noise * 0.5 + (random.random() - 0.5) * noise, 2)
        for i in range(count)
    ]
