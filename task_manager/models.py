import datetime
import json


class Task:
    def __init__(self, id: int, title: str, description: str, created_at: datetime.datetime, due_date: datetime.datetime, completed: bool) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.due_date = due_date
        self.completed = completed
    
    def change_title(self, new_title: str):
        if not new_title or len(new_title) > 30:
            raise ValueError("Invalid length")
        self.title = new_title
    
    def change_description(self, new_description: str):
        if not new_description or len(new_description) > 300:
            raise ValueError("Invalid length")
        self. description = new_description
    
    def change_due_date(self, new_due_date: datetime.datetime):
        if new_due_date > datetime.datetime.now():
            raise ValueError("Due time cannot be set to the past")
        self.due_date = new_due_date
    
    def complete_task(self, completed: bool = True):
        self.completed = completed
    
    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "created_at" : self.created_at.isoformat(),
            "due_date" : self.due_date.isoformat(),
            "completed" : self.completed
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["id"],
            data["title"],
            data["description"],
            datetime.datetime.fromisoformat(data["created_at"]),
            datetime.datetime.fromisoformat(data["due_date"]),
            data["completed"],
        )
    
    
    def __str__(self) -> str:
        return f"id {self.id}, title {self.title}, description {self.description}, created at {self.created_at}, due {self.due_date}, completed: {self.completed}"





class TaskManager:
    _id_counter: int = 0
    
    def __init__(self) -> None:
        self.task_list: list[Task] = []
    
    
    def create_task(self, title: str, description: str, due_date: datetime.datetime) -> object:
        TaskManager._id_counter +=1
        due_date = datetime.datetime.fromisoformat(due_date)
        if due_date < datetime.datetime.now():
            raise ValueError("Due time cannot be set to the past")
        task = Task(TaskManager._id_counter, title, description, datetime.datetime.now(),due_date, False)
        self.task_list.append(task)
        return task
    
    
    def get_task_by_id(self, id: int) -> Task:
        for task in self.task_list:
            if task.id == id:
                return task
        raise ValueError("Task with given ID does not exist.")
    
    
    def change_task(self, task_id: int, selected_task_aspect: str, *args) -> None:
        task = self.get_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found.")

        match selected_task_aspect:
            case "title":
                if len(args) != 1:
                    raise ValueError("Expected a single argument for title.")
                task.change_title(args[0])
            case "description":
                if len(args) != 1:
                    raise ValueError("Expected a single argument for description.")
                task.change_description(args[0])
            case "due_date":
                if len(args) != 1 or not isinstance(args[0], datetime.datetime):
                    raise ValueError("Expected a single datetime argument for due_date.")
                task.change_due_date(args[0])
            case "complete_task":
                if len(args) != 1 or not isinstance(args[0], bool):
                    raise ValueError("Expected a single boolean argument for complete_task.")
                task.complete_task(args[0])
            case _:
                raise ValueError("Invalid task parameter name to change")
    
    def complete_task(self, id:int):
        task_to_complete = self.get_task_by_id(id)
        task_to_complete.completed = True
    
    
    def delete_task(self,id: int) -> None:
        index_of_the_task_to_delete = [task.id for task in self.task_list].index(id)
        task_to_delete = self.task_list[index_of_the_task_to_delete]
        self.task_list.pop(index_of_the_task_to_delete)
        return task_to_delete
    
    def list_tasks(self):
        for task in self.task_list:
            print(task)
    
    
    def save_to_file(self, filename: str = "data/database.json") -> None:
        with open(filename, "w") as file:
            json.dump([task.to_dict() for task in self.task_list], file, indent=4)
    
    def load_from_file(self, filename: str = "data/database.json") -> None:
        try:
            with open(filename, "r") as file:
                tasks_data = json.load(file)
                self.task_list = [Task.from_dict(data) for data in tasks_data]
        except FileNotFoundError:
            print(f"No file named {filename} found. Starting with an empty task manager.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {filename}. Starting with an empty task manager.")