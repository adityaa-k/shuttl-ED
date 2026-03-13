"""
ShuttleForce — Custom CSS Branding (v2 — Mobile-First + UUPM Optimized)

Design System:
  Style:       Glassmorphism Dark
  Primary:     #00E5FF (Electric Cyan)
  Secondary:   #FFB300 (Warm Amber)
  Background:  #0A1628 (Deep Navy)
  Panel:       #112240
  Text:        #E0E6ED
  Muted:       #8892A0
  Typography:  Inter (body) / Outfit (headings)

  Breakpoints: 375px · 480px · 768px · 1024px · 1440px
  Transitions: 200ms ease (standard) / 150ms (micro) / 300ms (entrance)
"""

GOOGLE_FONTS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
"""

MAIN_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════
   DESIGN TOKENS
   ═══════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap');

:root {
    --navy:       #0A1628;
    --panel:      #112240;
    --panel-alt:  #162a50;
    --cyan:       #00E5FF;
    --cyan-dim:   rgba(0, 229, 255, 0.65);
    --amber:      #FFB300;
    --amber-dim:  rgba(255, 179, 0, 0.65);
    --text:       #E0E6ED;
    --muted:      #8892A0;
    --glass:      rgba(17, 34, 64, 0.6);
    --glass-heavy:rgba(17, 34, 64, 0.85);
    --border:     rgba(0, 229, 255, 0.15);
    --border-hover:rgba(0, 229, 255, 0.35);
    --glow:       0 0 20px rgba(0, 229, 255, 0.12);
    --glow-strong:0 0 30px rgba(0, 229, 255, 0.22);
    --radius-sm:  8px;
    --radius-md:  12px;
    --radius-lg:  16px;
    --radius-xl:  20px;
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --transition: 200ms ease;
    --transition-fast: 150ms ease;
    --transition-entrance: 300ms ease-out;
    --font-body:  'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-heading: 'Outfit', var(--font-body);
}

/* ═══════════════════════════════════════════════════════════
   GLOBAL RESET & BASE
   ═══════════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: var(--font-body) !important;
    color: var(--text);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
}

/* ── Streamlit Native UI ────────────────────────────── */
/* Keep Streamlit's native header completely untouched so the sidebar toggle always works */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stStatusWidget"] { display: none; }
[data-testid="stDecoration"] { display: none; }


/* ═══════════════════════════════════════════════════════════
   SIDEBAR
   ═══════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B2A 0%, #112240 100%) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

[data-testid="stSidebar"] .stRadio > label {
    font-family: var(--font-heading) !important;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
}

[data-testid="stSidebar"] .stRadio > div > label {
    padding: 0.65rem 1rem !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 4px;
    transition: all var(--transition);
    cursor: pointer;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(0, 229, 255, 0.08) !important;
}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
[data-testid="stSidebar"] .stRadio > div [aria-checked="true"] {
    background: rgba(0, 229, 255, 0.12) !important;
    border-left: 3px solid var(--cyan) !important;
}

/* ── Sidebar Collapsed Toggle (ALWAYS VISIBLE FIX) ──────── */
/* When sidebar is collapsed, Streamlit shows [data-testid="collapsedControl"] */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: all !important;
    background: linear-gradient(135deg, var(--cyan), #00B8D4) !important;
    color: #0A1628 !important;
    border-radius: 0 var(--radius-md) var(--radius-md) 0 !important;
    border: none !important;
    box-shadow: 2px 0 16px rgba(0, 229, 255, 0.3) !important;
    width: 28px !important;
    min-height: 52px !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    position: fixed !important;
    left: 0 !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 9999 !important;
    transition: all var(--transition) !important;
    animation: sidebar-tab-pulse 3s ease-in-out infinite !important;
}

[data-testid="collapsedControl"]:hover {
    width: 36px !important;
    box-shadow: 4px 0 24px rgba(0, 229, 255, 0.5) !important;
    animation: none !important;
    background: linear-gradient(135deg, #33ECFF, var(--cyan)) !important;
}

[data-testid="collapsedControl"] svg {
    color: #0A1628 !important;
    fill: #0A1628 !important;
    stroke: #0A1628 !important;
    width: 14px !important;
    height: 14px !important;
}

@keyframes sidebar-tab-pulse {
    0%, 100% { box-shadow: 2px 0 12px rgba(0, 229, 255, 0.25); }
    50%       { box-shadow: 2px 0 24px rgba(0, 229, 255, 0.5); }
}

/* Also keep the expand/collapse button inside an open sidebar visible */
[data-testid="stSidebar"] button[aria-label="Close sidebar"],
[data-testid="stSidebarNav"] button {
    opacity: 0.6 !important;
    transition: opacity var(--transition-fast) !important;
}
[data-testid="stSidebar"] button[aria-label="Close sidebar"]:hover,
[data-testid="stSidebarNav"] button:hover {
    opacity: 1 !important;
}

/* ═══════════════════════════════════════════════════════════
   GLASS CARD (Core Component)
   ═══════════════════════════════════════════════════════════ */
.glass-card {
    background: var(--glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-md);
    box-shadow: var(--glow);
    transition: transform var(--transition), box-shadow var(--transition);
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--glow-strong);
}

/* ═══════════════════════════════════════════════════════════
   METRIC CARD
   ═══════════════════════════════════════════════════════════ */
.metric-card {
    background: var(--glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--spacing-md) var(--spacing-lg);
    text-align: center;
    box-shadow: var(--glow);
    transition: transform var(--transition-fast), box-shadow var(--transition-fast);
    min-height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.metric-card:hover {
    transform: translateY(-1px);
    box-shadow: var(--glow-strong);
}
.metric-card .metric-value {
    font-family: var(--font-heading);
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 800;
    background: linear-gradient(135deg, var(--cyan), var(--amber));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.metric-card .metric-label {
    color: var(--muted);
    font-size: clamp(0.65rem, 1.5vw, 0.8rem);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: var(--spacing-xs);
}

/* ═══════════════════════════════════════════════════════════
   PAGE TITLE
   ═══════════════════════════════════════════════════════════ */
.page-title {
    font-family: var(--font-heading);
    font-size: clamp(1.5rem, 5vw, 2.2rem);
    font-weight: 800;
    background: linear-gradient(90deg, var(--cyan), var(--amber));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.15rem;
    line-height: 1.2;
}
.page-subtitle {
    color: var(--muted);
    font-size: clamp(0.8rem, 2vw, 0.95rem);
    margin-bottom: var(--spacing-lg);
    line-height: 1.4;
}

/* ═══════════════════════════════════════════════════════════
   SCORE DISPLAY
   ═══════════════════════════════════════════════════════════ */
.score-display {
    font-family: var(--font-heading);
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 800;
    text-align: center;
    line-height: 1;
    padding: var(--spacing-sm) 0;
    user-select: none;
}
.score-team-a { color: var(--cyan); text-shadow: 0 0 20px rgba(0, 229, 255, 0.3); }
.score-team-b { color: var(--amber); text-shadow: 0 0 20px rgba(255, 179, 0, 0.3); }
.score-vs {
    color: var(--muted);
    font-size: clamp(1rem, 3vw, 1.5rem);
    font-weight: 600;
    margin: 0 0.4rem;
}

/* Team labels for live scorer */
.team-label {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: clamp(0.75rem, 2vw, 0.9rem);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    margin-bottom: var(--spacing-xs);
}
.team-label-a { color: var(--cyan-dim); }
.team-label-b { color: var(--amber-dim); }

/* ═══════════════════════════════════════════════════════════
   LEADERBOARD TABLE
   ═══════════════════════════════════════════════════════════ */
.table-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    border-radius: var(--radius-md);
    scrollbar-width: thin;
    scrollbar-color: rgba(0,229,255,0.2) transparent;
}
.table-wrapper::-webkit-scrollbar { height: 4px; }
.table-wrapper::-webkit-scrollbar-track { background: transparent; }
.table-wrapper::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.25); border-radius: 4px; }

.leaderboard-table {
    width: 100%;
    min-width: 360px;
    border-collapse: separate;
    border-spacing: 0 5px;
}
.leaderboard-table th {
    color: var(--muted);
    font-size: clamp(0.6rem, 1.5vw, 0.75rem);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: var(--spacing-sm) var(--spacing-md);
    text-align: left;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    position: sticky;
    top: 0;
    background: var(--navy);
    z-index: 1;
}
.leaderboard-table td {
    padding: 0.65rem var(--spacing-md);
    background: var(--glass);
    font-size: clamp(0.78rem, 1.8vw, 0.9rem);
    white-space: nowrap;
    transition: background var(--transition-fast);
}
.leaderboard-table tr td:first-child {
    border-radius: var(--radius-sm) 0 0 var(--radius-sm);
}
.leaderboard-table tr td:last-child {
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.leaderboard-table tr:hover td {
    background: rgba(0, 229, 255, 0.06);
}

/* Rank badges */
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: var(--radius-sm);
    font-weight: 700;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.rank-1 { background: linear-gradient(135deg, #FFD700, #FFA000); color: #1a1a2e; }
.rank-2 { background: linear-gradient(135deg, #C0C0C0, #9E9E9E); color: #1a1a2e; }
.rank-3 { background: linear-gradient(135deg, #CD7F32, #A0522D); color: #fff; }
.rank-default { background: var(--panel); color: var(--muted); border: 1px solid var(--border); }

/* ═══════════════════════════════════════════════════════════
   BUTTONS (UUPM: cursor-pointer, focus states, transitions)
   ═══════════════════════════════════════════════════════════ */
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-family: var(--font-body) !important;
    transition: all var(--transition) !important;
    border: 1px solid var(--border) !important;
    cursor: pointer !important;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
    min-height: 44px;
    font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
}
.stButton > button:hover {
    box-shadow: 0 0 16px rgba(0, 229, 255, 0.22) !important;
    transform: translateY(-1px);
}
.stButton > button:focus-visible {
    outline: 2px solid var(--cyan) !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 4px rgba(0, 229, 255, 0.2) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--cyan), #00B8D4) !important;
    color: #0A1628 !important;
    font-weight: 700 !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #33ECFF, var(--cyan)) !important;
    box-shadow: 0 4px 20px rgba(0, 229, 255, 0.35) !important;
}

/* ═══════════════════════════════════════════════════════════
   MATCH CARD
   ═══════════════════════════════════════════════════════════ */
.match-card {
    background: var(--glass);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: var(--spacing-md) var(--spacing-lg);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-sm);
    transition: all var(--transition);
    flex-wrap: wrap;
}
.match-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--glow);
}
.match-card .match-info {
    flex: 1;
    min-width: 0;
}
.match-card .match-info span {
    font-size: clamp(0.8rem, 2vw, 0.95rem);
}

/* ═══════════════════════════════════════════════════════════
   STATUS BADGES
   ═══════════════════════════════════════════════════════════ */
.status-badge {
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 20px;
    font-size: clamp(0.6rem, 1.5vw, 0.72rem);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
    flex-shrink: 0;
}
.status-live {
    background: rgba(0, 229, 255, 0.15);
    color: var(--cyan);
    border: 1px solid rgba(0, 229, 255, 0.3);
    animation: pulse-glow 2s ease-in-out infinite;
}
.status-completed {
    background: rgba(76, 175, 80, 0.15);
    color: #66BB6A;
    border: 1px solid rgba(76, 175, 80, 0.3);
}
.status-scheduled {
    background: rgba(255, 179, 0, 0.15);
    color: var(--amber);
    border: 1px solid rgba(255, 179, 0, 0.3);
}

/* ═══════════════════════════════════════════════════════════
   ANIMATIONS (UUPM: prefers-reduced-motion)
   ═══════════════════════════════════════════════════════════ */
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 5px rgba(0, 229, 255, 0.2); }
    50%      { box-shadow: 0 0 15px rgba(0, 229, 255, 0.4); }
}

@keyframes fade-in-up {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}

.fade-in {
    animation: fade-in-up var(--transition-entrance) ease-out;
}

/* UUPM: Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    .glass-card:hover,
    .metric-card:hover,
    .stButton > button:hover {
        transform: none !important;
    }
}

/* ═══════════════════════════════════════════════════════════
   INPUTS / SELECTS (UUPM: focus states)
   ═══════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
    background: var(--panel) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    min-height: 44px;
    transition: border-color var(--transition), box-shadow var(--transition) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.15) !important;
    outline: none !important;
}

.stMultiSelect > div {
    border-radius: var(--radius-md) !important;
}
.stMultiSelect > div > div {
    min-height: 44px;
}

/* ═══════════════════════════════════════════════════════════
   TABS
   ═══════════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    gap: var(--spacing-sm);
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    flex-wrap: nowrap;
}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-md) !important;
    padding: 0.5rem 1rem !important;
    font-weight: 600 !important;
    font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
    white-space: nowrap;
    cursor: pointer;
    min-height: 40px;
    transition: all var(--transition);
}
.stTabs [data-baseweb="tab"]:focus-visible {
    outline: 2px solid var(--cyan);
    outline-offset: 2px;
}

/* ═══════════════════════════════════════════════════════════
   DIVIDER
   ═══════════════════════════════════════════════════════════ */
.brand-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--amber), transparent);
    border: none;
    margin: var(--spacing-lg) 0;
    border-radius: 2px;
}

/* ═══════════════════════════════════════════════════════════
   AI REFEREE CARD
   ═══════════════════════════════════════════════════════════ */
.ai-card {
    background: linear-gradient(135deg, rgba(0, 229, 255, 0.06), rgba(255, 179, 0, 0.06));
    border: 1px solid rgba(0, 229, 255, 0.2);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    position: relative;
    overflow: hidden;
}
.ai-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 229, 255, 0.03) 0%, transparent 70%);
    animation: rotate-bg 20s linear infinite;
    pointer-events: none;
}
@keyframes rotate-bg {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
.ai-card > * { position: relative; z-index: 1; }

/* ═══════════════════════════════════════════════════════════
   MVP CARD
   ═══════════════════════════════════════════════════════════ */
.mvp-card {
    background: linear-gradient(135deg, rgba(255, 215, 0, 0.08), rgba(255, 160, 0, 0.06));
    border: 1px solid rgba(255, 215, 0, 0.3);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.mvp-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, transparent 40%, rgba(255, 215, 0, 0.04) 100%);
    pointer-events: none;
}
.mvp-crown { font-size: clamp(2rem, 6vw, 2.8rem); }
.mvp-name {
    font-family: var(--font-heading);
    font-size: clamp(1.2rem, 4vw, 1.7rem);
    font-weight: 800;
    background: linear-gradient(135deg, #FFD700, #FFA000);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: var(--spacing-xs);
}
.mvp-subtitle {
    color: var(--muted);
    font-size: clamp(0.75rem, 2vw, 0.85rem);
    margin-top: var(--spacing-xs);
}

/* ═══════════════════════════════════════════════════════════
   PODIUM CARD
   ═══════════════════════════════════════════════════════════ */
.podium-card {
    background: var(--glass);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg) var(--spacing-md);
    text-align: center;
    transition: transform var(--transition), box-shadow var(--transition);
}
.podium-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--glow-strong);
}
.podium-medal { font-size: clamp(1.6rem, 5vw, 2.2rem); }
.podium-name {
    font-family: var(--font-heading);
    font-size: clamp(0.9rem, 2.5vw, 1.2rem);
    font-weight: 700;
    color: var(--text);
    margin-top: var(--spacing-xs);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.podium-dept {
    color: var(--muted);
    font-size: clamp(0.6rem, 1.5vw, 0.75rem);
    margin-top: 2px;
}
.podium-stats {
    margin-top: var(--spacing-sm);
    font-size: clamp(0.75rem, 2vw, 0.85rem);
}

/* ═══════════════════════════════════════════════════════════
   DEMO MODE BADGE
   ═══════════════════════════════════════════════════════════ */
.demo-badge {
    background: rgba(255, 179, 0, 0.08);
    border: 1px solid rgba(255, 179, 0, 0.25);
    border-radius: var(--radius-md);
    padding: 0.65rem var(--spacing-md);
    text-align: center;
    margin-top: var(--spacing-sm);
}
.demo-badge-title {
    color: var(--amber);
    font-weight: 600;
    font-size: 0.85rem;
}
.demo-badge-desc {
    color: var(--muted);
    font-size: 0.7rem;
    margin-top: 2px;
    line-height: 1.4;
}

/* ═══════════════════════════════════════════════════════════
   SIDEBAR BRAND (Mobile)
   ═══════════════════════════════════════════════════════════ */
.sidebar-brand {
    text-align: center;
    padding: var(--spacing-lg) 0 var(--spacing-md);
}
.sidebar-brand-name {
    font-family: var(--font-heading);
    font-size: clamp(1.4rem, 4vw, 1.8rem);
    font-weight: 800;
    background: linear-gradient(135deg, var(--cyan), var(--amber));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sidebar-brand-sub {
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 2px;
}

/* ═══════════════════════════════════════════════════════════
   SETUP INSTRUCTIONS CARD
   ═══════════════════════════════════════════════════════════ */
.instructions-card {
    color: var(--muted);
    font-size: clamp(0.72rem, 1.8vw, 0.82rem);
    line-height: 1.7;
}
.instructions-card code {
    background: rgba(0, 229, 255, 0.08);
    color: var(--cyan);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 0.85em;
}

/* ═══════════════════════════════════════════════════════════
   EMPTY STATE
   ═══════════════════════════════════════════════════════════ */
.empty-state {
    text-align: center;
    padding: var(--spacing-xl) var(--spacing-md);
    color: var(--muted);
}
.empty-state-icon {
    font-size: clamp(2rem, 6vw, 3rem);
    margin-bottom: var(--spacing-sm);
    opacity: 0.5;
}
.empty-state-text {
    font-size: clamp(0.85rem, 2vw, 1rem);
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE: MOBILE SMALL (≤ 480px)
   iPhone SE, iPhone Mini, small Androids
   ═══════════════════════════════════════════════════════════ */
@media screen and (max-width: 480px) {
    /* Streamlit main content padding */
    [data-testid="stAppViewContainer"] > section > div {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }

    .glass-card {
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
    }

    .metric-card {
        padding: var(--spacing-sm) var(--spacing-md);
        min-height: 72px;
        border-radius: var(--radius-sm);
    }

    .match-card {
        padding: var(--spacing-sm) var(--spacing-md);
        flex-direction: column;
        align-items: flex-start;
        gap: var(--spacing-xs);
    }

    /* Stack score +/- buttons better */
    .stButton > button {
        min-height: 48px !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 0.6rem !important;
    }

    .leaderboard-table td,
    .leaderboard-table th {
        padding: 0.4rem 0.5rem;
    }

    .ai-card {
        padding: var(--spacing-md);
    }
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE: MOBILE MEDIUM (≤ 768px)
   iPhone 12-16, iPhone Plus, Samsung Galaxy, Pixel
   ═══════════════════════════════════════════════════════════ */
@media screen and (max-width: 768px) {
    /* Streamlit columns should stack on mobile */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    /* But allow metric cards to be 2-up */
    .metric-row [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 calc(50% - 0.5rem) !important;
        min-width: calc(50% - 0.5rem) !important;
    }

    .glass-card {
        padding: var(--spacing-md) var(--spacing-md);
        margin-bottom: 0.75rem;
    }

    /* Sidebar collapses on mobile by default (Streamlit handles this) */
    [data-testid="stSidebar"] {
        min-width: 260px !important;
    }

    /* Hide overflow on page titles */
    .page-title {
        word-break: break-word;
    }

    /* Touch-friendly tap targets (UUPM: 44px minimum) */
    .stButton > button,
    .stTabs [data-baseweb="tab"],
    input, textarea, select {
        min-height: 44px !important;
    }
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE: TABLET (≤ 1024px)
   iPad, iPad Air, Android tablets
   ═══════════════════════════════════════════════════════════ */
@media screen and (min-width: 769px) and (max-width: 1024px) {
    [data-testid="stAppViewContainer"] > section > div {
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* Allow 2 columns on tablets */
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        flex: 1 1 calc(50% - 0.5rem) !important;
        min-width: calc(50% - 0.5rem) !important;
    }
}

/* ═══════════════════════════════════════════════════════════
   RESPONSIVE: DESKTOP LARGE (≥ 1440px)
   ═══════════════════════════════════════════════════════════ */
@media screen and (min-width: 1440px) {
    .glass-card {
        padding: var(--spacing-xl);
    }

    .metric-card {
        min-height: 100px;
    }
}

/* ═══════════════════════════════════════════════════════════
   SAFE AREA (Notch / Dynamic Island support)
   ═══════════════════════════════════════════════════════════ */
@supports (padding: env(safe-area-inset-top)) {
    [data-testid="stAppViewContainer"] {
        padding-top: env(safe-area-inset-top);
        padding-bottom: env(safe-area-inset-bottom);
        padding-left: env(safe-area-inset-left);
        padding-right: env(safe-area-inset-right);
    }
}

/* ═══════════════════════════════════════════════════════════
   HIGH CONTRAST / ACCESSIBILITY
   ═══════════════════════════════════════════════════════════ */
@media (forced-colors: active) {
    .glass-card, .metric-card, .match-card, .ai-card {
        border: 2px solid CanvasText;
    }
    .status-badge {
        border: 1px solid CanvasText;
    }
}

/* ═══════════════════════════════════════════════════════════
   SELECTION COLOR
   ═══════════════════════════════════════════════════════════ */
::selection {
    background: rgba(0, 229, 255, 0.25);
    color: var(--text);
}

/* ═══════════════════════════════════════════════════════════
   SCROLLBAR (Desktop)
   ═══════════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(0, 229, 255, 0.15);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 255, 0.3); }

</style>
"""


def inject_css():
    """Call this once at the top of app.py to inject all custom styles."""
    import streamlit as st
    st.markdown(GOOGLE_FONTS, unsafe_allow_html=True)
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
