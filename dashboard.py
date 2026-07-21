import streamlit as st
import mysql.connector
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

import subprocess
import threading

def refresh_data_in_background():
    """Runs scraper + news fetcher silently when dashboard loads"""
    subprocess.run(["python", "scraper.py"], capture_output=True)
    subprocess.run(["python", "news_fetcher.py"], capture_output=True)

# Only refresh once per hour, not on every page interaction
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()
    thread = threading.Thread(target=refresh_data_in_background)
    thread.daemon = True
    thread.start()
elif (datetime.now() - st.session_state.last_refresh).seconds > 3600:
    st.session_state.last_refresh = datetime.now()
    thread = threading.Thread(target=refresh_data_in_background)
    thread.daemon = True
    thread.start()
# ── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="AI Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── DESIGN SYSTEM ────────────────────────────────────────────
# Tokens: paper background, near-black ink, a single navy identity
# color, and two semantic colors (green/red) for sentiment only.
# Type: Fraunces (editorial serif, used sparingly for the signature
# moment) + Inter (data/UI, tabular numerals) + IBM Plex Mono
# (ticker-style micro labels).
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,380;9..144,480;9..144,560&family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --paper:      #FAFAF9;
  --surface:    #FFFFFF;
  --ink-900:    #121214;
  --ink-700:    #45454B;
  --ink-500:    #78787F;
  --ink-300:    #C6C6CB;
  --line:       #E7E7E9;
  --line-strong:#D6D6D9;
  --navy:       #16233F;
  --brass:      #9C6B1F;
  --green:      #1E7145;
  --red:        #A13434;
}

html, body, [class*="css"], .stApp{
  background: var(--paper) !important;
  color: var(--ink-900) !important;
  font-family: 'Inter', -apple-system, sans-serif !important;
}
#MainMenu, footer, header{ visibility: hidden; }
section[data-testid="stSidebar"]{ display:none; }
.block-container{
  padding: 40px 56px 64px !important;
  max-width: 1240px !important;
}
div[data-testid="stVerticalBlock"] > div{ margin-bottom:0 !important; }
div[data-testid="stDataFrame"]{ display:none !important; }
.stMarkdown p{ margin:0; }

::selection{ background: rgba(22,35,63,0.12); }
a:focus-visible, button:focus-visible{ outline: 2px solid var(--navy); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce){ .ec-live-dot{ animation:none !important; } }

/* ── MASTHEAD ─────────────────────────────────────────── */
.ec-eyebrow{
  font-family:'IBM Plex Mono', monospace;
  font-size:11px; font-weight:500;
  letter-spacing: 0.14em; text-transform: uppercase;
  color: var(--ink-500);
}
.ec-masthead{
  display:flex; align-items:flex-end; justify-content:space-between;
  padding-bottom:20px; margin-bottom:20px;
  border-bottom: 1px solid var(--ink-900);
}
.ec-wordmark{
  font-family:'Fraunces', serif;
  font-optical-sizing:auto;
  font-weight:480; font-size:42px; letter-spacing:-0.01em;
  line-height:1; color: var(--ink-900); margin-top:6px;
}
.ec-masthead-right{ text-align:right; display:flex; flex-direction:column; align-items:flex-end; gap:6px; }
.ec-live{
  display:inline-flex; align-items:center; gap:7px;
  font-family:'IBM Plex Mono', monospace; font-size:11px; font-weight:500;
  letter-spacing:0.1em; text-transform:uppercase; color: var(--ink-700);
}
.ec-live-dot{
  width:6px; height:6px; border-radius:50%; background: var(--green);
  animation: ec-pulse 2.4s ease-in-out infinite;
}
@keyframes ec-pulse{ 0%,100%{opacity:1;} 50%{opacity:0.35;} }
.ec-timestamp{ font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-500); }

/* ── EXECUTIVE SUMMARY ────────────────────────────────── */
.ec-summary{
  font-family:'Inter', sans-serif;
  font-size:19px; line-height:1.55; font-weight:400;
  color: var(--ink-700);
  max-width: 860px;
  margin: 0 0 40px 0;
}
.ec-summary b{ color: var(--ink-900); font-weight:600; }

/* ── KPI STRIP ────────────────────────────────────────── */
.ec-kpi-strip{
  display:grid; grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid var(--line-strong);
  border-bottom: 1px solid var(--line-strong);
  margin-bottom: 56px;
}
.ec-tile{
  padding: 20px 24px 22px; border-left: 1px solid var(--line);
  border-top: 2px solid transparent; margin-top:-2px;
}
.ec-tile:first-child{ border-left:none; padding-left:0; }
.ec-tile:last-child{ padding-right:0; }
.ec-tile.c-navy{ border-top-color: var(--navy); }
.ec-tile.c-brass{ border-top-color: var(--brass); }
.ec-tile.c-green{ border-top-color: var(--green); }
.ec-tile.c-red{ border-top-color: var(--red); }
.ec-tile-eyebrow{
  font-family:'IBM Plex Mono', monospace; font-size:10.5px; font-weight:500;
  letter-spacing:0.1em; text-transform:uppercase; color: var(--ink-500);
  margin-bottom: 10px;
}
.ec-tile-value{
  font-family:'Inter', sans-serif; font-weight:800; font-size:38px;
  letter-spacing:-0.02em; color: var(--ink-900); font-variant-numeric: tabular-nums;
  line-height:1; margin-bottom: 14px;
}
.ec-tile-foot{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
.ec-segbar{ display:flex; width:56px; height:5px; border-radius:2px; overflow:hidden; background: var(--line); flex-shrink:0; }
.ec-segbar span{ height:100%; }
.ec-spark{ flex-shrink:0; }
.ec-tile-delta{
  font-size:12px; font-weight:500; color: var(--ink-500);
  text-align:right; line-height:1.35;
}
.ec-tile-delta.up{ color: var(--green); }
.ec-tile-delta.down{ color: var(--red); }

/* ── SECTION HEADERS ──────────────────────────────────── */
.ec-section{ margin-bottom:16px; }
.ec-section-title{
  font-family:'Inter', sans-serif; font-weight:700; font-size:15px;
  color: var(--ink-900); letter-spacing:-0.01em;
  display:flex; align-items:center; gap:8px;
}
.ec-section-title::before{
  content:''; width:7px; height:7px; border-radius:50%;
  background: var(--navy); display:inline-block;
}
.ec-section-title.brass::before{ background: var(--brass); }
.ec-section-sub{
  font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-500);
  margin-top:3px;
}

/* ── EXECUTIVE INSIGHT (signature moment) ─────────────── */
.ec-insight{
  display:grid; grid-template-columns: 1.5fr 1fr; gap:64px;
  align-items:center;
  padding: 44px 56px 52px 56px;
  margin: 0 -56px 56px -56px;
  border-bottom: 1px solid var(--line-strong);
  background: linear-gradient(180deg, rgba(30,113,69,0.035) 0%, rgba(22,35,63,0.03) 100%);
}
.ec-insight-stat{
  font-family:'Fraunces', serif; font-optical-sizing:auto;
  font-weight:480; font-size:118px; line-height:0.92; letter-spacing:-0.03em;
  color: var(--navy); margin: 14px 0 20px 0;
}
.ec-insight-stat sup{
  font-size:44px; top:-0.5em; font-weight:400; color: var(--ink-500);
}
.ec-insight-text{
  font-family:'Inter', sans-serif; font-size:16px; line-height:1.6;
  color: var(--ink-700); max-width: 480px;
}
.ec-insight-right{ display:flex; flex-direction:column; align-items:center; gap:22px; }
.ec-ring{
  width:190px; height:190px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
}
.ec-ring-hole{
  width:136px; height:136px; border-radius:50%; background: var(--paper);
  display:flex; flex-direction:column; align-items:center; justify-content:center;
}
.ec-ring-hole span{ font-family:'Inter'; font-weight:800; font-size:26px; color: var(--ink-900); font-variant-numeric: tabular-nums; }
.ec-ring-hole small{ font-family:'IBM Plex Mono', monospace; font-size:10px; color: var(--ink-500); text-transform:uppercase; letter-spacing:0.08em; margin-top:2px; }
.ec-ring-legend{ display:flex; gap:20px; }
.ec-ring-legend div{ display:flex; align-items:center; gap:7px; font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-700); }
.ec-ring-legend i{ width:7px; height:7px; border-radius:50%; display:inline-block; }

/* ── CHART LEGEND (integrated, not Plotly default) ────── */
.ec-chart-legend{ display:flex; gap:22px; flex-wrap:wrap; margin-bottom:6px; }
.ec-chart-legend div{ display:flex; align-items:center; gap:7px; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.03em; color: var(--ink-700); }
.ec-chart-legend i{ width:9px; height:2px; display:inline-block; border-radius:1px; }

/* ── SUPPORTING SIGNALS (bar leaderboards) ────────────── */
.ec-support-grid{ display:grid; grid-template-columns: 1fr 1fr; gap:64px; margin: 8px 0 56px 0; }
.ec-lb-row{ display:grid; grid-template-columns: 20px 108px 1fr 34px; align-items:center; gap:12px; padding: 9px 0; border-bottom: 1px solid var(--line); }
.ec-lb-row:last-child{ border-bottom:none; }
.ec-lb-rank{ font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-300); }
.ec-lb-label{ font-family:'Inter', sans-serif; font-size:13.5px; color: var(--ink-900); font-weight:500;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.ec-lb-bar-track{ height:5px; background: var(--line); border-radius:2px; overflow:hidden; }
.ec-lb-bar-fill{ height:100%; background: var(--ink-900); border-radius:2px; }
.ec-lb-row:first-child .ec-lb-bar-fill{ background: var(--navy); }
.ec-lb-count{ font-family:'IBM Plex Mono', monospace; font-size:12px; color: var(--ink-500); text-align:right; font-variant-numeric: tabular-nums; }

/* ── ACTIVITY LIST (news) ─────────────────────────────── */
.ec-activity-wrap{ background: transparent; }
.ec-act-row{ display:grid; grid-template-columns: 84px 1fr 130px 90px; align-items:baseline; gap:20px;
  padding: 14px 0; border-bottom: 1px solid var(--line); }
.ec-act-row:first-child{ border-top: 1px solid var(--line-strong); }
.ec-act-time{ font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-500); }
.ec-act-title{ font-family:'Fraunces', serif; font-weight:480; font-size:16px; color: var(--ink-900);
  line-height:1.35; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ec-act-source{ font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-500); text-transform:uppercase; letter-spacing:0.04em; }
.ec-act-sent{ display:flex; align-items:center; gap:7px; justify-content:flex-end; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.04em; text-transform:uppercase; }
.ec-act-sent i{ width:6px; height:6px; border-radius:50%; display:inline-block; }
.ec-pos{ color: var(--green); } .ec-pos i{ background: var(--green); }
.ec-neu{ color: var(--ink-500); } .ec-neu i{ background: var(--ink-300); }
.ec-neg{ color: var(--red); } .ec-neg i{ background: var(--red); }

/* ── FOOTER ───────────────────────────────────────────── */
.ec-footer{
  display:flex; align-items:center; justify-content:space-between;
  margin-top:56px; padding-top:20px; border-top:1px solid var(--line);
  font-family:'IBM Plex Mono', monospace; font-size:11px; color: var(--ink-500);
}
.ec-footer-stack span{ margin-left:14px; }

/* ── RESPONSIVE ───────────────────────────────────────── */
@media (max-width: 900px){
  .ec-kpi-strip{ grid-template-columns: repeat(2, 1fr); }
  .ec-insight{ grid-template-columns: 1fr; gap:32px; }
  .ec-insight-stat{ font-size:80px; }
  .ec-support-grid{ grid-template-columns: 1fr; gap:32px; }
  .ec-act-row{ grid-template-columns: 1fr; gap:4px; }
}
</style>
""", unsafe_allow_html=True)

# ── DB CONNECTION ──────────────────────────────────────────
import streamlit as st
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

@st.cache_data(ttl=600)
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ── QUERIES (identical SQL to original) ─────────────────────
total_jobs    = run_query("SELECT COUNT(*) as c FROM ai_jobs")["c"][0]
total_news    = run_query("SELECT COUNT(*) as c FROM ai_news")["c"][0]
avg_sentiment = float(run_query("SELECT ROUND(AVG(sentiment_score),3) as c FROM ai_news")["c"][0] or 0)
positive_pct  = float(run_query("""
    SELECT ROUND(100.0 * SUM(sentiment_label='positive') / COUNT(*), 1) as c FROM ai_news
""")["c"][0] or 0)

jobs_by_location = run_query("""
    SELECT 
        CASE WHEN location IS NULL OR location = '' THEN 'Remote / Unknown'
             ELSE location END AS location,
        COUNT(*) as job_count
    FROM ai_jobs
    GROUP BY location
    ORDER BY job_count DESC
    LIMIT 10
""")

sentiment_counts = run_query("""
    SELECT sentiment_label, COUNT(*) as count FROM ai_news GROUP BY sentiment_label
""")

trends_df = run_query("SELECT keyword, week, interest_score FROM ai_trends ORDER BY week ASC")
trends_df["week"] = pd.to_datetime(trends_df["week"])

news_df = run_query("""
    SELECT title, source, published_at, sentiment_label, sentiment_score
    FROM ai_news ORDER BY published_at DESC LIMIT 20
""")

jobs_df = run_query("SELECT title, skills FROM ai_jobs WHERE title IS NOT NULL")

ai_skills = [
    "python", "machine learning", "deep learning", "nlp", "tensorflow",
    "pytorch", "sql", "docker", "aws", "azure", "kubernetes",
    "data science", "llm", "computer vision", "spark",
    "analyst", "engineer", "scientist", "researcher", "ai", "ml"
]
skill_counts = {}
for _, row in jobs_df.iterrows():
    text = (str(row["title"]) + " " + str(row["skills"])).lower()
    for skill in ai_skills:
        if skill in text:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

# ── PRESENTATION-ONLY DERIVED VALUES (display formatting only) ──
sent_map = {r["sentiment_label"]: r["count"] for _, r in sentiment_counts.iterrows()}
pos_c, neu_c, neg_c = sent_map.get("positive", 0), sent_map.get("neutral", 0), sent_map.get("negative", 0)
tot_c = (pos_c + neu_c + neg_c) or 1
pos_pct2, neu_pct2, neg_pct2 = pos_c / tot_c * 100, neu_c / tot_c * 100, neg_c / tot_c * 100

top_location = jobs_by_location.iloc[0]["location"] if not jobs_by_location.empty else "remote-first teams"
sentiment_word = "net positive" if positive_pct >= 50 else "mixed to cautious"
now_str  = datetime.now().strftime("%b %d, %Y")
time_str = datetime.now().strftime("%H:%M")

def sparkline(values, color):
    values = [float(v) for v in values]
    if len(values) < 2:
        return ""
    w, h = 60, 22
    lo, hi = min(values), max(values)
    rng = (hi - lo) or 1
    step = w / (len(values) - 1)
    pts = " ".join(f"{i*step:.1f},{h-((v-lo)/rng)*h:.1f}" for i, v in enumerate(values))
    return (f'<svg class="ec-spark" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">'
            f'<polyline points="{pts}" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def segbar(parts):
    total = sum(v for v, _ in parts) or 1
    spans = "".join(f'<span style="width:{v/total*100:.1f}%;background:{c};"></span>' for v, c in parts)
    return f'<div class="ec-segbar">{spans}</div>'

trend_spark_vals = (
    trends_df.groupby("week")["interest_score"].mean().tolist()
    if not trends_df.empty else [0, 0]
)

# ── MASTHEAD ─────────────────────────────────────────────────
st.markdown(f"""
<div class="ec-masthead">
  <div>
    <div class="ec-eyebrow">Executive Briefing · AI Sector</div>
    <div class="ec-wordmark">AI Intelligence</div>
  </div>
  <div class="ec-masthead-right">
    <div class="ec-live"><span class="ec-live-dot"></span>Live</div>
    <div class="ec-timestamp">{now_str} — {time_str}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── EXECUTIVE SUMMARY ──────────────────────────────────────────
st.markdown(f"""
<p class="ec-summary">
Sentiment across <b>{total_news} tracked articles</b> is running <b>{sentiment_word}</b>
at {positive_pct:.0f}% favorable, while <b>{total_jobs} open AI roles</b> remain concentrated
around <b>{top_location}</b>. The signals below are refreshed on a rolling basis from
live job postings, news coverage, and search interest.
</p>
""", unsafe_allow_html=True)

# ── KPI STRIP ──────────────────────────────────────────────────
loc_parts = [(int(r["job_count"]), c) for r, c in zip(
    jobs_by_location.head(5).to_dict("records"),
    ["#16233F", "#45454B", "#78787F", "#C6C6CB", "#E7E7E9"]
)] if not jobs_by_location.empty else [(1, "#E7E7E9")]

sent_parts = [(pos_c, "#1E7145"), (neu_c, "#C6C6CB"), (neg_c, "#A13434")]

sent_trend_cls = "up" if avg_sentiment > 0 else ("down" if avg_sentiment < 0 else "")
sent_arrow = "▲" if avg_sentiment > 0 else ("▼" if avg_sentiment < 0 else "—")
pos_trend_cls = "up" if positive_pct >= 50 else "down"
pos_arrow = "▲" if positive_pct >= 50 else "▼"

st.markdown(f"""
<div class="ec-kpi-strip">

  <div class="ec-tile c-navy">
    <div class="ec-tile-eyebrow">AI Jobs Tracked</div>
    <div class="ec-tile-value">{total_jobs}</div>
    <div class="ec-tile-foot">
      {segbar(loc_parts)}
      <div class="ec-tile-delta">{top_location}<br>leads listings</div>
    </div>
  </div>

  <div class="ec-tile c-brass">
    <div class="ec-tile-eyebrow">News Articles</div>
    <div class="ec-tile-value">{total_news}</div>
    <div class="ec-tile-foot">
      {segbar(sent_parts)}
      <div class="ec-tile-delta {pos_trend_cls}">{pos_arrow} {positive_pct:.0f}% favorable</div>
    </div>
  </div>

  <div class="ec-tile {'c-green' if avg_sentiment >= 0 else 'c-red'}">
    <div class="ec-tile-eyebrow">Avg Sentiment</div>
    <div class="ec-tile-value">{avg_sentiment:+.3f}</div>
    <div class="ec-tile-foot">
      {sparkline(trend_spark_vals, "#16233F")}
      <div class="ec-tile-delta">{sent_arrow} polarity, −1 to +1</div>
    </div>
  </div>

  <div class="ec-tile {'c-green' if positive_pct >= 50 else 'c-red'}">
    <div class="ec-tile-eyebrow">Positive Coverage</div>
    <div class="ec-tile-value">{positive_pct:.0f}%</div>
    <div class="ec-tile-foot">
      {segbar([(pos_c, "#1E7145"), (tot_c - pos_c, "#E7E7E9")])}
      <div class="ec-tile-delta {pos_trend_cls}">{"majority positive" if positive_pct >= 50 else "below majority"}</div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ── EXECUTIVE INSIGHT (signature moment) ────────────────────────
ring_style = (
    f"background: conic-gradient(#1E7145 0% {pos_pct2:.2f}%, "
    f"#C6C6CB {pos_pct2:.2f}% {pos_pct2+neu_pct2:.2f}%, "
    f"#A13434 {pos_pct2+neu_pct2:.2f}% 100%);"
)

st.markdown(f"""
<div class="ec-insight">
  <div>
    <div class="ec-eyebrow">Most Important Signal</div>
    <div class="ec-insight-stat">{positive_pct:.0f}<sup>%</sup></div>
    <p class="ec-insight-text">
      of AI news coverage skews favorable — the strongest single indicator this cycle.
      Neutral commentary accounts for {neu_pct2:.0f}%, with only {neg_pct2:.0f}% carrying
      a negative tone across {total_news} sources analyzed.
    </p>
  </div>
  <div class="ec-insight-right">
    <div class="ec-ring" style="{ring_style}">
      <div class="ec-ring-hole"><span>{total_news}</span><small>Articles</small></div>
    </div>
    <div class="ec-ring-legend">
      <div><i style="background:#1E7145;"></i>Positive {pos_pct2:.0f}%</div>
      <div><i style="background:#C6C6CB;"></i>Neutral {neu_pct2:.0f}%</div>
      <div><i style="background:#A13434;"></i>Negative {neg_pct2:.0f}%</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── DOMINANT CHART: KEYWORD INTEREST OVER TIME ──────────────────
st.markdown("""
<div class="ec-section">
  <div class="ec-section-title">Keyword Interest Over Time</div>
  <div class="ec-section-sub">Search attention · weekly · five tracked AI topics</div>
</div>
""", unsafe_allow_html=True)

TREND_COLORS = ["#16233F", "#1E7145", "#A13434", "#78787F", "#9C6B1F"]
keywords_list = trends_df["keyword"].unique().tolist()

legend_html = "".join(
    f'<div><i style="background:{TREND_COLORS[i % len(TREND_COLORS)]};"></i>{kw}</div>'
    for i, kw in enumerate(keywords_list)
)
st.markdown(f'<div class="ec-chart-legend">{legend_html}</div>', unsafe_allow_html=True)

FONT = dict(family="Inter, -apple-system, sans-serif", color="#78787F", size=11)
AXIS = dict(
    showgrid=True, gridcolor="rgba(18,18,20,0.06)", gridwidth=1,
    tickfont=dict(family="IBM Plex Mono", color="#78787F", size=10),
    showline=False, zeroline=False, ticks="",
)

fig = go.Figure()
for i, kw in enumerate(keywords_list):
    kw_df = trends_df[trends_df["keyword"] == kw]
    color = TREND_COLORS[i % len(TREND_COLORS)]
    fig.add_trace(go.Scatter(
        x=kw_df["week"], y=kw_df["interest_score"],
        name=kw, mode="lines",
        line=dict(color=color, width=1.8, shape="spline", smoothing=0.3),
        hovertemplate=f"<b>{kw}</b>  %{{y}}<extra></extra>",
    ))
fig.update_layout(
    height=300,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=FONT, showlegend=False,
    margin=dict(t=6, b=6, l=6, r=6),
    xaxis={**AXIS, "showgrid": False, "tickformat": "%b %d"},
    yaxis={**AXIS, "range": [0, 105]},
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#121214", bordercolor="rgba(0,0,0,0)",
                     font=dict(family="Inter", color="#FAFAF9", size=12)),
)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── SUPPORTING SIGNALS: LOCATIONS + SKILLS ──────────────────────
col_a, col_b = st.columns(2, gap="large")

with col_a:
    st.markdown("""
    <div class="ec-section">
      <div class="ec-section-title">Top Hiring Locations</div>
      <div class="ec-section-sub">By open role count</div>
    </div>
    """, unsafe_allow_html=True)

    max_jobs = int(jobs_by_location["job_count"].max()) if not jobs_by_location.empty else 1
    rows = ""
    for i, r in enumerate(jobs_by_location.head(6).to_dict("records"), start=1):
        pct = r["job_count"] / max_jobs * 100
        rows += f"""
        <div class="ec-lb-row">
          <span class="ec-lb-rank">{i:02d}</span>
          <span class="ec-lb-label">{r['location']}</span>
          <span class="ec-lb-bar-track"><span class="ec-lb-bar-fill" style="width:{pct:.0f}%;"></span></span>
          <span class="ec-lb-count">{r['job_count']}</span>
        </div>"""
    st.markdown(rows, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="ec-section">
      <div class="ec-section-title brass">In-Demand AI Skills</div>
      <div class="ec-section-sub">Mentions across job titles &amp; listings</div>
    </div>
    """, unsafe_allow_html=True)

    if skill_counts:
        skills_sorted = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:6]
        max_skill = skills_sorted[0][1]
        rows = ""
        for i, (skill, count) in enumerate(skills_sorted, start=1):
            pct = count / max_skill * 100
            rows += f"""
            <div class="ec-lb-row">
              <span class="ec-lb-rank">{i:02d}</span>
              <span class="ec-lb-label">{skill.title()}</span>
              <span class="ec-lb-bar-track"><span class="ec-lb-bar-fill" style="width:{pct:.0f}%;"></span></span>
              <span class="ec-lb-count">{count}</span>
            </div>"""
        st.markdown(rows, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:var(--ink-500);font-size:13px;">No skill data found.</p>', unsafe_allow_html=True)

# ── LATEST ACTIVITY ──────────────────────────────────────────────
st.markdown("""
<div class="ec-section" style="margin-top:56px;">
  <div class="ec-section-title">Latest Activity</div>
  <div class="ec-section-sub">Most recent AI news, sentiment analyzed on ingest</div>
</div>
""", unsafe_allow_html=True)

sent_cls_map = {"positive": "ec-pos", "negative": "ec-neg"}

rows_html = ""
for _, row in news_df.iterrows():
    label = str(row["sentiment_label"])
    cls = sent_cls_map.get(label, "ec-neu")
    date = str(row["published_at"])[:10]
    src = str(row["source"]).upper()
    title = str(row["title"]).replace("<", "&lt;").replace(">", "&gt;")
    rows_html += f"""
    <div class="ec-act-row">
      <span class="ec-act-time">{date}</span>
      <span class="ec-act-title">{title}</span>
      <span class="ec-act-source">{src}</span>
      <span class="ec-act-sent {cls}"><i></i>{label}</span>
    </div>"""

table_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,480&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap');
*{ margin:0; padding:0; box-sizing:border-box; }
body{ background:transparent; font-family:'Inter', sans-serif; }
.ec-act-row{ display:grid; grid-template-columns: 84px 1fr 130px 90px; align-items:baseline; gap:20px;
  padding: 14px 4px; border-bottom: 1px solid #E7E7E9; }
.ec-act-row:first-child{ border-top: 1px solid #D6D6D9; }
.ec-act-time{ font-family:'IBM Plex Mono', monospace; font-size:11px; color:#78787F; }
.ec-act-title{ font-family:'Fraunces', serif; font-weight:480; font-size:16px; color:#121214;
  line-height:1.35; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ec-act-source{ font-family:'IBM Plex Mono', monospace; font-size:11px; color:#78787F; letter-spacing:0.04em; }
.ec-act-sent{ display:flex; align-items:center; gap:7px; justify-content:flex-end;
  font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.04em; text-transform:uppercase; }
.ec-act-sent i{ width:6px; height:6px; border-radius:50%; display:inline-block; }
.ec-pos{ color:#1E7145; } .ec-pos i{ background:#1E7145; }
.ec-neu{ color:#78787F; } .ec-neu i{ background:#C6C6CB; }
.ec-neg{ color:#A13434; } .ec-neg i{ background:#A13434; }
</style>
"""

import streamlit.components.v1 as components
components.html(f"{table_css}<div>{rows_html}</div>", height=560, scrolling=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="ec-footer">
  <div>AI Intelligence · Executive Briefing · Compiled by Omer</div>
  <div class="ec-footer-stack">
    Python <span>MySQL</span><span>Streamlit</span><span>Plotly</span>
    <span>{now_str} {time_str}</span>
  </div>
</div>
""", unsafe_allow_html=True)
