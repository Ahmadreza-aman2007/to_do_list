import json


class TASK:

    def __init__(self, name: str, explanation: str, status: bool):
        self.name = name
        self.explanation = explanation
        self.status = status

    def show_the_task(self):
        status = "done" if self.status else "not done"
        print(f"""
name: {self.name}

explanation:
{self.explanation}

status: {status}
""")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "explanation": self.explanation,
            "status": self.status,
        }

    @classmethod
    def dict_to_task(cls, d: dict):
        return TASK(d["name"], d["explanation"], d["status"])


def load() -> list[TASK]:
    tasks: list[TASK] = []
    try:
        with open("tasks.json", "r") as file:
            l = json.load(file)
            for task in l:
                tasks.append(TASK.dict_to_task(task))
        return tasks
    except Exception as e:
        print(f"error in loading tasks{e} start with empty list")
        return []


def save(tasks: list[TASK]):
    t = []
    for task in tasks:
        t.append(task.to_dict())
    try:
        with open("tasks.json", "w") as file:
            json.dump(t, file, indent=4)
    except Exception as e:
        print(f"error in saving tasks{e}")


def show_menu():
    print("""
1:see tasks
2:add a new task
3:remove a task
4:edit status of a task
5:exit
(please enter the number)
""")


def is_task_exist(tasks: list[TASK], task_name: str) -> bool:
    for task in tasks:
        if task.name == task_name:
            return True
    return False


def add_a_task(tasks: list[TASK]):
    while True:
        name = input("enter the task's name (for back to menu enter $menu$ )").strip()
        if not name:
            print("this filed can't be empty")
            continue
        if name == "$menu$":
            return
        if is_task_exist(tasks, name):
            print("please enter a new name(this name already exist)")
            continue
        explanation = input(
            "enter the task's explanation (for back to menu enter $menu$ )"
        ).strip()
        if explanation == "$menu$":
            return
        tasks.append(TASK(name, explanation, False))
        save(tasks)
        print("your task saved successfully")


def remove_a_task(tasks: list[TASK]):
    if not tasks:
        print("there is no task to remove")
        return
    for i in range(0, len(tasks)):
        print(f"{i+1} : {tasks[i].name} ")
    print("for delete a task enter 'del [task number]' ")
    print("for see a task enter 'show [task number]' ")
    print("for back to menu enter $menu$")
    while True:
        order = input().strip()
        if order == "$menu$":
            return
        order = order.split(" ")
        if len(order) != 2:
            print("command not found")
            continue
        if order[0] == "del":
            try:
                choice = int(order[1])
                if choice > len(tasks) or choice <= 0:
                    print("please enter a valid number")
                    continue
                tasks.pop(choice - 1)
                print("your task removed successfully")
                save(tasks)
                tasks = load()
            except ValueError:
                print("command not found")
        elif order[0] == "show":
            try:
                choice = int(order[1])
                show_specific_task(tasks, choice - 1)
            except ValueError:
                print("command not found")


def show_specific_task(tasks: list[TASK], index: int):
    if 0 <= index < len(tasks):
        tasks[index].show_the_task()
    else:
        print("⚠️ Invalid index")


def edit_a_task(tasks: list[TASK]):
    if not tasks:
        print("there is no task to remove")
        return
    for i in range(0, len(tasks)):
        print(f"{i+1} : {tasks[i].name} ")
    print("for edit a task enter 'edit [task number]' ")
    print("for see a task enter 'show [task number]' ")
    print("for back to menu enter $menu$")
    while True:
        order = input().strip()
        if order == "$menu$":
            return
        order = order.split(" ")
        if len(order) != 2:
            print("command not found")
            continue
        if order[0] == "edit":
            try:
                choice = int(order[1])
                if choice > len(tasks) or choice <= 0:
                    print("please enter a valid number")
                    continue
                p = input(
                    "enter on of these for edit (name,explanation,status)"
                ).strip()
                while True:
                    if p == "status":
                        tasks[choice - 1].status = not tasks[choice - 1].status
                        break
                    elif p == "name":
                        while True:
                            name = input(
                                "please enter the new name (for back to menu enter $menu$ )"
                            )
                            if name == "$menu$":
                                return
                            if not name:
                                print("this field can't be empty")
                                continue
                            if is_task_exist(tasks, name):
                                print("this name already exist")
                                continue
                            tasks[choice - 1].name = name
                            break
                        break
                    elif p == "explanation":
                        e = input(
                            "please enter the new explanation(for back to menu enter $menu$ )"
                        )
                        if e == "$menu$":
                            return
                        tasks[choice - 1].explanation = e
                        break
                    else:
                        print("please enter a valid word")
                print("your task edited successfully")
                save(tasks)
                tasks = load()
            except ValueError:
                print("command not found")
        elif order[0] == "show":
            try:
                choice = int(order[1])
                show_specific_task(tasks, choice - 1)
            except ValueError:
                print("command not found")


def main() -> None:
    print("""
|            welcome to TO_DO_LIST           |
|                .............               |

""")
    tasks: list[TASK] = []
    while True:
        tasks = load()
        show_menu()
        try:
            choice = int(input("enter your choice").strip())
        except ValueError:
            print("please enter a number")
            continue
        if choice > 5:
            print("please enter a valid number")
        elif choice == 5:
            return
        elif choice == 1:
            if not tasks:
                print("there is no task here")
            else:
                for task in tasks:
                    task.show_the_task()
        elif choice == 2:
            add_a_task(tasks)
        elif choice == 3:
            remove_a_task(tasks)
        elif choice == 4:
            edit_a_task(tasks)


if __name__ == "__main__":
    main()
