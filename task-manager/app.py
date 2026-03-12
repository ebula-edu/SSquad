import sys
import json

TASKS_FILE = "tasks.json"
tasks = []
next_id = 1

def load_tasks():
    global tasks, next_id
    try:
        with open(TASKS_FILE, "r") as f:
            tasks = json.load(f)
            if tasks:
                next_id = max(task["id"] for task in tasks) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []


def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task():
    global next_id
    print("\n=== Add New Task ===\n")
    title = input("Title: ").strip()
    description = input("Description: ").strip()
    while True:
        try:
            priority = int(input("Priority (1=High, 2=Medium, 3=Low): "))
            if priority not in [1, 2, 3]:
                raise ValueError
            break
        except ValueError:
            print("Invalid priority! Enter 1, 2, or 3 only.")

    task = {"id": next_id, "title": title, "description": description, "priority": priority}
    tasks.append(task)
    next_id += 1
    save_tasks()
    print("\nTask '" + title + "' added successfully!\n")


def list_tasks():
    if not tasks:
        print("\nNo tasks available.\n")
        return

    print("\n=== Task List ===")
    print("{:<5} {:<20} {:<8} {}".format("ID", "Title", "Priority", "Description"))
    print("-"*60)
    sorted_tasks = sorted(tasks, key=lambda x: x["priority"])
    for task in sorted_tasks:
        print("{:<5} {:<20} {:<8} {}".format(
            task["id"],
            task["title"][:20],  
            task["priority"],
            task["description"]
        ))
    print("-"*60 + "\n")


def update_task():
    if not tasks:
        print("\nNo tasks to update.\n")
        return

    try:
        task_id = int(input("\nEnter task ID to update: "))
    except ValueError:
        print("Invalid ID! Must be a number.\n")
        return

    for task in tasks:
        if task["id"] == task_id:
            print("\nUpdating Task ID " + str(task_id))
            new_title = input("New title [" + task["title"] + "]: ").strip()
            if new_title != "":
                task["title"] = new_title

            new_desc = input("New description [" + task["description"] + "]: ").strip()
            if new_desc != "":
                task["description"] = new_desc

            new_priority = input("New priority (1-High,2-Medium,3-Low) [" + str(task["priority"]) + "]: ").strip()
            if new_priority != "":
                try:
                    new_priority = int(new_priority)
                    if new_priority in [1, 2, 3]:
                        task["priority"] = new_priority
                    else:
                        print("Invalid priority, keeping previous.")
                except ValueError:
                    print("Invalid input, keeping previous.")
            save_tasks()
            print("Task updated successfully!\n")
            return

    print("Task ID not found.\n")


def delete_task():
    if not tasks:
        print("\nNo tasks to delete.\n")
        return

    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print("Invalid ID! Must be a number.\n")
        return

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            confirm = input("Are you sure you want to delete '" + task["title"] + "'? (y/n): ").lower()
            if confirm == "y":
                tasks.pop(i)
                save_tasks()
                print("Task ID " + str(task_id) + " deleted successfully!\n")
            else:
                print("Delete canceled.\n")
            return

    print("Task ID not found.\n")


def search_tasks():
    if not tasks:
        print("\nNo tasks to search.\n")
        return

    keyword = input("\nEnter keyword to search in titles: ").strip().lower()
    found = []
    for task in tasks:
        if keyword in task["title"].lower():
            found.append(task)

    if not found:
        print("No matching tasks found.\n")
        return

    print("\n=== Search Results (" + str(len(found)) + " tasks found) ===")
    print("{:<5} {:<20} {:<8} {}".format("ID", "Title", "Priority", "Description"))
    print("-"*60)
    for task in found:
        print("{:<5} {:<20} {:<8} {}".format(
            task["id"],
            task["title"][:20],
            task["priority"],
            task["description"]
        ))
    print("-"*60 + "\n")


def menu():
    load_tasks()
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            search_tasks()
        elif choice == "6":
            print("\nExiting program. Goodbye!\n")
            sys.exit()
        else:
            print("Invalid choice! Please try again.\n")

if __name__ == "__main__":
    menu()
