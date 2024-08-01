import argparse
from models import TaskManager

task_manager = TaskManager()
parser = argparse.ArgumentParser(description="Task Manager CLI")

task_manager.load_from_file()

subparsers = parser.add_subparsers(dest="command")

# ----------------ADD--------------
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("title", type=str, help="Title of the task")
add_parser.add_argument("description", type=str, help="Description of the task")
add_parser.add_argument("due_date", type=str, help="Due date in format YYYY-MM-DD")


# ------------REMOVE---------------
remove_parser = subparsers.add_parser("remove", help="Remove a task")
remove_parser.add_argument("id", type=int, help="ID of the task to remove")


# ------------EDIT-----------------
edit_parser = subparsers.add_parser("edit", help="Edit an existing task")
edit_parser.add_argument("id", type=int, help="ID of the task to edit")
edit_parser.add_argument("--aspect", type=str, help="Which setting of a task to change for example: cli.py edit 6 'title' ...")
edit_parser.add_argument("--title", type=str, help="New title of the task")
edit_parser.add_argument("--description", type=str, help="New description of the task")
edit_parser.add_argument("--due_date", type=str, help="New due date in format YYYY-MM-DD")

# ------------LIST-----------------
list_parser = subparsers.add_parser("list", help="List all tasks")


# -----------COMPLETE---------------
complete_parser = subparsers.add_parser("complete", help="Complete a task")
complete_parser.add_argument("id", type=int, help="ID of the task to mark as complete")


args = parser.parse_args()


# -----------LOGIC-------------------
if args.command == "add":
    # Call the function to add a task
    task_manager.create_task(args.title, args.description, args.due_date)
elif args.command == "remove":
    # Call the function to remove a task
    task_manager.delete_task(args.id)
elif args.command == "edit":
    # Call the function to edit a task
    task_manager.change_task(args.id,args.aspect, args.title, args.description, args.due_date)
elif args.command == "list":
    # Call the function to list all tasks
    task_manager.list_tasks()
elif args.command == "complete":
    # Call the function to complete a task
    task_manager.complete_task(args.id)


task_manager.save_to_file()
