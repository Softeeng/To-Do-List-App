import json
import os
from datetime import datetime
import sys

# On some Windows consoles the default encoding can't print emoji; try to wrap stdout/stderr in UTF-8
try:
    if sys.stdout.encoding is None or 'UTF' not in sys.stdout.encoding.upper():
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    # Python <3.7 or other environments may not support reconfigure; ignore if it fails
    pass
try:
    if sys.stderr.encoding is None or 'UTF' not in sys.stderr.encoding.upper():
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

class TodoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
                print(f"✔️ Loaded {len(self.tasks)} tasks from file")
            except json.JSONDecodeError:
                print("⚠️ Error loading tasks. Starting with an empty list.")
                self.tasks = []
        else:
            print("ℹ️ No existing task file found. Starting with an empty list.")
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            print("✔️ Tasks saved successfully")
        except Exception as e:
            print(f"⚠️ Error saving tasks: {e}")

    def add_task(self, description):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'done': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        print(f"✔️ Task added: '{description}'")
        self.save_tasks()

    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("\n📋 No tasks yet! Add one to get started.\n")
            return

        print("\n" + "="*60)
        print("📋 YOUR TO-DO LIST")
        print("="*60)

        for task in self.tasks:
            status = "✅" if task['done'] else "❌"
            done_text = "DONE" if task['done'] else "PENDING"
            print(f"{status} [{task['id']}] {task['description']}")
            print(f"    Status: {done_text} | Created at: {task['created_at']}")
            print("-"*60)
        print()

    def edit_task(self, task_id, new_description):
        """Edit an existing task"""
        for task in self.tasks:
            if task['id'] == task_id:
                old_description = task['description']
                task['description'] = new_description
                print(f"✔️ Task {task_id} updated:")
                print(f"   Old: '{old_description}'")
                print(f"   New: '{new_description}'")
                self.save_tasks()
                return
        print(f"✖️ Task {task_id} not found.")

    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted = self.tasks.pop(i)
                print(f"✔️ Deleted: '{deleted['description']}'")
                # Re-number remaining tasks
                for idx, t in enumerate(self.tasks):
                    t['id'] = idx + 1
                self.save_tasks()
                return
        print(f"✖️ Task {task_id} not found.")

    def mark_done(self, task_id):
        """Mark a task as done"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['done'] = True
                print(f"✔️ Marked as done: '{task['description']}'")
                self.save_tasks()
                return
        print(f"✖️ Task {task_id} not found.")

    def mark_undone(self, task_id):
        """Mark a task as undone"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['done'] = False
                print(f"⭕ Marked as undone: '{task['description']}'")
                self.save_tasks()
                return
        print(f"✖️ Task {task_id} not found.")

def print_menu():
        """Display the main menu"""
        print("\n" + "="*60)
        print("📋 TO-DO LIST MANAGER")
        print("="*60)
        print("1. View all Tasks")
        print("2. Add a Task")
        print("3. Edit a Task")
        print("4. Delete a Task")
        print("5. Mark Task as Done")
        print("6. Mark Task as Undone")
        print("7. Exit")
        print("="*60)

def main():
    # Show welcome message before initializing TodoList so it is visible
    # even if loading tasks raises an error. Flush to ensure output appears
    # immediately in environments with buffered stdout.
    print("👋 Welcome to your To-Do List Manager!", flush=True)
    todo = TodoList()

    while True:
        print_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == '1':
            todo.view_tasks()

        elif choice == '2':
            description = input("📝 Enter task description: ").strip()
            if description:
                todo.add_task(description)
            else:
                print("⚠️ Task description cannot be empty.")

        elif choice == '3':
            todo.view_tasks()
            try:
                task_id = int(input("✏️ Enter task ID to edit: "))
                new_description = input("📝 Enter new description: ").strip()
                if new_description:
                    todo.edit_task(task_id, new_description)
                else:
                    print("⚠️ New description cannot be empty.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid task ID.")

        elif choice == '4':
            todo.view_tasks()
            try:
                task_id = int(input("🗑️ Enter task ID to delete: "))
                confirm = input(f"Are you sure you want to delete task {task_id}? (y/n): ").lower()
                if confirm == 'y':
                    todo.delete_task(task_id)
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid task ID.")

        elif choice == '5':
            todo.view_tasks()
            try:
                task_id = int(input("✅ Enter task ID to mark as done: "))
                todo.mark_done(task_id)
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid task ID.")

        elif choice == '6':
            todo.view_tasks()
            try:
                task_id = int(input("⭕ Enter task ID to mark as undone: "))
                todo.mark_undone(task_id)
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid task ID.")

        elif choice == '7':
            print("\n👋 Thanks for using To-Do List Manager! Goodbye!")
            break

        else:
            print("⚠️ Invalid choice. Please select a valid option between 1 and 7.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()