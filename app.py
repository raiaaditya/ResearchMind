import os
import re
import time
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
from agents import search_agent, reader_agent, writer_agent, critic_agent

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Tokens ──────────────────────────────────────────────────────────────── */
:root {
    --bg:          #0d0f14;
    --bg-card:     #111827;
    --bg-input:    #1a1e2a;
    --border:      #1F2937;
    --border-hi:   #374151;
    --accent:      #8B5CF6;
    --accent-dim:  #6D28D9;
    --accent-glow: rgba(139,92,246,0.4);
    --blue:        #3B82F6;
    --success:     #22C55E;
    --success-dim: rgba(34,197,94,0.15);
    --warn:        #F59E0B;
    --error:       #EF4444;
    --error-dim:   rgba(239,68,68,0.15);
    --txt-pri:     #F3F4F6;
    --txt-sec:     #D1D5DB;
    --txt-muted:   #6B7280;
}

/* ── Imports + base ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; font-size: 16px; }
.stApp { background: var(--bg); color: var(--txt-pri); margin: 0; padding: 0; }
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 4px; }

/* Full width layout */
.block-container { max-width: 100% !important; padding-left: 1rem !important; padding-right: 1rem !important; }

/* ── Hero / Brand ────────────────────────────────────────────────────────── */
.hero { 
    padding: 1.5rem 0 0.5rem; 
    text-align: center; 
    position: relative;
}

.hero::before {
    content: '';
    position: absolute;
    top: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%);
    border-radius: 50%;
    z-index: -1;
}

.brand-name {
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    line-height: 1.05;
    margin: 0;
    background: linear-gradient(135deg, #C4B5FD 0%, #8B5CF6 45%, #3B82F6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 0 40px rgba(139,92,246,0.3);
}
.brand-tagline {
    display: block;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: var(--accent);
    opacity: 0.9;
    margin: 0.5rem 0 1.5rem;
}
.hero-title {
    font-size: 1.4rem;
    font-weight: 500;
    color: var(--txt-sec);
    margin: 0 0 0.5rem;
    line-height: 1.55;
}
.hero-sub {
    font-size: 1rem;
    color: var(--txt-muted);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 500;
    margin-top: 0.5rem;
}
.hero-divider {
    width: 64px; height: 4px;
    margin: 1.5rem auto 0;
    background: linear-gradient(90deg, var(--accent), var(--blue));
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(139,92,246,0.4);
}

/* ── Panels ──────────────────────────────────────────────────────────────── */
.panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
}
.panel-title {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--txt-muted);
    margin-bottom: 1.8rem;
}

/* ── Input ───────────────────────────────────────────────────────────────── */
.stTextInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--txt-pri) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    line-height: 1.5 !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--txt-muted) !important;
    font-size: 1rem !important;
}

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-dim)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 1rem 2rem !important;
    width: 100% !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 18px var(--accent-glow) !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #9D6FF8, var(--accent)) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px var(--accent-glow) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1.5px solid var(--accent-dim) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: 0.8rem 1.6rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(139,92,246,0.1) !important;
    border-color: var(--accent) !important;
    box-shadow: 0 0 12px var(--accent-glow) !important;
}

/* ── Pipeline ────────────────────────────────────────────────────────────── */
.pipeline-wrap { display: flex; flex-direction: column; gap: 0.5rem; }

.pipe-step {
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    padding: 1.2rem 1rem;
    position: relative;
    border-radius: 12px;
    transition: background 0.25s;
}
.pipe-step.active {
    background: rgba(139,92,246,0.12);
    box-shadow: inset 0 0 0 1px rgba(139,92,246,0.25);
}
.pipe-step:not(:last-child)::after {
    content: '';
    position: absolute;
    left: 26px; top: 52px;
    width: 3px;
    height: calc(100% - 20px);
    background: var(--border);
    transition: background 0.4s;
}
.pipe-step.done:not(:last-child)::after {
    background: linear-gradient(180deg, var(--accent-dim), var(--accent));
}

.pipe-icon {
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
    background: #161B2E;
    border: 1.5px solid var(--border-hi);
    z-index: 1;
    transition: all 0.35s ease;
}
.pipe-step.done .pipe-icon {
    background: #1A1040;
    border-color: var(--accent-dim);
    box-shadow: 0 0 0 4px rgba(109,40,217,0.22);
}
.pipe-step.active .pipe-icon {
    background: #1A1040;
    border-color: var(--accent);
    animation: pulse 1.6s ease-in-out infinite;
}
.pipe-step.failed .pipe-icon {
    background: #1F0A0A;
    border-color: var(--error);
    box-shadow: 0 0 12px rgba(239,68,68,0.4);
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 12px var(--accent-glow), 0 0 0 4px rgba(139,92,246,0.15); }
    50%       { box-shadow: 0 0 28px var(--accent-glow), 0 0 0 8px rgba(139,92,246,0.25); }
}
@keyframes stepIn {
    from { opacity: 0; transform: translateX(-8px); }
    to   { opacity: 1; transform: translateX(0); }
}
.pipe-step.active { animation: stepIn 0.25s ease forwards; }

.pipe-body { flex: 1; min-width: 0; }

.pipe-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--txt-muted);
    line-height: 1.4;
    transition: color 0.3s;
}
.pipe-step.done   .pipe-name { color: #C4B5FD; }
.pipe-step.active .pipe-name { color: var(--txt-pri); font-weight: 700; }
.pipe-step.failed .pipe-name { color: var(--error); }

.pipe-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    padding: 0.25rem 0.8rem;
    border-radius: 99px;
    margin-top: 0.35rem;
    transition: all 0.3s;
}
.badge-idle    { background: #161B2E; color: var(--txt-muted); border: 1px solid var(--border); }
.badge-running { background: rgba(139,92,246,0.18); color: #DDD6FE; border: 1px solid rgba(139,92,246,0.4); animation: fadepulse 1.1s ease-in-out infinite; }
.badge-done    { background: var(--success-dim); color: var(--success); border: 1px solid rgba(34,197,94,0.3); }
.badge-failed  { background: var(--error-dim); color: var(--error); border: 1px solid rgba(239,68,68,0.3); }

@keyframes fadepulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.pipe-detail {
    font-size: 0.85rem;
    color: var(--txt-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.25rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 240px;
}

/* ── Progress bar ────────────────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--blue)) !important;
    border-radius: 4px !important;
    transition: width 0.4s ease !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 4px !important;
    height: 6px !important;
}

/* ── Metrics ─────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1.5rem 1.8rem !important;
}
[data-testid="metric-container"] label {
    color: var(--txt-sec) !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--txt-pri) !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 3px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--txt-sec) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--txt-pri) !important;
    background: rgba(255,255,255,0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(139,92,246,0.18) !important;
    color: #DDD6FE !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.6rem !important; }

/* ── Output cards ────────────────────────────────────────────────────────── */
.out-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.out-card:hover {
    border-color: var(--border-hi);
    box-shadow: 0 6px 32px rgba(0,0,0,0.4);
}
.out-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.card-search::before { background: linear-gradient(180deg, #93C5FD, var(--blue)); }
.card-tavily::before { background: linear-gradient(180deg, #6EE7B7, var(--success)); }
.card-reader::before { background: linear-gradient(180deg, #F9A8D4, #EC4899); }
.card-writer::before { background: linear-gradient(180deg, #DDD6FE, var(--accent)); }
.card-critic::before { background: linear-gradient(180deg, #FCD34D, var(--warn)); }

.card-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.3rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}
.card-icon { font-size: 1.4rem; }
.card-title {
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.card-search .card-title { color: #93C5FD; }
.card-tavily .card-title { color: #6EE7B7; }
.card-reader .card-title { color: #F9A8D4; }
.card-writer .card-title { color: #DDD6FE; }
.card-critic .card-title { color: #FCD34D; }

.card-body {
    font-size: 1.1rem;
    line-height: 1.85;
    color: var(--txt-pri);
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.01em;
}

/* ── Expanders ───────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--txt-sec) !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 0.8rem 1.1rem !important;
}
.streamlit-expanderHeader:hover { color: var(--txt-pri) !important; border-color: var(--border-hi) !important; }
.streamlit-expanderContent {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.2rem !important;
}

/* ── Success banner ──────────────────────────────────────────────────────── */
.success-banner {
    background: linear-gradient(135deg, #052e16, #0b2818);
    border: 1px solid rgba(34,197,94,0.35);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
    box-shadow: 0 0 24px rgba(34,197,94,0.1);
    animation: slideIn 0.4s ease;
}
@keyframes slideIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.success-banner span { color: var(--success); font-size: 1.1rem; font-weight: 600; line-height: 1.5; }

/* ── Divider + alerts ────────────────────────────────────────────────────── */
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 2rem 0 !important; }
.stAlert { border-radius: 12px !important; font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Env + backend helpers (unchanged)
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def fetch_tavily_snippets(query: str, max_results: int = 5) -> tuple[str, int]:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    results = client.search(query=query, max_results=max_results)
    snippets = []
    for res in results.get("results", []):
        snippet = res.get("content") or res.get("snippet")
        if snippet:
            snippets.append(f"- Source: {res.get('url', '')}\n{snippet}")
    return "\n\n".join(snippets), len(snippets)


def extract_critic_score(critique: str) -> int | None:
    matches = re.findall(r'\b([0-9]|10)\s*/\s*10\b', critique)
    if matches:
        return int(matches[0])
    matches = re.findall(r'score[:\s]+([0-9]|10)\b', critique, re.IGNORECASE)
    if matches:
        return int(matches[0])
    return None


# ─────────────────────────────────────────────────────────────────────────────
# UI helpers
# ─────────────────────────────────────────────────────────────────────────────
STEPS = [
    ("search", "🔍", "Search Agent"),
    ("tavily", "🌐", "Tavily Fetch"),
    ("reader", "📖", "Reader Agent"),
    ("writer", "✍️",  "Writer Agent"),
    ("critic", "🔎", "Critic Agent"),
]


def render_pipeline(statuses: dict) -> str:
    step_cls_map  = {"idle": "", "running": "active", "done": "done", "failed": "failed"}
    badge_cls_map = {"idle": "badge-idle", "running": "badge-running", "done": "badge-done", "failed": "badge-failed"}
    badge_txt_map = {"idle": "Waiting", "running": "⏳ Running", "done": "✅ Done", "failed": "❌ Failed"}
    parts = ['<div class="pipeline-wrap">']
    for sid, icon, label in STEPS:
        info       = statuses.get(sid, {"state": "idle", "detail": ""})
        state      = info["state"]
        detail     = info.get("detail", "")
        step_cls   = step_cls_map.get(state, "")
        badge_cls  = badge_cls_map.get(state, "badge-idle")
        badge_txt  = badge_txt_map.get(state, "Waiting")
        detail_tag = f'<div class="pipe-detail">{detail}</div>' if detail else ""
        parts.append(
            f'<div class="pipe-step {step_cls}">'
            f'<div class="pipe-icon">{icon}</div>'
            f'<div class="pipe-body">'
            f'<div class="pipe-name">{label}</div>'
            f'<span class="pipe-badge {badge_cls}">{badge_txt}</span>'
            f'{detail_tag}'
            f'</div>'
            f'</div>'
        )
    parts.append('</div>')
    return "".join(parts)


def out_card(variant: str, icon: str, title: str, body: str):
    html = (
        f'<div class="out-card card-{variant}">'
        f'<div class="card-header">'
        f'<span class="card-icon">{icon}</span>'
        f'<span class="card-title">{title}</span>'
        f'</div>'
        f'<div class="card-body">{body}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def typing_effect(placeholder, text: str, chunk: int = 20, delay: float = 0.015):
    words = text.split(" ")
    displayed = ""
    for i, word in enumerate(words):
        displayed += ("" if i == 0 else " ") + word
        if i % chunk == 0:
            html = (
                '<div class="out-card card-writer">'
                '<div class="card-header">'
                '<span class="card-icon">✍️</span>'
                '<span class="card-title">Writer Agent — Final Report</span>'
                '</div>'
                f'<div class="card-body">{displayed}▌</div>'
                '</div>'
            )
            placeholder.markdown(html, unsafe_allow_html=True)
            time.sleep(delay)
    html = (
        '<div class="out-card card-writer">'
        '<div class="card-header">'
        '<span class="card-icon">✍️</span>'
        '<span class="card-title">Writer Agent — Final Report</span>'
        '</div>'
        f'<div class="card-body">{text}</div>'
        '</div>'
    )
    placeholder.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero">'
    '<h1 class="brand-name">ResearchMind</h1>'
    '<span class="brand-tagline">Powered by Multi-Agent AI</span>'
    '<p class="hero-title">🤖 Multi-Agent AI Research System</p>'
    '<p class="hero-sub">Search · Fetch · Extract · Synthesize · Evaluate</p>'
    '<div class="hero-divider"></div>'
    '</div>',
    unsafe_allow_html=True,
)

if not TAVILY_API_KEY:
    st.error("⚠️  TAVILY_API_KEY not found. Add it to your .env file and restart.")
    st.stop()

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Split layout
# ─────────────────────────────────────────────────────────────────────────────
left, right = st.columns([1, 2], gap="medium")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">Research Query</p>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="Enter a research topic…",
        key="research_topic",
    )
    st.markdown("<br style='margin:0.3rem'>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run Research", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<p class="panel-title">Agent Pipeline</p>', unsafe_allow_html=True)

# pipeline_ph and progress_ph MUST be created as st.empty() inside their column
# but referenced globally — we do this by keeping them in left column scope
# and calling .markdown() on them directly (works across column boundaries).
with left:
    pipeline_ph = st.empty()
    st.markdown("<br>", unsafe_allow_html=True)
    progress_ph = st.empty()
    st.markdown("</div>", unsafe_allow_html=True)  # close .panel

# Render initial idle state
idle_statuses = {sid: {"state": "idle", "detail": ""} for sid, _, _ in STEPS}
pipeline_ph.markdown(render_pipeline(idle_statuses), unsafe_allow_html=True)
progress_ph.progress(0)

with right:
    output_ph = st.empty()
    output_ph.markdown(
        '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
        'height:360px;color:#2d3748;text-align:center;gap:1rem;">'
        '<div style="font-size:3.5rem">🤖</div>'
        '<div style="font-size:1.2rem;font-weight:500;color:#334155">Ready to research</div>'
        '<div style="font-size:1rem;color:#1e293b;max-width:400px;">Enter a topic on the left and hit Run Research to start the multi-agent analysis pipeline</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Pipeline execution
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        with left:
            st.warning("Please enter a research topic first.")
        st.stop()

    statuses: dict = {sid: {"state": "idle", "detail": ""} for sid, _, _ in STEPS}

    def update(step_id: str, state: str, detail: str = "", pct: float = 0.0):
        statuses[step_id] = {"state": state, "detail": detail}
        pipeline_ph.empty()
        pipeline_ph.markdown(render_pipeline(statuses), unsafe_allow_html=True)
        progress_ph.progress(pct)

    with right:
        output_ph.empty()

        # Step 1 — Search Agent
        update("search", "running", "Generating query…", 0.05)
        search_query = search_agent(topic)
        time.sleep(0.4)
        update("search", "done", (search_query[:55] + "…") if len(search_query) > 55 else search_query, 0.20)

        # Step 2 — Tavily Fetch
        update("tavily", "running", "Fetching live sources…", 0.25)
        snippets, snippet_count = fetch_tavily_snippets(search_query)
        time.sleep(0.4)
        if not snippets:
            update("tavily", "failed", "No results returned", 0.25)
            st.error("Tavily returned no results. Try a different topic.")
            st.stop()
        update("tavily", "done", f"{snippet_count} snippets retrieved", 0.42)

        # Step 3 — Reader Agent
        update("reader", "running", "Extracting insights…", 0.46)
        insights = reader_agent(snippets)
        time.sleep(0.4)
        update("reader", "done", "Insights extracted", 0.62)

        # Step 4 — Writer Agent
        update("writer", "running", "Composing report…", 0.66)
        report = writer_agent(insights)
        time.sleep(0.4)
        update("writer", "done", "Report ready", 0.82)

        # Step 5 — Critic Agent
        update("critic", "running", "Evaluating report…", 0.86)
        critique = critic_agent(report)
        time.sleep(0.4)
        update("critic", "done", "Evaluation complete", 1.0)

        # Save
        report_text = (
            "=== Analytical Research Report ===\n\n"
            + report
            + "\n\n=== Critic Evaluation ===\n\n"
            + critique
        )
        with open("final_report.txt", "w", encoding="utf-8") as f:
            f.write(report_text)

        # Metrics
        score = extract_critic_score(critique)
        m1, m2, m3 = st.columns(3)
        m1.metric("📦 Sources", snippet_count)
        m2.metric("📝 Words", len(report.split()))
        m3.metric("📊 Score", f"{score}/10" if score is not None else "—")

        st.markdown("<hr>", unsafe_allow_html=True)

        # Tabs
        tab_report, tab_insights, tab_critic, tab_raw = st.tabs([
            "📄 Report", "📊 Insights", "💬 Critic Feedback", "🗂 Raw Data"
        ])

        with tab_report:
            typing_ph = st.empty()
            typing_effect(typing_ph, report)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                "⬇  Download Report",
                data=report_text,
                file_name="final_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with tab_insights:
            out_card("reader", "📖", "Reader Agent — Extracted Insights", insights)

        with tab_critic:
            out_card("critic", "🔎", "Critic Agent — Evaluation", critique)

        with tab_raw:
            with st.expander("🔍 Search Query", expanded=False):
                out_card("search", "🔍", "Search Agent — Generated Query", search_query)
            with st.expander(f"🌐 Tavily Snippets ({snippet_count} sources)", expanded=False):
                st.code(snippets[:4000] + ("…" if len(snippets) > 4000 else ""), language=None)

        st.markdown(
            '<div class="success-banner">'
            '<span>🎉</span>'
            '<span>Research complete! Report saved to '
            '<code style="background:#1a1e2a;padding:0.1rem 0.4rem;border-radius:4px;font-size:0.82rem;">final_report.txt</code>'
            '</span></div>',
            unsafe_allow_html=True,
        )