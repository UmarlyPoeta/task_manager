import datetime
import json
import random


class Task:
    """
    Represents a task with an id, title, description, creation date, due date, and completion status.

    Methods to modify task details, complete the task, convert to dictionary, and create from dictionary.

    Attributes:
        id: The unique identifier of the task.
        title: The title of the task.
        description: The description of the task.
        created_at: The datetime when the task was created.
        due_date: The datetime when the task is due.
        completed: A boolean indicating if the task is completed.
    """
    
    
    def __init__(self, id: int, title: str, description: str, created_at: datetime.datetime, due_date: datetime.datetime, completed: bool) -> None:
        """
        Initializes a Task object with the provided details.

        Args:
            id: The unique identifier of the task.
            title: The title of the task.
            description: The description of the task.
            created_at: The datetime when the task was created.
            due_date: The datetime when the task is due.
            completed: A boolean indicating if the task is completed.

        Returns:
            None
        """
        
        self.id = id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.due_date = due_date
        self.completed = completed
    
    def change_title(self, new_title: str):
        """
        Changes the title of the task.

        Args:
            new_title: The new title for the task.

        Returns:
            None

        Raises:
            ValueError: If the new title is empty or exceeds 30 characters.
        """
        
        if not new_title or len(new_title) > 30:
            raise ValueError("Invalid length")
        self.title = new_title
    
    def change_description(self, new_description: str):
        """
        Changes the description of the task.

        Args:
            new_description: The new description for the task.

        Returns:
            None

        Raises:
            ValueError: If the new description is empty or exceeds 300 characters.
        """
        
        if not new_description or len(new_description) > 300:
            raise ValueError("Invalid length")
        self. description = new_description
    
    def change_due_date(self, new_due_date: datetime.datetime):
        """
        Changes the due date of the task.

        Args:
            new_due_date: The new due date for the task.

        Returns:
            None

        Raises:
            ValueError: If the new due date is in the past.
        """
        
        if new_due_date > datetime.datetime.now():
            raise ValueError("Due time cannot be set to the past")
        self.due_date = new_due_date
    
    def complete_task(self, completed: bool = True):
        """
        Marks the task as completed or incomplete.

        Args:
            completed: A boolean indicating if the task is completed.

        Returns:
            None
        """
        self.completed = completed
    
    def to_dict(self) -> dict:
        """
        Converts the task details to a dictionary.

        Returns:
            A dictionary containing the task details.
        """
        
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
        """
        Creates a Task object from a dictionary.

        Args:
            data: A dictionary containing task details.

        Returns:
            A Task object created from the dictionary data.
        """
        
        return cls(
            data["id"],
            data["title"],
            data["description"],
            datetime.datetime.fromisoformat(data["created_at"]),
            datetime.datetime.fromisoformat(data["due_date"]),
            data["completed"],
        )
    
    
    def __str__(self) -> str:
        """
        Returns a string representation of the task.

        Returns:
            A string with the task details.
        """
        
        return f"""
                id {self.id},
                title {self.title},
                description {self.description},
                created at {self.created_at},
                due {self.due_date},
                completed: {self.completed}
                """


class TaskManager:
    """
    Manages a collection of tasks, allowing creation, modification, completion, deletion, and storage to a file.

    Methods to create, retrieve, update, complete, delete, list, save, and load tasks.

    Attributes:
        task_list: A list of Task objects managed by the TaskManager.
    """
    
    
    def __init__(self) -> None:
        """
        Initializes a TaskManager object with an empty task list.

        Returns:
            None
        """
        
        self.task_list: list[Task] = []
    
    
    def create_task(self, title: str, description: str, due_date: datetime.datetime) -> Task:
        """
        Creates a new task with the provided details and adds it to the task list.

        Args:
            title: The title of the task.
            description: The description of the task.
            due_date: The due date of the task.

        Returns:
            The created Task object.
        
        Raises:
            ValueError: If the due date is in the past.
        """
        
        due_date = datetime.datetime.fromisoformat(due_date)
        if due_date < datetime.datetime.now():
            raise ValueError("Due time cannot be set to the past")
        task = Task(random.randint(1,100), title, description, datetime.datetime.now(),due_date, False)
        self.task_list.append(task)
        return task
    
    
    def get_task_by_id(self, id: int) -> Task:
        """
        Retrieves a task by its unique identifier.

        Args:
            id: The unique identifier of the task to retrieve.

        Returns:
            The Task object with the specified ID.

        Raises:
            ValueError: If no task exists with the given ID.
        """
        
        for task in self.task_list:
            if task.id == id:
                return task
        raise ValueError("Task with given ID does not exist.")
    
    
    def change_task(self, task_id: int, selected_task_aspect: str, *args) -> None:
        """
        Changes a specific aspect of a task identified by its ID.

        Args:
            task_id: The ID of the task to modify.
            selected_task_aspect: The aspect of the task to change.
            *args: Variable number of arguments based on the selected aspect.

        Returns:
            None

        Raises:
            ValueError: If the task is not found, or if the arguments are invalid.
        """
        
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
    
    def complete_task(self, id:int) -> None:
        """
        Marks a task as completed.

        Args:
            id: The ID of the task to mark as completed.

        Returns:
            None
        """
        
        task_to_complete = self.get_task_by_id(id)
        task_to_complete.completed = True
    
    
    def delete_task(self,id: int) -> None:
        """
        Deletes a task by its ID.

        Args:
            id: The ID of the task to delete.

        Returns:
            None
        """
        
        index_of_the_task_to_delete = [task.id for task in self.task_list].index(id)
        task_to_delete = self.task_list[index_of_the_task_to_delete]
        self.task_list.pop(index_of_the_task_to_delete)
        return task_to_delete
    
    def list_tasks(self) -> None:
        """
        Prints a list of all tasks in the task manager.

        Returns:
            None
        """
        for task in self.task_list:
            print(task)
    
    
    def save_to_file(self, filename: str = "data/database.json") -> None:
        """
        Saves the task manager data to a JSON file.

        Args:
            filename: The name of the file to save the data to.

        Returns:
            None
        """
        
        with open(filename, "w") as file:
            json.dump([task.to_dict() for task in self.task_list], file, indent=4)
    
    def load_from_file(self, filename: str = "data/database.json") -> None:
        """
        Loads task data from a JSON file into the task manager.

        Args:
            filename: The name of the file to load data from.

        Returns:
            None
        """
        
        try:
            with open(filename, "r") as file:
                tasks_data = json.load(file)
                self.task_list = [Task.from_dict(data) for data in tasks_data]
        except FileNotFoundError:
            print(f"No file named {filename} found. Starting with an empty task manager.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the file {filename}. Starting with an empty task manager.")