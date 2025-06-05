# cli-task-tracker

**task-cli** is a simple command-line interface (CLI) tool written in Python for managing your to-do tasks.  
It helps you add, update, mark status, and list tasks directly from your terminal.

---

## Features

- Add a new task  
  `task-cli add "Buy Groceries"`

- Update a task description by ID  
  `task-cli update 1 "Buy Books"`

- Mark a task status:  
  - In progress  
    `task-cli mark-in-progress 1`  
  - Done  
    `task-cli mark-done 1`

- List tasks with optional status filter:  
  - List all tasks  
    `task-cli list`  
  - List tasks by status (`todo`, `in progress`, `done`)  
    `task-cli list done`

---

## Usage

1. Clone this repository:  
   ```bash
   git clone https://github.com/huszen/task-cli.git
   cd task-cli
   python task-cli.py <command> [arguments]
   
   example:
   python task-cli.py add "Buy Groceries"
