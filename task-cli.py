import argparse 
import json
import os
import datetime

def write_file(data):
    with open("todo.json", "w") as f:
        json.dump(data, f, indent = 4)

def read_file():
    if os.path.exists("todo.json"):
        try:
            with open("todo.json", "r") as f:
                todo_dict = json.load(f)
        except json.JSONDecodeError:
            todo_dict = {}
    else:
        todo_dict = {}
    
    return todo_dict


def add_task(task_description, status = 'todo'):

    todo_dict = read_file()
    
    if todo_dict:
        current_id = max(int(k) for k in todo_dict.keys()) + 1
    else:
        current_id = 1
    
    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    update_time = current_time

    todo_dict[current_id] = {
        'description':task_description,
        'status': status,
        'createdAt':current_time,
        'updatedAt':update_time
    }

    write_file(todo_dict)
    print("Complete adding Task!")

def update_task(id, new_description):
    todo_dict = read_file()

    key = str(id)
    item = todo_dict.get(key)

    if not item:
        print(f"Task with {id} was not found!")
        return

    item['description'] = new_description
    item['updatedAt'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    todo_dict[key] = item
    write_file(todo_dict)

    print(f"Complete updating task with id {key}")

def delete_task(id):
    todo_dict = read_file()

    key = str(id)

    del todo_dict[key]
    write_file(todo_dict)

    print(f"Complete deleting task with id {key}")


def mark_in_progress(id):
    todo_dict = read_file()

    key = str(id)

    item = todo_dict[key]
    old_status = item.get('status', 'unknown')

    
    item['status'] = "in progress"
    item['updatedAt'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    todo_dict[key] = item
    write_file(todo_dict)

    print(f"Successfully change status from {old_status} to on-progress")

def mark_done(id):
    todo_dict = read_file()

    key = str(id)
    item = todo_dict[key]

    old_status = item.get('status', "unknown")
    item["status"] = "done"
    item['updatedAt'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    todo_dict[key] = item
    write_file(todo_dict)

    print(f"Successfully change status from {old_status} to done")

def list_task(status_filter = None):
    todo_dict = read_file()

    print(f"{'ID':<4} {'Todo':<50} {'Status':<20} {'Created At':<20} {"Last Updated":<20}")
    print("-" * 120)
    for id_, item in todo_dict.items():
        if status_filter is None or item["status"] == status_filter:   
            print(f"{id_:<4} {item['description']:<50} {item['status']:<20} {item['createdAt']:<20} {item['updatedAt']:<20}")
    print("-" * 120)

def main():
    parser = argparse.ArgumentParser(prog = 'task-cli', description = "Simple task manager")

    subparsers= parser.add_subparsers(dest = "command", help="Sub-command help")

    # subcommand add
    addTask_parser = subparsers.add_parser("add", help ="Add a new task")
    addTask_parser.add_argument("description", type=str, help = 'Add Task Description')

    # subcommand update
    updateTask_parser = subparsers.add_parser("update", help = "Update a task with id")
    updateTask_parser.add_argument("id", type = int, help = "Task ID")
    updateTask_parser.add_argument("description", type = str, help = "Update Task Description")

    # subcommand delete
    deleteTask_parser = subparsers.add_parser("delete", help = "Delete A task")
    deleteTask_parser.add_argument("id", type = int, help="Task ID")

    # subcommand mark-in-progress
    mipTask_parser = subparsers.add_parser("mark-in-progress", help= "Mark status to 'in progress'")
    mipTask_parser.add_argument("id", type=int, help= "Task ID")

    # subcommand done 
    doneTask_parser = subparsers.add_parser("mark-done", help="Mark status to 'done'")
    doneTask_parser.add_argument("id", type= int, help= "Task ID")

    # subcommand list
    listTask_parser = subparsers.add_parser("list", help="List all Task")
    listTask_parser.add_argument(
        "status",
        type=str,
        nargs = "?",
        choices=['todo','in-progress','done'],
        help="Filter Task By Status"
    )


    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        mark_in_progress(args.id)
    elif args.command == "mark-done":
        mark_done(args.id)
    elif args.command == "list":
        list_task(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()