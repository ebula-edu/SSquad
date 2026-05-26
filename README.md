# SSquad Task Manager

A polished Tkinter desktop task manager for Windows and cross-platform Python environments. It keeps your tasks in JSON, provides a modern dashboard-style UI, and can be packaged into a standalone executable with PyInstaller.

---

## What changed

- Replaced the old command-line workflow with a Tkinter desktop UI.
- Added a cleaner dashboard with stats cards, search, filtering, and a task table.
- Added task creation, editing, completion toggling, and deletion in one workflow.
- Added persistent JSON storage via `task_store.py`.
- Added executable build guidance and a verified Windows build artifact.

---

## Features

- Add, edit, and delete tasks
- Mark tasks as complete or pending
- Search by title or description
- Filter by all, pending, or completed tasks
- View total, pending, completed, and high-priority counts
- Persist data in JSON between sessions
- Build a standalone `.exe` for distribution

---

## Requirements

- Python 3.10 or newer
- Tkinter (included with most Python installations)
- Optional: PyInstaller for creating an executable

To check your Python installation:

```powershell
python --version
```

---

## Project structure

```text
task-manager/
├── app.py               # Tkinter UI entry point
├── task_store.py        # JSON persistence and validation
├── tasks.json            # Default local data file for source runs
└── README.md             # This document
```

---

## Running the app from source

From the repository root:

```powershell
cd task-manager
python app.py
```

### Source-run storage location

When you run the app from source, the data is stored in:

```text
task-manager/tasks.json
```

If that file does not exist, it is created automatically.

---

## How to use the UI

### Create a task

1. Enter a title.
2. Select a priority.
3. Optionally enter a due date in `YYYY-MM-DD` format.
4. Add a short description.
5. Click **Save task**.

### Edit a task

1. Click a row in the task table.
2. Update the form fields.
3. Click **Save task** again.

### Filter and search

- Use the search box to filter by title or description.
- Use the dropdown to switch between **All**, **Pending**, and **Completed**.

### Complete or delete

- Select a task and click **Toggle complete**.
- Select a task and click **Delete task** to confirm removal.

---

## Build a Windows executable

PyInstaller is already installed in this environment, so you can build a standalone executable with either of the following methods.

### Option 1: Run the build command directly

```powershell
cd task-manager
pyinstaller --noconfirm --onefile --windowed --name SSquadTaskManager app.py
```

### Option 2: Use the helper script

```powershell
cd task-manager
powershell -ExecutionPolicy Bypass -File .\build_exe.ps1
```

The executable is produced in:

```text
task-manager/dist/SSquadTaskManager.exe
```

### Packaged-app storage location

When the executable is running, data is stored in:

```text
%USERPROFILE%\.ssquad\tasks.json
```

This prevents the packaged app from writing into the extracted temporary directory.

---

## Data model

Each saved task contains:

- `id` — numeric identifier
- `title` — task title
- `description` — short summary
- `priority` — `high`, `medium`, or `low`
- `due_date` — optional date in `YYYY-MM-DD`
- `completed` — boolean status

---

## Verification

The current implementation has been verified with:

```powershell
cd task-manager
python -m unittest discover -s tests
python -m py_compile app.py task_store.py
```

It also produced a packaged executable at:

```text
task-manager/dist/SSquadTaskManager.exe
```

---

## Troubleshooting

### "No module named tkinter"

Install Python with Tkinter support enabled, or reinstall Python on Windows and make sure the Tk/Tcl components are selected.

### "PyInstaller not found"

Install it with:

```powershell
python -m pip install pyinstaller
```

### App opens but does not save data

Check that the app has permission to write to the storage path:

- Source run: `task-manager/tasks.json`
- Packaged run: `%USERPROFILE%\.ssquad\tasks.json`

---

## Notes

- The sample content in `tasks.json` is preserved and will load automatically.
- The app uses its own validation for empty titles and invalid due dates.
- The UI is intentionally lightweight and uses only Python's standard library plus Tkinter.


