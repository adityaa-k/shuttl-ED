"""
shuttl-ED — Internal Company Badminton App
Main Streamlit Application (v2 — Mobile-First + UUPM Optimized)
"""

import random
from datetime import date

import pandas as pd
import streamlit as st

from styles import inject_css
from database import get_db
from referee import solve_scheduling_conflict, get_demo_reschedule

# ──────────────────────────────────────────────────────────
# Page Config & Branding
# ──────────────────────────────────────────────────────────

st.set_page_config(
    page_title="shuttl-ED",
    page_icon="🏸",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ── Sidebar toggle fix (always-visible cyan pill) ──────────
import streamlit.components.v1 as _components
_components.html("""
<script>
(function() {
    function fixSidebarToggle() {
        // Walk up into the parent frame since components run in an iframe
        var doc = window.parent.document;

        // Try multiple known selectors across Streamlit versions
        var selectors = [
            '[data-testid="collapsedControl"]',
            '[data-testid="stSidebarCollapsedControl"]',
            'button[aria-label="Open sidebar"]',
            'button[aria-label="Show sidebar navigation"]',
        ];

        var btn = null;
        for (var i = 0; i < selectors.length; i++) {
            btn = doc.querySelector(selectors[i]);
            if (btn) break;
        }

        // Fallback: find any small button at x < 40px in parent
        if (!btn) {
            var allBtns = doc.querySelectorAll('button');
            for (var j = 0; j < allBtns.length; j++) {
                var r = allBtns[j].getBoundingClientRect();
                if (r.left < 40 && r.width > 0 && r.width < 60) {
                    btn = allBtns[j];
                    break;
                }
            }
        }

        if (btn) {
            btn.style.cssText = [
                'display:flex',
                'visibility:visible',
                'opacity:1',
                'pointer-events:all',
                'background:linear-gradient(135deg,#00E5FF,#00B8D4)',
                'border-radius:0 12px 12px 0',
                'border:none',
                'outline:none',
                'box-shadow:2px 0 20px rgba(0,229,255,0.5)',
                'width:32px',
                'height:56px',
                'align-items:center',
                'justify-content:center',
                'cursor:pointer',
                'position:fixed',
                'left:0',
                'top:50%',
                'transform:translateY(-50%)',
                'z-index:2147483647',
            ].join(';');
            btn.querySelectorAll('svg,path,polyline,line').forEach(function(el){
                el.setAttribute('stroke','#0A1628');
                el.setAttribute('fill','none');
                el.style.stroke = '#0A1628';
            });
        }
    }

    fixSidebarToggle();
    setInterval(fixSidebarToggle, 600);
})();
</script>
""", height=0)


# ──────────────────────────────────────────────────────────
# Initialize Database
# ──────────────────────────────────────────────────────────

db = get_db()

# ──────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────

def render_metric(label: str, value, icon: str = ""):
    """Render a styled metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{icon} {value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_title(title: str, subtitle: str = ""):
    """Render a branded page title."""
    st.markdown(f'<div class="page-title fade-in">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)


def rank_badge(rank: int) -> str:
    if rank == 1:
        return '<span class="rank-badge rank-1">1</span>'
    elif rank == 2:
        return '<span class="rank-badge rank-2">2</span>'
    elif rank == 3:
        return '<span class="rank-badge rank-3">3</span>'
    return f'<span class="rank-badge rank-default">{rank}</span>'


def status_badge(status: str) -> str:
    cls = {
        "Live": "status-live",
        "Completed": "status-completed",
        "Scheduled": "status-scheduled",
    }.get(status, "status-scheduled")
    return f'<span class="status-badge {cls}">{status}</span>'


def render_table(headers: list[str], rows_html: str):
    """Wrap a table in a responsive scrollable container."""
    header_html = "".join(f"<th>{h}</th>" for h in headers)
    st.markdown(f"""
    <div class="table-wrapper">
        <table class="leaderboard-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────
# Sidebar Navigation
# ──────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-name">🏸 shuttl-ED</div>
        <div class="sidebar-brand-sub">Internal Badminton League</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["Play", "Leaderboard", "AI Referee", "Admin"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # Demo mode indicator
    from database import DemoDB
    if isinstance(db, DemoDB):
        st.markdown("""
        <div class="demo-badge">
            <div class="demo-badge-title">Demo Mode</div>
            <div class="demo-badge-desc">Using in-memory data.<br>Add credentials for Google Sheets.</div>
        </div>
        """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: PLAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if page == "Play":
    render_title("Match Center", "Set up matches, keep score, and dominate the court.")

    players_df = db.get_players()
    player_names = players_df["Name"].tolist() if not players_df.empty else []

    # ── Quick Stats ────────────────────────────────────────
    today_matches = db.get_todays_matches()
    completed = today_matches[today_matches["Status"] == "Completed"] if not today_matches.empty else pd.DataFrame()
    live = today_matches[today_matches["Status"] == "Live"] if not today_matches.empty else pd.DataFrame()
    scheduled = today_matches[today_matches["Status"] == "Scheduled"] if not today_matches.empty else pd.DataFrame()

    # 2x2 grid on mobile, 4-col on desktop
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        render_metric("Total Today", len(today_matches))
    with r1c2:
        render_metric("Completed", len(completed))

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        render_metric("Live Now", len(live))
    with r2c2:
        render_metric("Upcoming", len(scheduled))

    st.markdown("---")

    # ── Match Setup ────────────────────────────────────────
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    st.markdown("#### New Match Setup")

    match_mode = st.radio("Match Type", ["Singles (1v1)", "Doubles (2v2)"], horizontal=True)
    required_count = 2 if "Singles" in match_mode else 4

    if st.button("Randomize Players", use_container_width=True):
        if len(player_names) >= required_count:
            picks = random.sample(player_names, required_count)
            st.session_state["random_picks"] = picks
        else:
            st.warning(f"Need at least {required_count} players to randomize.")

    # Player selection
    if "Singles" in match_mode:
        default_a, default_b = [], []
        if "random_picks" in st.session_state and len(st.session_state["random_picks"]) >= 2:
            default_a = [st.session_state["random_picks"][0]]
            default_b = [st.session_state["random_picks"][1]]

        team_a_sel = st.multiselect("🔵 Team A", player_names, default=default_a, max_selections=1, key="ta_s")
        team_b_sel = st.multiselect("🟡 Team B", player_names, default=default_b, max_selections=1, key="tb_s")

        team_a_str = team_a_sel[0] if team_a_sel else ""
        team_b_str = team_b_sel[0] if team_b_sel else ""
    else:
        default_a, default_b = [], []
        if "random_picks" in st.session_state and len(st.session_state["random_picks"]) >= 4:
            default_a = st.session_state["random_picks"][:2]
            default_b = st.session_state["random_picks"][2:4]

        team_a_sel = st.multiselect("Team A", player_names, default=default_a, max_selections=2, key="ta_d")
        team_b_sel = st.multiselect("Team B", player_names, default=default_b, max_selections=2, key="tb_d")

        team_a_str = " & ".join(team_a_sel) if team_a_sel else ""
        team_b_str = " & ".join(team_b_sel) if team_b_sel else ""

    if st.button("Create Match", type="primary", use_container_width=True):
        if team_a_str and team_b_str:
            overlap = set(team_a_sel) & set(team_b_sel)
            if overlap:
                st.error(f"Player(s) **{', '.join(overlap)}** cannot be on both teams!")
            else:
                mid = db.add_match(team_a_str, team_b_str)
                st.success(f"Match **{mid}** created! {team_a_str} vs {team_b_str}")
                if "random_picks" in st.session_state:
                    del st.session_state["random_picks"]
                st.rerun()
        else:
            st.warning("Select players for both teams first.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Scoring Section ────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Score Matches")

    active_matches = today_matches[today_matches["Status"].isin(["Scheduled", "Live"])] if not today_matches.empty else pd.DataFrame()

    if active_matches.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-text">No active matches. Create one above!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        score_tab1, score_tab2 = st.tabs(["Live Mode", "Quick Entry"])

        with score_tab1:
            for idx, match in active_matches.iterrows():
                mid = match["Match_ID"]
                st.markdown(f'<div class="glass-card fade-in">', unsafe_allow_html=True)

                # Match header
                st.markdown(
                    f'**{mid}** — {match["Team_A"]} vs {match["Team_B"]} '
                    f'{status_badge(match["Status"])}',
                    unsafe_allow_html=True,
                )

                # Score state
                sa_key = f"live_sa_{mid}"
                sb_key = f"live_sb_{mid}"
                if sa_key not in st.session_state:
                    st.session_state[sa_key] = int(match["Score_A"])
                if sb_key not in st.session_state:
                    st.session_state[sb_key] = int(match["Score_B"])

                # Score display (always visible, responsive via clamp)
                st.markdown(
                    f'<div class="score-display">'
                    f'<span class="score-team-a">{st.session_state[sa_key]}</span>'
                    f'<span class="score-vs">—</span>'
                    f'<span class="score-team-b">{st.session_state[sb_key]}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Team labels
                lc1, lc2 = st.columns(2)
                with lc1:
                    st.markdown(f'<div class="team-label team-label-a">{match["Team_A"]}</div>', unsafe_allow_html=True)
                with lc2:
                    st.markdown(f'<div class="team-label team-label-b">{match["Team_B"]}</div>', unsafe_allow_html=True)

                # Score buttons — 2 columns, stacked for mobile friendliness
                bc_a1, bc_a2 = st.columns(2)
                with bc_a1:
                    if st.button("Score Team A", key=f"pa_{mid}", use_container_width=True):
                        st.session_state[sa_key] += 1
                        st.rerun()
                with bc_a2:
                    if st.button("Minus Team A", key=f"ma_{mid}", use_container_width=True):
                        if st.session_state[sa_key] > 0:
                            st.session_state[sa_key] -= 1
                            st.rerun()

                bc_b1, bc_b2 = st.columns(2)
                with bc_b1:
                    if st.button("Score Team B", key=f"pb_{mid}", use_container_width=True):
                        st.session_state[sb_key] += 1
                        st.rerun()
                with bc_b2:
                    if st.button("Minus Team B", key=f"mb_{mid}", use_container_width=True):
                        if st.session_state[sb_key] > 0:
                            st.session_state[sb_key] -= 1
                            st.rerun()

                st.markdown("---")

                # Action buttons
                ac1, ac2 = st.columns(2)
                with ac1:
                    if st.button("Save Score", key=f"upd_{mid}", use_container_width=True):
                        db.update_score(mid, st.session_state[sa_key], st.session_state[sb_key], "Live")
                        st.success("Score updated!")
                        st.rerun()
                with ac2:
                    if st.button("End Match", key=f"end_{mid}", type="primary", use_container_width=True):
                        db.update_score(mid, st.session_state[sa_key], st.session_state[sb_key], "Completed")
                        st.success("Match completed!")
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        with score_tab2:
            st.markdown("Enter final scores directly:")
            for idx, match in active_matches.iterrows():
                mid = match["Match_ID"]
                st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(f"**{mid}** — {match['Team_A']} vs {match['Team_B']}")

                q_sa = st.number_input("Team A Score", min_value=0, max_value=30, value=0, key=f"q_sa_{mid}")
                q_sb = st.number_input("Team B Score", min_value=0, max_value=30, value=0, key=f"q_sb_{mid}")

                if st.button("Submit Score", key=f"qsub_{mid}", type="primary", use_container_width=True):
                    db.update_score(mid, q_sa, q_sb, "Completed")
                    st.success(f"Match {mid} recorded!")
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LEADERBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "Leaderboard":
    render_title("Leaderboard", "See who rules the court — today and all-time.")

    lb_tab1, lb_tab2 = st.tabs(["Today's MVP", "Hall of Fame"])

    with lb_tab1:
        today_matches = db.get_todays_matches()
        completed_today = today_matches[today_matches["Status"] == "Completed"] if not today_matches.empty else pd.DataFrame()

        if completed_today.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-text">No completed matches today. Get playing!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Build today's leaderboard
            wins = {}
            points = {}
            for _, m in completed_today.iterrows():
                w = m["Winner"]
                if w:
                    wins[w] = wins.get(w, 0) + 1
                    s = max(int(m["Score_A"]), int(m["Score_B"]))
                    points[w] = points.get(w, 0) + s

            today_lb = pd.DataFrame([
                {"Name": k, "Wins": v, "Points": points.get(k, 0)}
                for k, v in wins.items()
            ]).sort_values("Wins", ascending=False).reset_index(drop=True)

            # MVP highlight
            if not today_lb.empty:
                mvp = today_lb.iloc[0]
                wins_text = f"{mvp['Wins']} win{'s' if mvp['Wins'] > 1 else ''}"
                st.markdown(f"""
                <div class="mvp-card fade-in">
                    <div class="mvp-name">{mvp["Name"]}</div>
                    <div class="mvp-subtitle">Today's MVP — {wins_text}, {mvp["Points"]} pts</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("&nbsp;", unsafe_allow_html=True)

            # Table
            rows = ""
            for i, row in today_lb.iterrows():
                rows += f"""
                <tr>
                    <td>{rank_badge(i + 1)}</td>
                    <td style="font-weight:600;">{row["Name"]}</td>
                    <td style="color:var(--cyan); font-weight:700;">{row["Wins"]}</td>
                    <td style="color:var(--amber); font-weight:700;">{row["Points"]}</td>
                </tr>"""

            render_table(["Rank", "Player", "Wins", "Points"], rows)

    with lb_tab2:
        leaderboard = db.get_leaderboard()
        if leaderboard.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-text">No players registered yet.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Top 3 podium
            top3 = leaderboard.head(3)
            display_order = [1, 0, 2] if len(top3) >= 3 else list(range(len(top3)))

            podium_cols = st.columns(min(len(top3), 3))
            for col_idx, player_idx in enumerate(display_order):
                if player_idx < len(top3):
                    p = top3.iloc[player_idx]
                    medals = ["🥇", "🥈", "🥉"]
                    with podium_cols[col_idx]:
                        st.markdown(f"""
                        <div class="podium-card fade-in">
                            <div class="podium-name">{p["Name"]}</div>
                            <div class="podium-dept">{p["Department"]}</div>
                            <div class="podium-stats">
                                <span style="color:var(--cyan); font-weight:700;">{p["All_Time_Wins"]}W</span>
                                <span style="color:var(--muted);"> · </span>
                                <span style="color:var(--amber); font-weight:700;">{p["All_Time_Points"]}pts</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("&nbsp;", unsafe_allow_html=True)

            # Full table
            rows = ""
            for i, row in leaderboard.iterrows():
                rows += f"""
                <tr>
                    <td>{rank_badge(i + 1)}</td>
                    <td style="font-weight:600;">{row["Name"]}</td>
                    <td style="color:var(--muted);">{row["Department"]}</td>
                    <td style="color:var(--cyan); font-weight:700;">{row["All_Time_Wins"]}</td>
                    <td style="color:var(--amber); font-weight:700;">{row["All_Time_Points"]}</td>
                    <td>{row["Matches_Played"]}</td>
                </tr>"""

            render_table(["Rank", "Player", "Dept", "Wins", "Points", "Played"], rows)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: AI REFEREE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "🤖 AI Referee":
    render_title("AI Referee", "Smart match rescheduling powered by Gemini 1.5 Flash")

    st.markdown("""
    <div class="ai-card fade-in">
        <div style="font-family:var(--font-heading); font-size:clamp(1rem, 3vw, 1.3rem); font-weight:700; color:var(--cyan);">
            Intelligent Match Scheduling
        </div>
        <div style="color:var(--muted); font-size:clamp(0.75rem, 2vw, 0.85rem); margin-top:0.3rem; line-height:1.5;">
            Tell the AI Referee about constraints — player availability, time limits, or priorities —
            and it will reorganize the match queue automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("&nbsp;", unsafe_allow_html=True)

    # Current Queue
    today_matches = db.get_todays_matches()
    pending = today_matches[today_matches["Status"].isin(["Scheduled", "Live"])] if not today_matches.empty else pd.DataFrame()

    st.markdown("#### Current Match Queue")
    if pending.empty:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-text">No pending matches in the queue.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, (_, match) in enumerate(pending.iterrows()):
            st.markdown(f"""
            <div class="match-card fade-in">
                <div class="match-info">
                    <span style="color:var(--muted); font-weight:600;">#{i+1}</span>&nbsp;&nbsp;
                    <span style="font-weight:600;">{match["Team_A"]}</span>
                    <span style="color:var(--muted);"> vs </span>
                    <span style="font-weight:600;">{match["Team_B"]}</span>
                </div>
                <div>{status_badge(match["Status"])}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("&nbsp;", unsafe_allow_html=True)

    # Constraint input
    st.markdown("#### Instruction")
    constraint = st.text_area(
        "Tell the AI Referee what to do...",
        placeholder='e.g. "Vikram is in a meeting, move his matches to the end" or "We only have 20 mins, prioritize top players"',
        height=100,
        label_visibility="collapsed",
    )

    if st.button("Reschedule Now", type="primary", use_container_width=True):
        if not constraint.strip():
            st.warning("Please type an instruction first.")
        elif pending.empty:
            st.warning("No pending matches to reschedule.")
        else:
            with st.spinner("AI Referee is thinking..."):
                queue = pending[["Match_ID", "Team_A", "Team_B", "Status"]].to_dict("records")

                import os
                if os.getenv("GEMINI_API_KEY"):
                    result = solve_scheduling_conflict(queue, constraint)
                else:
                    result = get_demo_reschedule(queue, constraint)

            st.markdown("#### Rescheduled Queue")
            for i, match in enumerate(result):
                note = match.get("Note", "")
                note_html = f'<br><span style="color:var(--amber); font-size:0.72rem;">Review: {note}</span>' if note else ""
                st.markdown(f"""
                <div class="match-card fade-in">
                    <div class="match-info">
                        <span style="color:var(--cyan); font-weight:700;">#{i+1}</span>&nbsp;&nbsp;
                        <span style="font-weight:600;">{match.get("Team_A", "?")}</span>
                        <span style="color:var(--muted);"> vs </span>
                        <span style="font-weight:600;">{match.get("Team_B", "?")}</span>
                        {note_html}
                    </div>
                    <div>{status_badge(match.get("Status", "Scheduled"))}</div>
                </div>
                """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: ADMIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "Admin":
    render_title("Admin Panel", "Manage players, matches, and system configuration.")

    # ── Admin Password Check ────────────────────────────────
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("#### Restricted Access")
        password = st.text_input("Enter Admin Password", type="password", placeholder="••••••••")
        
        if st.button("Unlock Panel", type="primary", use_container_width=True):
            if password == "moodle":
                st.session_state["admin_authenticated"] = True
                st.success("Access Granted")
                st.rerun()
            else:
                st.error("Invalid password. Please try again.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()  # Stop rendering the rest of the page if not authenticated

    # ── Authenticated Admin UI ──────────────────────────────
    
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Players", "Match Log", "Settings"])

    with admin_tab1:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("#### Add New Player")

        new_name = st.text_input("Player Name", placeholder="e.g. Rahul Verma")
        new_dept = st.text_input("Department", placeholder="e.g. Engineering")

        if st.button("Add Player", type="primary", use_container_width=True):
            if new_name.strip() and new_dept.strip():
                existing = db.get_players()
                if new_name.strip() in existing["Name"].values:
                    st.error("Player already exists!")
                else:
                    db.add_player(new_name.strip(), new_dept.strip())
                    st.success(f"Added **{new_name.strip()}** from {new_dept.strip()}")
                    st.rerun()
            else:
                st.warning("Please fill in both fields.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Registered players table
        st.markdown("#### Registered Players")
        players = db.get_players()
        if players.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">👥</div>
                <div class="empty-state-text">No players registered.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            rows = ""
            for _, p in players.iterrows():
                rows += f"""
                <tr>
                    <td style="font-weight:600;">{p["Name"]}</td>
                    <td style="color:var(--muted);">{p["Department"]}</td>
                    <td style="color:var(--cyan); font-weight:700;">{p["All_Time_Wins"]}</td>
                    <td style="color:var(--amber); font-weight:700;">{p["All_Time_Points"]}</td>
                    <td>{p["Matches_Played"]}</td>
                </tr>"""

            render_table(["Name", "Department", "Wins", "Points", "Played"], rows)

    with admin_tab2:
        st.markdown("#### Full Match Log")
        all_matches = db.get_matches()
        if all_matches.empty:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-text">No matches recorded yet.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            rows = ""
            for _, m in all_matches.iterrows():
                rows += f"""
                <tr>
                    <td style="color:var(--muted);">{m["Date"]}</td>
                    <td style="font-weight:600; color:var(--cyan);">{m["Match_ID"]}</td>
                    <td>{m["Team_A"]}</td>
                    <td>{m["Team_B"]}</td>
                    <td style="color:var(--cyan); font-weight:700;">{m["Score_A"]}</td>
                    <td style="color:var(--amber); font-weight:700;">{m["Score_B"]}</td>
                    <td style="font-weight:600;">{m["Winner"] if m["Winner"] else "—"}</td>
                    <td>{status_badge(m["Status"])}</td>
                </tr>"""

            render_table(["Date", "ID", "Team A", "Team B", "A", "B", "Winner", "Status"], rows)

    with admin_tab3:
        st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
        st.markdown("#### System Status")

        import os
        sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        gemini_key = os.getenv("GEMINI_API_KEY", "")

        sc1, sc2 = st.columns(2)
        with sc1:
            render_metric("Sheets", "Connected" if sheet_id else "Not Set")
        with sc2:
            render_metric("Gemini", "Connected" if gemini_key else "Not Set")

        st.markdown("&nbsp;", unsafe_allow_html=True)
        st.markdown("""
        <div class="instructions-card">
            <b>Setup Instructions:</b><br>
            1. Place <code>credentials.json</code> (Service Account key) in the project root.<br>
            2. Create a <code>.env</code> file with <code>GOOGLE_SHEET_ID</code> and <code>GEMINI_API_KEY</code>.<br>
            3. Ensure your Google Sheet has <b>Players</b> and <b>Match_Log</b> tabs.<br>
            4. Restart the app to connect.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("&nbsp;", unsafe_allow_html=True)

        # Reset demo data
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### Demo Data")
        st.caption("Reset demo data to defaults (demo mode only).")
        if st.button("Reset Demo Data", use_container_width=True):
            if isinstance(db, DemoDB):
                for key in ["demo_players", "demo_matches"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("Demo data reset!")
                st.rerun()
            else:
                st.warning("This only works in demo mode.")
        st.markdown('</div>', unsafe_allow_html=True)
