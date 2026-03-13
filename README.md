# shuttl-ED

**shuttl-ED** is a premium, internal-only company badminton league management application. Built with **Streamlit**, **Google Sheets**, and **Gemini 1.5 Flash**, it provides a seamless and visually stunning experience for tracking matches, leaderboards, and AI-driven rescheduling.

---

## Key Features

### Match Center
- **Setup Matches**: Support for both Singles (1v1) and Doubles (2v2).
- **Player Randomization**: Quickly pick fair matches from the registered player pool.
- **Dual Scoring Modes**:
  - **Live Mode**: A real-time +/- counter for keeping score during the match.
  - **Quick Entry**: Fast-track score entry for completed matches.

### Dynamic Leaderboards
- **Today's MVP**: Highlights the top-performing player of the current day.
- **Hall of Fame**: An all-time leaderboard aggregating wins, points, and matches played from the entire history.
- **Podium View**: Digital awards for the top 3 all-time players.

### AI Referee (Gemini 1.5 Flash)
- **Natural Language Rescheduling**: Admins can provide constraints (e.g., *"Vikram has a meeting in 10 mins"* or *"Prioritize matches with the top players"*) and the AI will automatically reorganize the queue.
- **Intelligent Feedback**: The AI provides notes on why specific matches were moved.

### Secure Admin Panel
- **Password Protected**: The panel is locked behind a password (`ed@admin`) to ensure data integrity.
- **Player Management**: Add new players and departments.
- **Full Match Log**: View the complete history of every match played.
- **System Settings**: Monitor connection status to Google Sheets and Gemini AI.

### Premium UX (UI UX Pro Max)
- **Glassmorphism Design**: A modern, sleek dark theme with frost-glass effects.
- **Mobile-First Responsiveness**: Optimized for every device from iPhone SE to 4K monitors.
- **Micro-Animations**: Smooth transitions and pulsing indicators for live matches.
- **Accessibility**: Support for forced-colors and reduced-motion preferences.

---

## Technical Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database**: [Google Sheets](https://www.google.com/sheets/about/) (via `gspread`)
- **AI Engine**: [Google Gemini 1.5 Flash](https://ai.google.dev/)
- **Styling**: Custom CSS with native JS injections for advanced UI control.
- **Environment**: Python 3.10+

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10 or higher.
- A Google Cloud Project with the **Google Sheets API** and **Google Drive API** enabled.
- A **Service Account** key (`credentials.json`) from Google Cloud Console.
- A Gemini API Key from [AI Studio](https://aistudio.google.com/).

### 2. Local Setup
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/adityaa-k/shuttl-ED.git
   cd shuttl-ED
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Create a `.env` file in the root directory:
     ```env
     GOOGLE_SHEET_ID=your_google_sheet_id_here
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
   - Place your `credentials.json` file in the root directory.

4. **Run the App**:
   ```bash
   python -m streamlit run app.py
   ```

---

## Deployment (Streamlit Community Cloud)

1. **Push to GitHub**: Ensure your `.env` and `credentials.json` are **NOT** checked into Git.
2. **Deploy on Streamlit**:
   - Connect your GitHub repo to [Streamlit Cloud](https://share.streamlit.io/).
   - Go to **Settings > Secrets** in the Streamlit Dashboard.
   - Paste your `.env` values and the content of your `credentials.json` into the secrets area.

---

## Security
- **Admin Password**: `moodle`
- **Secrets Management**: Ensure all API keys and credentials are kept in `.env` or Streamlit Secrets.

---

## Contributing
This is an internal company tool. For feature requests or bug reports, please contact the internal IT/Badminton committee.

---

*Made for the company badminton community.*
