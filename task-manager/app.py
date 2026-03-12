class Task:
    def __init__(self, task_id, title, priority, due_date, completed):
        self.task_id = task_id
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def display(self):
        if self.completed == True:
            status = "✓"
        else:
            status = "○"
        if self.priority == 1:
            p = "HIGH"
        elif self.priority == 2:
            p = "MED"
        else:
            p = "LOW"
        return status + " | " + p + " | ID:" + str(self.task_id) + " | " + self.title + " | Due: " + self.due_date

class TaskManager:

    def __init__(self):
        self.tasks = {}
        self.priority_list = []
        self.next_id = 1
        self.load_tasks()

    def save_tasks(self):
        file = open("tasks.txt", "w")
        for task_id in self.tasks:
            t = self.tasks[task_id]
            line = str(t.task_id) + "|" + t.title + "|" + str(t.priority) + "|" + t.due_date + "|" + str(t.completed)
            file.write(line + "\n")
        file.close()

    def load_tasks(self):

        try:
            file = open("tasks.txt", "r")
            for line in file:
                line = line.strip()
                parts = line.split("|")
                tid = int(parts[0])
                title = parts[1]
                priority = int(parts[2])
                date = parts[3]
                if parts[4] == "True":
                    completed = True
                else:
                    completed = False
                task = Task(tid, title, priority, date, completed)
                self.tasks[tid] = task
                self.priority_list.append((priority, tid))
                if tid >= self.next_id:
                    self.next_id = tid + 1
            file.close()

        except:
            pass

    def add_task(self):
        print("\nADD TASK")
        title = input("Title: ")
        if title == "":
            print("Title cannot be empty")
            return
        print("Priority")
        print("1 High")
        print("2 Medium")
        print("3 Low")

        pr = input("Choose: ")
        if pr == "1":
            p = 1
        elif pr == "2":
            p = 2
        elif pr == "3":
            p = 3
        else:
            p = 2
        date = input("Due Date YYYY-MM-DD: ")
        task = Task(self.next_id, title, p, date, False)
        self.tasks[self.next_id] = task
        self.priority_list.append((p, self.next_id))
        print("Task added ID " + str(self.next_id))
        self.next_id = self.next_id + 1
        self.save_tasks()

    def view_tasks(self):
        if len(self.tasks) == 0:
            print("No tasks")
            return
        print("1 By ID")
        print("2 By Priority")
        print("3 By Title")
        print("4 By Date")
        c = input("Choice: ")
        if c == "1":
            self.view_by_id()
        elif c == "2":
            self.view_by_priority()
        elif c == "3":
            self.view_by_title()
        elif c == "4":
            self.view_by_date()
        else:
            self.view_by_id()
    def view_by_id(self):

        ids = []
        for task_id in self.tasks:
            ids.append(task_id)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                if ids[i] > ids[j]:
                    temp = ids[i]
                    ids[i] = ids[j]
                    ids[j] = temp
        for i in ids:
            print(self.tasks[i].display())
    def view_by_priority(self):
        task_list = []
        for task_id in self.tasks:
            task_list.append(self.tasks[task_id])
        n = len(task_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if task_list[j].priority > task_list[j + 1].priority:
                    temp = task_list[j]
                    task_list[j] = task_list[j + 1]
                    task_list[j + 1] = temp
        for t in task_list:
            print(t.display())
    def view_by_title(self):
        task_list = []
        for task_id in self.tasks:
            task_list.append(self.tasks[task_id])
        n = len(task_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if task_list[j].title > task_list[j + 1].title:
                    temp = task_list[j]
                    task_list[j] = task_list[j + 1]
                    task_list[j + 1] = temp
        for t in task_list:
            print(t.display())

    def view_by_date(self):
        task_list = []
        for task_id in self.tasks:
            task_list.append(self.tasks[task_id])
        n = len(task_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if task_list[j].due_date > task_list[j + 1].due_date:
                    temp = task_list[j]
                    task_list[j] = task_list[j + 1]
                    task_list[j + 1] = temp
        for t in task_list:
            print(t.display())

    def search_task(self):
        text = input("Search title: ")
        text = text.lower()
        found = False
        for task_id in self.tasks:
            t = self.tasks[task_id]
            if text in t.title.lower():
                print(t.display())
                found = True
        if found == False:
            print("No result")

    def complete_task(self):
        tid = input("Enter task ID: ")
        if tid.isdigit():
            tid = int(tid)
            if tid in self.tasks:
                self.tasks[tid].completed = True
                print("Task completed")
                self.save_tasks()
            else:
                print("Not found")
        else:
            print("Invalid ID")
    def delete_task(self):
        tid = input("Delete ID: ")
        if tid.isdigit():
            tid = int(tid)
            if tid in self.tasks:
                del self.tasks[tid]
                new_list = []
                for item in self.priority_list:
                    if item[1] != tid:
                        new_list.append(item)
                self.priority_list = new_list
                print("Deleted")
                self.save_tasks()
            else:
                print("Task not found")
    def stats(self):
        total = len(self.tasks)
        done = 0
        high = 0
        med = 0
        low = 0

        for task_id in self.tasks:
            t = self.tasks[task_id]
            if t.completed == True:
                done = done + 1
            if t.priority == 1:
                high = high + 1
            elif t.priority == 2:
                med = med + 1
            else:
                low = low + 1
        pending = total - done
        print("Total " + str(total))
        print("Completed " + str(done))
        print("Pending " + str(pending))
        print("High " + str(high))
        print("Medium " + str(med))
        print("Low " + str(low))

    def run(self):
        while True:
            print("\nTASK MANAGER")
            print("1 Add")
            print("2 View")
            print("3 Search")
            print("4 Complete")
            print("5 Delete")
            print("6 Stats")
            print("7 Exit")

            c = input("Choice: ")
            if c == "1":
                self.add_task()
            elif c == "2":
                self.view_tasks()
            elif c == "3":
                self.search_task()
            elif c == "4":
                self.complete_task()
            elif c == "5":
                self.delete_task()
            elif c == "6":
                self.stats()
            elif c == "7":
                print("Babye")
                break
            else:
                print("Invalid")
            input("Press Enter...")
            
print("TASK MANAGER SYSTEM")
manager = TaskManager()
manager.run()
