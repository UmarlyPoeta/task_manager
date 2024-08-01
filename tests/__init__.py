import pytest
import datetime
from task_manager.models import Task, TaskManager
import json

@pytest.fixture
def task_manager():
    return TaskManager()

@pytest.fixture
def sample_task():
    return Task(1, "Sample Task", "This is a sample task", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1), False)

@pytest.mark.parametrize("id, title, description, created_at, due_date, completed", [
    (1, "Task 1", "Description 1", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=1), False),
    (2, "Task 2", "Description 2", datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=2), True),
], ids=["task_1", "task_2"])
def test_task_initialization(id, title, description, created_at, due_date, completed):
    # Act
    task = Task(id, title, description, created_at, due_date, completed)

    # Assert
    assert task.id == id
    assert task.title == title
    assert task.description == description
    assert task.created_at == created_at
    assert task.due_date == due_date
    assert task.completed == completed

@pytest.mark.parametrize("new_title, expected_exception", [
    ("New Title", None),
    ("", ValueError),
    ("A" * 31, ValueError),
], ids=["valid_title", "empty_title", "too_long_title"])
def test_change_title(sample_task, new_title, expected_exception):
    # Arrange
    task = sample_task

    # Act and Assert
    if expected_exception:
        with pytest.raises(expected_exception):
            task.change_title(new_title)
    else:
        task.change_title(new_title)
        assert task.title == new_title

@pytest.mark.parametrize("new_description, expected_exception", [
    ("New Description", None),
    ("", ValueError),
    ("A" * 301, ValueError),
], ids=["valid_description", "empty_description", "too_long_description"])
def test_change_description(sample_task, new_description, expected_exception):
    # Arrange
    task = sample_task

    # Act and Assert
    if expected_exception:
        with pytest.raises(expected_exception):
            task.change_description(new_description)
    else:
        task.change_description(new_description)
        assert task.description == new_description

@pytest.mark.parametrize("new_due_date, expected_exception", [
    (datetime.datetime.now() + datetime.timedelta(days=1), None),
    (datetime.datetime.now() - datetime.timedelta(days=1), ValueError),
], ids=["valid_due_date", "past_due_date"])
def test_change_due_date(sample_task, new_due_date, expected_exception):
    # Arrange
    task = sample_task

    # Act and Assert
    if expected_exception:
        with pytest.raises(expected_exception):
            task.change_due_date(new_due_date)
    else:
        task.change_due_date(new_due_date)
        assert task.due_date == new_due_date

def test_complete_task(sample_task):
    # Arrange
    task = sample_task

    # Act
    task.complete_task()

    # Assert
    assert task.completed is True

def test_task_to_dict(sample_task):
    # Arrange
    task = sample_task

    # Act
    task_dict = task.to_dict()

    # Assert
    assert task_dict["id"] == task.id
    assert task_dict["title"] == task.title
    assert task_dict["description"] == task.description
    assert task_dict["created_at"] == task.created_at.isoformat()
    assert task_dict["due_date"] == task.due_date.isoformat()
    assert task_dict["completed"] == task.completed

def test_task_from_dict():
    # Arrange
    task_data = {
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "created_at": datetime.datetime.now().isoformat(),
        "due_date": (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
        "completed": False
    }

    # Act
    task = Task.from_dict(task_data)

    # Assert
    assert task.id == task_data["id"]
    assert task.title == task_data["title"]
    assert task.description == task_data["description"]
    assert task.created_at == datetime.datetime.fromisoformat(task_data["created_at"])
    assert task.due_date == datetime.datetime.fromisoformat(task_data["due_date"])
    assert task.completed == task_data["completed"]

@pytest.mark.parametrize("title, description, due_date, expected_exception", [
    ("Task 1", "Description 1", (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(), None),
    ("Task 2", "Description 2", (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(), ValueError),
], ids=["valid_task", "past_due_date"])
def test_create_task(task_manager, title, description, due_date, expected_exception):
    # Act and Assert
    if expected_exception:
        with pytest.raises(expected_exception):
            task_manager.create_task(title, description, due_date)
    else:
        task = task_manager.create_task(title, description, due_date)
        assert task.title == title
        assert task.description == description
        assert task.due_date == datetime.datetime.fromisoformat(due_date)

def test_get_task_by_id(task_manager, sample_task):
    # Arrange
    task_manager.task_list.append(sample_task)

    # Act
    task = task_manager.get_task_by_id(sample_task.id)

    # Assert
    assert task == sample_task

def test_get_task_by_id_not_found(task_manager):
    # Act and Assert
    with pytest.raises(ValueError):
        task_manager.get_task_by_id(999)

@pytest.mark.parametrize("task_id, selected_task_aspect, args, expected_exception", [
    (1, "title", ["New Title"], None),
    (1, "description", ["New Description"], None),
    (1, "due_date", [datetime.datetime.now() + datetime.timedelta(days=1)], None),
    (1, "complete_task", [True], None),
    (1, "invalid_aspect", ["Invalid"], ValueError),
], ids=["change_title", "change_description", "change_due_date", "complete_task", "invalid_aspect"])
def test_change_task(task_manager, sample_task, task_id, selected_task_aspect, args, expected_exception):
    # Arrange
    task_manager.task_list.append(sample_task)

    # Act and Assert
    if expected_exception:
        with pytest.raises(expected_exception):
            task_manager.change_task(task_id, selected_task_aspect, *args)
    else:
        task_manager.change_task(task_id, selected_task_aspect, *args)
        task = task_manager.get_task_by_id(task_id)
        if selected_task_aspect == "title":
            assert task.title == args[0]
        elif selected_task_aspect == "description":
            assert task.description == args[0]
        elif selected_task_aspect == "due_date":
            assert task.due_date == args[0]
        elif selected_task_aspect == "complete_task":
            assert task.completed == args[0]

def test_complete_task_manager(task_manager, sample_task):
    # Arrange
    task_manager.task_list.append(sample_task)

    # Act
    task_manager.complete_task(sample_task.id)

    # Assert
    assert sample_task.completed is True

def test_delete_task(task_manager, sample_task):
    # Arrange
    task_manager.task_list.append(sample_task)

    # Act
    deleted_task = task_manager.delete_task(sample_task.id)

    # Assert
    assert deleted_task == sample_task
    assert sample_task not in task_manager.task_list

def test_list_tasks(task_manager, sample_task, capsys):
    # Arrange
    task_manager.task_list.append(sample_task)

    # Act
    task_manager.list_tasks()

    # Assert
    captured = capsys.readouterr()
    assert str(sample_task) in captured.out

def test_save_to_file(task_manager, sample_task, tmp_path):
    # Arrange
    task_manager.task_list.append(sample_task)
    file_path = tmp_path / "tasks.json"

    # Act
    task_manager.save_to_file(file_path)

    # Assert
    with open(file_path, "r") as file:
        data = json.load(file)
        assert len(data) == 1
        assert data[0]["id"] == sample_task.id

def test_load_from_file(task_manager, tmp_path):
    # Arrange
    task_data = [{
        "id": 1,
        "title": "Task 1",
        "description": "Description 1",
        "created_at": datetime.datetime.now().isoformat(),
        "due_date": (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
        "completed": False
    }]
    file_path = tmp_path / "tasks.json"
    with open(file_path, "w") as file:
        json.dump(task_data, file)

    # Act
    task_manager.load_from_file(file_path)

    # Assert
    assert len(task_manager.task_list) == 1
    task = task_manager.task_list[0]
    assert task.id == task_data[0]["id"]
    assert task.title == task_data[0]["title"]
    assert task.description == task_data[0]["description"]
    assert task.created_at == datetime.datetime.fromisoformat(task_data[0]["created_at"])
    assert task.due_date == datetime.datetime.fromisoformat(task_data[0]["due_date"])
    assert task.completed == task_data[0]["completed"]
