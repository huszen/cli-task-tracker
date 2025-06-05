import json
import time
import sys
import os


# function helper
def clear_screen():
    if os.name == "nt":
        os.system("cls")

def print_welcome():
    print("=" * 40)
    print("      📝 Welcome to CLI-Task 🧠      ")
    print("=" * 40)

def loading_spinner(duration = 3):
    spinner = ["|", "/", "-", "\\"]
    print("Processing ", end = "", flush =True)
    end_time = time.time() + duration
    i = 0  
    while time.time() < end_time:
        sys.stdout.write(spinner[i % len(spinner)])
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
        i+=1

def show_menu():
    options = ["Add ToDo", "Update ToDo", "Delete ToDO", "Read ToDo"]
    print("="*40)
    for i,opt in enumerate(options):
        print(f"{i + 1}. {opt}")
    print("="*40)

def input_range(prompt, min_val, max_val):
    while True:
        value = input(prompt)
        if value.isdigit() and min_val <=int(value) <= int(max_val):
            return value
        print(f"❌ Input is invalid. Please input range between {min_val} - {max_val}")

def write_todos(data):
    with open("todo.json", "w") as f:
        json.dump(data, f, indent = 4)

def read_todos_file():
    if os.path.exists("todo.json"):
        with open("todo.json", "r") as f:
            try:
                todo_dict = json.load(f)
            except json.JSONDecodeError:
                todo_dict = {}
    else:
        todo_dict = {}
    return todo_dict

def view_todos():
    todo_dict = read_todos_file()
    print(f"{'ID':<4} {'Todo':<50} {'Deadline'}")
    print("-" * 120)
    for id_, item in todo_dict.items():
        print(f"{id_:<4} {item['todo']:<50} {item['date']}/{item['month']}/2025")
    print("-" * 120)

def add_todo():
    todo_dict = read_todos_file()
    while True:
        # the inputs
        todo = input("What you want to do? : ")
        print("When is the deadline?")
        print("="*40)
        date = input_range("Date (1-31): ", 1, 31)
        month = input_range("Month (1-12): ", 1, 12)

        # take the id
        if todo_dict:
            current_id = max(int(k) for k in todo_dict.keys()) + 1
        else:
            current_id = 1

        # double check input before put it to json file
        print(f"\nYou are going to add:\n✅ {todo} in {date}/{month}/2025")

        confirm = input("Is it right? (Y/n)")
        if confirm.lower() == "y":
            todo_dict[str(current_id)] = {
                "todo":todo,
                "date":date,
                "month":month
            } 

            write_todos(todo_dict)
            
            next = input("Next? (Y/n)")
            if next.lower() == "n":
                print("\nTodo List")
                with open("todo.json", "r") as f:
                    data = json.load(f)
                
                # print(f"{'ID':<4} {'Todo':<100} {'Deadline'}")
                # print("-" * 150)
                # for id_, item in todo_dict.items():
                #     print(f"{id_:<4} {item['todo']:<100} {item['date']}/{item['month']}/2025")
                # print("-" * 150)
                view_todos()
                clear_screen()
                print("Your ToDo is Saved 👌, to exit press 'q'")

                break
        else:
            print("Please input again 😅")

def update_todo():
    view_todos()
    todo_dict = read_todos_file()

    select_id = input_range(f"Please select item you want to update 1-{len(todo_dict)}:",1, len(todo_dict))

    # get the item
    item = todo_dict.get(select_id)

    change_option = list(item.keys())

    print("Print What do you want to change?")
    for id, copt in enumerate(change_option):
        print(f"{id + 1} - {copt}")
    
    chooser = input_range(f"Choose the id between 1-{len(change_option)} : ", 1 , len(change_option))

    if chooser == "1":
        print("You want to change 'ToDo'")
        change_todo = input(f"Change Todo from '{item['todo']}' to : ")

        item['todo'] = change_todo
        todo_dict[select_id] = item
        write_todos(todo_dict)

        print(f"'ToDO' Successfully change! 📝")
    elif chooser == "2":
        print("You want to change 'Date'")
        change_date = input_range(f"Change Date from '{item['date']}' to : ", 1, 31)

        item['date'] = change_date
        todo_dict[select_id] = item
        write_todos(todo_dict)

        print(f"'Date' Successfully change! 📅")
    elif chooser == "3":
        print("You want to change 'Month'")
        change_month = input_range(f"Change 'Month' from '{item['month']}' to : ")

        item['month'] = change_month
        todo_dict[select_id] = item
        write_todos(todo_dict)

        print(f"Month successfully change! 🌑")
    
def delete_todo():
    view_todos()

    todo_dict= read_todos_file()
    select_id = input_range(f"Please select item you want to delete 1-{len(todo_dict)}:",1, len(todo_dict))

    item = todo_dict[select_id]

    while True:
        confirm_delete = input(f"Are you sure want to delete '{item['todo']}' (Y/n)?")
        if confirm_delete.lower() == 'y':
            del todo_dict[select_id]
            write_todos(todo_dict)
            print("Your Item is Deleted!")
            break
        elif confirm_delete.lower() == 'n':
            print("Delete canceled!")
            break
        else:
            print(f"❌ Input is invalid. Please input (Y/n)")


if __name__ == "__main__":
    # MAIN PROGRAM
    clear_screen()
    loading_spinner(1)
    print("\n")
    print_welcome()

    while True:
        show_menu()
        option = input("Please select the option (1-4): ")
        if option == 'q':
            clear_screen()
            loading_spinner(.5)
            print("👋 Goodbye!")
            break
        elif option == '1':
            add_todo()
        elif option == '2':
            clear_screen()
            # print("🔧 Update feature coming soon...")
            update_todo()
        elif option == '3':
            clear_screen()
            # print("🗑️  Delete feature coming soon...")
            delete_todo()
        elif option == '4':
            clear_screen()
            view_todos()
        else:
            print("❌ Invalid input/selection. Try again.")


