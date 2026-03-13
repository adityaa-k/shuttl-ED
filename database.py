"""
shuttl-ED — Database Layer
Provides SheetDB (Google Sheets) and DemoDB (in-memory fallback).
"""

import os
import uuid
from datetime import datetime, date

import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────────────────
# Google Sheets Database
# ──────────────────────────────────────────────────────────

class SheetDB:
    """CRUD operations backed by a Google Sheet with Players & Match_Log tabs."""

    def __init__(self, sheet_id: str, creds_path: str = "credentials.json"):
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(sheet_id)
        self._players_ws = self.sheet.worksheet("Players")
        self._match_ws = self.sheet.worksheet("Match_Log")

    # ── Players ────────────────────────────────────────────
    def get_players(self) -> pd.DataFrame:
        data = self._players_ws.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Name", "Department", "All_Time_Wins", "All_Time_Points", "Matches_Played"])
        return pd.DataFrame(data)

    def add_player(self, name: str, department: str) -> None:
        self._players_ws.append_row([name, department, 0, 0, 0])

    def _update_player_stats(self, winner_name: str, score: int):
        """Increment wins and points for the winner."""
        players = self.get_players()
        if winner_name in players["Name"].values:
            idx = players[players["Name"] == winner_name].index[0]
            row_num = idx + 2  # 1-indexed + header
            current = self._players_ws.row_values(row_num)
            wins = int(current[2]) + 1
            pts = int(current[3]) + score
            played = int(current[4]) + 1
            self._players_ws.update_cell(row_num, 3, wins)
            self._players_ws.update_cell(row_num, 4, pts)
            self._players_ws.update_cell(row_num, 5, played)

    # ── Matches ────────────────────────────────────────────
    def get_matches(self) -> pd.DataFrame:
        data = self._match_ws.get_all_records()
        if not data:
            return pd.DataFrame(columns=["Date", "Match_ID", "Team_A", "Team_B", "Score_A", "Score_B", "Winner", "Status"])
        return pd.DataFrame(data)

    def get_todays_matches(self) -> pd.DataFrame:
        df = self.get_matches()
        if df.empty:
            return df
        today_str = date.today().isoformat()
        return df[df["Date"] == today_str]

    def add_match(self, team_a: str, team_b: str) -> str:
        match_id = str(uuid.uuid4())[:8].upper()
        today = date.today().isoformat()
        self._match_ws.append_row([today, match_id, team_a, team_b, 0, 0, "", "Scheduled"])
        return match_id

    def update_score(self, match_id: str, score_a: int, score_b: int, status: str = "Live"):
        matches = self.get_matches()
        if match_id not in matches["Match_ID"].values:
            return
        idx = matches[matches["Match_ID"] == match_id].index[0]
        row_num = idx + 2
        winner = ""
        if status == "Completed":
            team_a = matches.loc[idx, "Team_A"]
            team_b = matches.loc[idx, "Team_B"]
            winner = team_a if score_a > score_b else team_b
            self._update_player_stats(winner, max(score_a, score_b))
        self._match_ws.update_cell(row_num, 5, score_a)
        self._match_ws.update_cell(row_num, 6, score_b)
        self._match_ws.update_cell(row_num, 7, winner)
        self._match_ws.update_cell(row_num, 8, status)

    def get_leaderboard(self) -> pd.DataFrame:
        players = self.get_players()
        if players.empty:
            return players
        return players.sort_values("All_Time_Wins", ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────────────────
# Demo (In-Memory) Database
# ──────────────────────────────────────────────────────────

_DEMO_PLAYERS = [
    {"Name": "Arjun Mehta",     "Department": "Engineering", "All_Time_Wins": 12, "All_Time_Points": 247, "Matches_Played": 18},
    {"Name": "Priya Sharma",    "Department": "Design",      "All_Time_Wins": 15, "All_Time_Points": 310, "Matches_Played": 20},
    {"Name": "Rohan Gupta",     "Department": "Marketing",   "All_Time_Wins": 8,  "All_Time_Points": 168, "Matches_Played": 14},
    {"Name": "Sneha Iyer",      "Department": "Engineering", "All_Time_Wins": 10, "All_Time_Points": 205, "Matches_Played": 16},
    {"Name": "Vikram Patel",    "Department": "Product",     "All_Time_Wins": 6,  "All_Time_Points": 130, "Matches_Played": 11},
    {"Name": "Ananya Reddy",    "Department": "HR",          "All_Time_Wins": 9,  "All_Time_Points": 189, "Matches_Played": 15},
    {"Name": "Karan Singh",     "Department": "Engineering", "All_Time_Wins": 11, "All_Time_Points": 224, "Matches_Played": 17},
    {"Name": "Meera Joshi",     "Department": "Finance",     "All_Time_Wins": 7,  "All_Time_Points": 145, "Matches_Played": 12},
]

_DEMO_MATCHES = [
    {"Date": date.today().isoformat(), "Match_ID": "SF-001", "Team_A": "Arjun Mehta",  "Team_B": "Priya Sharma",  "Score_A": 21, "Score_B": 18, "Winner": "Arjun Mehta",  "Status": "Completed"},
    {"Date": date.today().isoformat(), "Match_ID": "SF-002", "Team_A": "Rohan Gupta",  "Team_B": "Sneha Iyer",    "Score_A": 15, "Score_B": 21, "Winner": "Sneha Iyer",   "Status": "Completed"},
    {"Date": date.today().isoformat(), "Match_ID": "SF-003", "Team_A": "Vikram Patel", "Team_B": "Karan Singh",   "Score_A": 0,  "Score_B": 0,  "Winner": "",              "Status": "Scheduled"},
    {"Date": date.today().isoformat(), "Match_ID": "SF-004", "Team_A": "Ananya Reddy", "Team_B": "Meera Joshi",   "Score_A": 0,  "Score_B": 0,  "Winner": "",              "Status": "Scheduled"},
]


class DemoDB:
    """In-memory demo database using Pandas DataFrames in session_state."""

    def __init__(self):
        if "demo_players" not in st.session_state:
            st.session_state.demo_players = pd.DataFrame(_DEMO_PLAYERS)
        if "demo_matches" not in st.session_state:
            st.session_state.demo_matches = pd.DataFrame(_DEMO_MATCHES)

    # ── Players ────────────────────────────────────────────
    def get_players(self) -> pd.DataFrame:
        return st.session_state.demo_players.copy()

    def add_player(self, name: str, department: str) -> None:
        new = pd.DataFrame([{
            "Name": name, "Department": department,
            "All_Time_Wins": 0, "All_Time_Points": 0, "Matches_Played": 0,
        }])
        st.session_state.demo_players = pd.concat(
            [st.session_state.demo_players, new], ignore_index=True
        )

    # ── Matches ────────────────────────────────────────────
    def get_matches(self) -> pd.DataFrame:
        return st.session_state.demo_matches.copy()

    def get_todays_matches(self) -> pd.DataFrame:
        df = self.get_matches()
        if df.empty:
            return df
        today_str = date.today().isoformat()
        return df[df["Date"] == today_str]

    def add_match(self, team_a: str, team_b: str) -> str:
        match_id = "SF-" + str(uuid.uuid4())[:4].upper()
        today = date.today().isoformat()
        new = pd.DataFrame([{
            "Date": today, "Match_ID": match_id,
            "Team_A": team_a, "Team_B": team_b,
            "Score_A": 0, "Score_B": 0, "Winner": "", "Status": "Scheduled",
        }])
        st.session_state.demo_matches = pd.concat(
            [st.session_state.demo_matches, new], ignore_index=True
        )
        return match_id

    def update_score(self, match_id: str, score_a: int, score_b: int, status: str = "Live"):
        df = st.session_state.demo_matches
        mask = df["Match_ID"] == match_id
        if not mask.any():
            return
        idx = df[mask].index[0]
        winner = ""
        if status == "Completed":
            winner = df.at[idx, "Team_A"] if score_a > score_b else df.at[idx, "Team_B"]
            # Update player stats
            p = st.session_state.demo_players
            pmask = p["Name"] == winner
            if pmask.any():
                pidx = p[pmask].index[0]
                st.session_state.demo_players.at[pidx, "All_Time_Wins"] += 1
                st.session_state.demo_players.at[pidx, "All_Time_Points"] += max(score_a, score_b)
            # Mark both as played
            for name_col in ["Team_A", "Team_B"]:
                pname = df.at[idx, name_col]
                pm = p["Name"] == pname
                if pm.any():
                    pi = p[pm].index[0]
                    st.session_state.demo_players.at[pi, "Matches_Played"] += 1

        st.session_state.demo_matches.at[idx, "Score_A"] = score_a
        st.session_state.demo_matches.at[idx, "Score_B"] = score_b
        st.session_state.demo_matches.at[idx, "Winner"] = winner
        st.session_state.demo_matches.at[idx, "Status"] = status

    def get_leaderboard(self) -> pd.DataFrame:
        players = self.get_players()
        if players.empty:
            return players
        return players.sort_values("All_Time_Wins", ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────────────────
# Factory
# ──────────────────────────────────────────────────────────

def get_db():
    """Return SheetDB if credentials exist, otherwise DemoDB."""
    from dotenv import load_dotenv
    load_dotenv()

    creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "")

    if os.path.exists(creds_path) and sheet_id:
        try:
            return SheetDB(sheet_id, creds_path)
        except Exception as e:
            st.warning(f"⚠️ Could not connect to Google Sheets: {e}. Using demo mode.")
            return DemoDB()
    else:
        return DemoDB()
