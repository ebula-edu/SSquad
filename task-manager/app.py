from __future__ import annotations

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from task_store import TaskStore


class TaskManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SSquad Task Manager")
        self.root.geometry("1120x720")
        self.root.minsize(1040, 680)
        self.root.configure(bg="#0f172a")

        self.store = TaskStore()
        self.editing_id = None

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")
        self.title_var = tk.StringVar()
        self.due_date_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="Medium")
        self.description_text = tk.Text(height=6, width=55, wrap="word")

        self._build_styles()
        self._build_layout()
        self.refresh_tasks()

    def _build_styles(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#0f172a")
        style.configure("TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 18, "bold"))
        style.configure("Subheader.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 11))
        style.configure("Card.TFrame", background="#111827")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 6))
        style.configure("Primary.TButton", background="#38bdf8", foreground="#0f172a")
        style.configure("Danger.TButton", background="#fb7185", foreground="#0f172a")
        style.configure("TEntry", padding=(6, 4))
        style.configure("TCombobox", padding=(6, 4))

    def _build_layout(self):
        root = self.root
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        top_bar = tk.Frame(root, bg="#0f172a")
        top_bar.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 8))
        top_bar.grid_columnconfigure(1, weight=1)

        title_label = ttk.Label(top_bar, text="SSquad Task Manager", style="Header.TLabel")
        title_label.grid(row=0, column=0, sticky="w")

        subtitle = ttk.Label(
            top_bar,
            text="Plan, prioritize, and complete your work from one polished desktop dashboard.",
            style="Subheader.TLabel",
            justify="left",
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.status_label = ttk.Label(top_bar, text="Loading tasks…", style="Subheader.TLabel")
        self.status_label.grid(row=0, column=1, rowspan=2, sticky="e")

        stats_frame = tk.Frame(root, bg="#0f172a")
        stats_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 12))
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        stats_frame.grid_columnconfigure(2, weight=1)
        stats_frame.grid_columnconfigure(3, weight=1)

        self.stats_cards = {}
        for idx, (label, value) in enumerate((("Total tasks", "0"), ("Pending", "0"), ("Completed", "0"), ("High priority", "0"))):
            card = tk.Frame(stats_frame, bg="#111827", bd=0)
            card.grid(row=0, column=idx, padx=(0 if idx == 0 else 12, 0), sticky="ew")
            card.grid_columnconfigure(0, weight=1)

            ttk.Label(card, text=label, style="Subheader.TLabel").grid(row=0, column=0, sticky="w", padx=14, pady=(14, 4))
            value_label = ttk.Label(card, text=value, style="Header.TLabel")
            value_label.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 14))
            self.stats_cards[label] = value_label

        content = tk.Frame(root, bg="#0f172a")
        content.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        content.grid_columnconfigure(0, weight=0)
        content.grid_columnconfigure(1, weight=1)

        form_frame = tk.Frame(content, bg="#111827", bd=0)
        form_frame.grid(row=0, column=0, sticky="ns", padx=(0, 12))
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(9, weight=1)

        ttk.Label(form_frame, text="Create or edit a task", style="Header.TLabel").grid(row=0, column=0, sticky="w", padx=16, pady=(16, 10))
        ttk.Label(form_frame, text="Title", style="Subheader.TLabel").grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))
        ttk.Entry(form_frame, textvariable=self.title_var, width=40).grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))

        ttk.Label(form_frame, text="Priority", style="Subheader.TLabel").grid(row=3, column=0, sticky="w", padx=16, pady=(0, 4))
        priority_box = ttk.Combobox(form_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly")
        priority_box.grid(row=4, column=0, sticky="ew", padx=16, pady=(0, 12))

        ttk.Label(form_frame, text="Due date (YYYY-MM-DD)", style="Subheader.TLabel").grid(row=5, column=0, sticky="w", padx=16, pady=(0, 4))
        ttk.Entry(form_frame, textvariable=self.due_date_var, width=40).grid(row=6, column=0, sticky="ew", padx=16, pady=(0, 12))

        ttk.Label(form_frame, text="Description", style="Subheader.TLabel").grid(row=7, column=0, sticky="w", padx=16, pady=(0, 4))
        self.description_text.grid(row=8, column=0, sticky="ew", padx=16, pady=(0, 16))

        save_btn = ttk.Button(form_frame, text="Save task", command=self.save_task)
        save_btn.grid(row=9, column=0, sticky="ew", padx=16, pady=(0, 12))

        clear_btn = ttk.Button(form_frame, text="Clear form", command=self.clear_form)
        clear_btn.grid(row=10, column=0, sticky="ew", padx=16, pady=(0, 16))

        actions_frame = tk.Frame(form_frame, bg="#111827")
        actions_frame.grid(row=11, column=0, sticky="ew", padx=16, pady=(0, 16))
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

        toggle_btn = ttk.Button(actions_frame, text="Toggle complete", command=self.toggle_selected_task)
        toggle_btn.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        delete_btn = ttk.Button(actions_frame, text="Delete task", command=self.delete_selected_task)
        delete_btn.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        task_panel = tk.Frame(content, bg="#0f172a")
        task_panel.grid(row=0, column=1, sticky="nsew")
        task_panel.grid_rowconfigure(1, weight=1)
        task_panel.grid_columnconfigure(0, weight=1)

        toolbar = tk.Frame(task_panel, bg="#0f172a")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        toolbar.grid_columnconfigure(0, weight=1)

        ttk.Label(toolbar, text="Task list", style="Header.TLabel").grid(row=0, column=0, sticky="w")

        search_frame = tk.Frame(toolbar, bg="#0f172a")
        search_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        search_frame.grid_columnconfigure(0, weight=1)

        ttk.Entry(search_frame, textvariable=self.search_var, width=50).grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(search_frame, text="Search", command=self.refresh_tasks).grid(row=0, column=1, padx=(0, 10))

        filter_box = ttk.Combobox(search_frame, textvariable=self.filter_var, values=["All", "Pending", "Completed"], state="readonly", width=12)
        filter_box.grid(row=0, column=2)
        filter_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_tasks())

        columns = ("id", "status", "title", "priority", "due_date", "description")
        self.tree = ttk.Treeview(task_panel, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("status", text="Status")
        self.tree.heading("title", text="Title")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("due_date", text="Due date")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("title", width=240)
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("due_date", width=120, anchor="center")
        self.tree.column("description", width=300)

        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        scrollbar = ttk.Scrollbar(task_panel, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.root.bind("<Return>", lambda _event: self.save_task())

    def _priority_label(self, value):
        text = str(value).strip().lower()
        if text == "high":
            return "High"
        if text == "low":
            return "Low"
        return "Medium"

    def _due_date_display(self, due_date):
        if not due_date:
            return "No due date"
        return due_date

    def _task_count_info(self):
        tasks = self.store.get_tasks()
        total = len(tasks)
        pending = sum(1 for task in tasks if not task.get("completed"))
        completed = total - pending
        high = sum(1 for task in tasks if task.get("priority") == "high")
        return total, pending, completed, high

    def refresh_tasks(self):
        tasks = self.store.get_tasks()
        query = self.search_var.get().strip().lower()
        selected_filter = self.filter_var.get()

        filtered = []
        for task in tasks:
            if selected_filter == "Pending" and task.get("completed"):
                continue
            if selected_filter == "Completed" and not task.get("completed"):
                continue
            if query and query not in task.get("title", "").lower() and query not in task.get("description", "").lower():
                continue
            filtered.append(task)

        for child in self.tree.get_children():
            self.tree.delete(child)

        for task in filtered:
            status = "Completed" if task.get("completed") else "Pending"
            priority = self._priority_label(task.get("priority"))
            self.tree.insert(
                "",
                "end",
                values=(
                    task.get("id"),
                    status,
                    task.get("title", ""),
                    priority,
                    self._due_date_display(task.get("due_date", "")),
                    task.get("description", ""),
                ),
                tags=(task.get("priority"), "completed" if task.get("completed") else "pending"),
            )

        total, pending, completed, high = self._task_count_info()
        self.stats_cards["Total tasks"].configure(text=str(total))
        self.stats_cards["Pending"].configure(text=str(pending))
        self.stats_cards["Completed"].configure(text=str(completed))
        self.stats_cards["High priority"].configure(text=str(high))

        self.status_label.configure(text=f"{len(filtered)} visible • {pending} pending • {completed} completed")

        if not filtered:
            self.tree.insert("", "end", values=("", "No tasks", "", "", "", ""))

    def on_tree_select(self, _event):
        selection = self.tree.selection()
        if not selection:
            return

        task_id = int(self.tree.item(selection[0], "values")[0])
        task = next((item for item in self.store.get_tasks() if item.get("id") == task_id), None)
        if not task:
            return

        self.editing_id = task_id
        self.title_var.set(task.get("title", ""))
        self.priority_var.set(self._priority_label(task.get("priority")))
        self.due_date_var.set(task.get("due_date", ""))
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", task.get("description", ""))

    def clear_form(self):
        self.editing_id = None
        self.title_var.set("")
        self.priority_var.set("Medium")
        self.due_date_var.set("")
        self.description_text.delete("1.0", tk.END)

    def save_task(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please add a title before saving the task.")
            return

        due_date = self.due_date_var.get().strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Invalid date", "Please use the format YYYY-MM-DD for the due date.")
                return

        description = self.description_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get().strip().lower()

        if self.editing_id is not None:
            updated = self.store.update_task(
                self.editing_id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
            )
            if updated is None:
                messagebox.showerror("Save failed", "The selected task could not be updated.")
                return
            messagebox.showinfo("Task updated", f"Updated task #{self.editing_id}.")
        else:
            self.store.add_task(title=title, description=description, priority=priority, due_date=due_date)
            messagebox.showinfo("Task added", f"Added task '{title}'.")

        self.clear_form()
        self.refresh_tasks()

    def toggle_selected_task(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a task first to toggle its completion status.")
            return

        task_id = int(self.tree.item(selection[0], "values")[0])
        updated = self.store.toggle_complete(task_id)
        if updated is None:
            messagebox.showerror("Toggle failed", "The selected task could not be updated.")
            return

        self.refresh_tasks()

    def delete_selected_task(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No selection", "Select a task first to delete it.")
            return

        task_id = int(self.tree.item(selection[0], "values")[0])
        if not messagebox.askyesno("Delete task", "Delete this task permanently?"):
            return

        deleted = self.store.delete_task(task_id)
        if not deleted:
            messagebox.showerror("Delete failed", "The selected task could not be deleted.")
            return

        self.clear_form()
        self.refresh_tasks()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TaskManagerApp().run()

