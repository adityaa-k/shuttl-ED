"""
shuttl-ED — AI Referee (Gemini 1.5 Flash)
Handles smart match rescheduling via natural-language constraints.
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are the shuttl-ED AI Referee — an intelligent match scheduler for an internal company badminton tournament.

You will be given:
1. A JSON list of upcoming matches, each with: Match_ID, Team_A, Team_B, Status.
2. A natural-language constraint from the admin.

Your job:
- Reorder, postpone, or prioritize matches based on the constraint.
- Return ONLY a valid JSON array of the reordered matches.
- Preserve the original match objects — just change the order.
- If a match should be removed from the queue, exclude it.
- If you need to add a note, add a "Note" field to the match object.

Respond ONLY with the JSON array. No explanation, no markdown fences."""


def solve_scheduling_conflict(current_queue: list[dict], constraint_string: str) -> list[dict]:
    """
    Use Gemini 1.5 Flash to reorder the match queue based on an admin constraint.
    
    Args:
        current_queue: List of match dicts with Match_ID, Team_A, Team_B, Status.
        constraint_string: Natural-language instruction from the admin.
    
    Returns:
        Reordered list of match dicts, or the original queue on failure.
    """
    api_key = os.getenv("GEMINI_API_KEY", "")

    if not api_key:
        return current_queue  # Graceful fallback

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        user_message = (
            f"Current match queue:\n{json.dumps(current_queue, indent=2)}\n\n"
            f"Admin instruction: {constraint_string}"
        )

        response = model.generate_content(
            [
                {"role": "user", "parts": [{"text": SYSTEM_PROMPT}]},
                {"role": "model", "parts": [{"text": "Understood. Send me the match queue and constraint."}]},
                {"role": "user", "parts": [{"text": user_message}]},
            ]
        )

        raw = response.text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            if raw.endswith("```"):
                raw = raw[:-3]
            raw = raw.strip()

        reordered = json.loads(raw)
        if isinstance(reordered, list):
            return reordered
        return current_queue

    except Exception:
        return current_queue


def get_demo_reschedule(current_queue: list[dict], constraint_string: str) -> list[dict]:
    """
    Demo-mode rescheduling: a simple heuristic that simulates AI behavior.
    Useful when no Gemini API key is available.
    """
    constraint = constraint_string.lower()

    if "end" in constraint or "last" in constraint:
        # Move mentioned player's matches to the end
        words = constraint_string.split()
        names = {m["Team_A"] for m in current_queue} | {m["Team_B"] for m in current_queue}
        mentioned = [w for w in words if w.capitalize() in {n.split()[0] for n in names}]
        
        if mentioned:
            target_first = mentioned[0].capitalize()
            front = []
            back = []
            for m in current_queue:
                if target_first in m["Team_A"] or target_first in m["Team_B"]:
                    m["Note"] = f"Moved to end (player unavailable)"
                    back.append(m)
                else:
                    front.append(m)
            return front + back

    if "prioritize" in constraint or "top" in constraint:
        # Reverse order as a simple "prioritize top" simulation
        return list(reversed(current_queue))

    # Default: no change
    return current_queue
