# College Life App

A Kivy desktop app for helping college students manage daily routines, budgets, campus resources, social events, focus sessions, and persistent app preferences.

## Technology Versions

- Python: 3.11 or newer
- Tested with Python: 3.12.13
- Kivy: 2.3.0

## Build and Run

1. Open a terminal in the project root.
2. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies.

```powershell
pip install -r requirements.txt
```

4. Run the application.

```powershell
python main.py
```

On Windows, you can also use the provided helper script:

```powershell
.\run_app.ps1
```

## Project Files

- `main.py`: app startup, theme state, screen registration, and responsive scaling
- `screens/`: Python behavior for each app screen
- `kv/`: Kivy layout files for each app screen
- `app/widgets/`: custom reusable widgets, including the pie chart, bottom-nav icons, and auto-fitting action buttons
- `services/`: local data models and JSON persistence
- `assets/`: image assets used by the UI
- `data/app_state.json`: local persistent app data

## Implemented Features

- Dashboard page with today's schedule, budget summary, upcoming events, and a quick focus timer
- Weekly Routine page for adding, viewing, categorizing, and deleting tasks by weekday
- Budgeting page with budget limit, transaction history, category summary, progress bar, and pie chart visualization
- Social Hub page with campus event feed, event creation, event details, and category filters
- Campus Resources page with searchable campus support contacts and resource details
- Settings page with persistent dark mode, font size scaling, and app reset/data management

## Persistent Data

The app stores data locally in `data/app_state.json`. This includes tasks, transactions, events, resources, budget limit, dark mode, font size settings, and other app preferences. The Settings page can reset this stored data.

## Notes

- The app is local/offline and does not require a network connection.
- If the UI appears unusually large or small, adjust the window size or the font size slider in Settings.
