# College Life App

A Kivy desktop app for helping college students manage daily routines, budgets, campus resources, social events, focus sessions, and persistent app preferences.

## Technology Versions

- Python: 3.11 or 3.12, official 64-bit CPython recommended
- Tested with Python: 3.12.10
- Kivy: 2.3.0

Avoid Python 3.13 or MSYS2/MinGW Python for this project. If pip cannot find a Kivy wheel, it may try to build Kivy from source and fail while installing build dependencies.

## Build and Run

1. Open a terminal in the project root.
2. Create a virtual environment.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
```

If `py -3.12` is not available, install Python 3.12 from python.org or use Python 3.11.

```powershell
py -3.11 -m venv .venv
```

macOS/Linux:

```bash
python3.12 -m venv .venv
```

3. Activate the virtual environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Run the application.

```powershell
python main.py
```

On Windows PowerShell, you can also use the provided helper script:

```powershell
.\run_app.ps1
```

If activation does not work, run through the virtual environment's Python directly.

Windows:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

macOS/Linux:

```bash
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py
```

## Kivy Install Troubleshooting

If installation fails with a message like `Failed to build kivy` or `installing build dependencies for kivy`, the wrong Python version or Python distribution is usually being used.

Check your Python version:

```powershell
python --version
where python
```

Use official Python 3.11 or 3.12 from python.org, then recreate the virtual environment:

```powershell
Remove-Item .venv -Recurse -Force
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

On Linux/Codespaces, Kivy may also need desktop graphics libraries before it can open a window:

```bash
sudo apt update
sudo apt install -y libgl1 libmtdev1 libsdl2-2.0-0
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
- Codespaces/Linux environments may need extra GUI libraries before Kivy can open a window, such as `libgl1`, `libmtdev1`, and `libsdl2-2.0-0`.
