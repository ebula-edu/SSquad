# Python Task Manager

A simple command-line task manager built with Python that allows you to add, list, update, delete, and search tasks. Tasks are stored in a local JSON file (`tasks.json`) for persistence.

---

## Features

* Add a new task with title, description, and priority (High, Medium, Low)
* List all tasks, sorted by priority
* Update existing tasks
* Delete tasks with confirmation
* Search tasks by keyword in the title
* Persistent storage using JSON

---

## Requirements

* Python 3.x installed
* Basic familiarity with command-line interface (CLI)

---

## Installation

1. Clone or download this repository to your local machine:

```bash
git clone <https://github.com/ebula-edu/SSquad/>
```

2. Navigate to the project folder:

```bash
cd <task-manager>
```

3. Make sure Python 3 is installed:

```bash
python --version
```

4. No additional libraries are required since this project uses only Python's built-in modules (`sys` and `json`).

---

## Setup

1. Create an empty file named `tasks.json` in the project directory:

```bash
touch tasks.json
```

*(Optional: If the file does not exist, the program will create it automatically when you first add a task.)*

2. Open a terminal and run the program:

```bash
python task_manager.py
```

---

## How to Use

When you run the program, a menu will appear:

```
=== Task Manager ===
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Search Tasks
6. Exit
```

### 1. Add Task

* Enter the title and description of the task.
* Set the priority:

  * `1` = High
  * `2` = Medium
  * `3` = Low

### 2. List Tasks

* Displays all tasks sorted by priority in a table format.
* Shows task ID, title, priority, and description.

### 3. Update Task

* Enter the task ID you want to update.
* Update any of the fields (leave blank to keep the current value).

### 4. Delete Task

* Enter the task ID you want to delete.
* Confirm deletion by typing `y`.

### 5. Search Tasks

* Enter a keyword to search in task titles.
* Displays all matching tasks.

### 6. Exit

* Closes the program safely.

---

## File Structure

```
task-manager/
│
├── app.py             # Main Python program
├── tasks.json         # JSON file storing tasks
└── README.md          # This file
```

---

## Example Usage

```
=== Task Manager ===
1. Add Task
2. List Tasks
3. Update Task
4. Delete Task
5. Search Tasks
6. Exit

Choose an option: 1

=== Add New Task ===
Title: Finish report
Description: Complete the annual report by Friday
Priority (1=High, 2=Medium, 3=Low): 1

Task 'Finish report' added successfully!
```

---

## Notes

* Task IDs are automatically generated.
* Priority is used for sorting tasks when listing them.
* Data persists between sessions using `tasks.json`.
* Make sure `tasks.json` has proper read/write permissions.
