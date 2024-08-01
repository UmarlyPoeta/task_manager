# Task Manager CLI

Task Manager CLI is a simple command-line interface application for managing tasks. It allows you to create, edit, delete, and list tasks. The application is built using the `argparse` library to handle user input.

## Features

- **Add Tasks**: Create new tasks with a title, description, and due date.
- **Remove Tasks**: Delete existing tasks by their ID.
- **Edit Tasks**: Update the title, description, or due date of existing tasks.
- **Complete Tasks**: Mark tasks as completed.
- **List Tasks**: Display all tasks in the system.
- **Save and Load**: Save the task list to a JSON file and load it from a JSON file.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/UmarlyPoeta/task_manager.git
   ```

2. Navigate to the project directory:

   ```bash
   cd task_manager
   ```

3. Install any required dependencies:

## Usage

To use the application, run the following command:

```bash
python cli.py [COMMAND] [OPTIONS]
```

### Examples

1. **Add a Task**:
   ```bash
   python cli.py add "Task Title" "Task Description" "YYYY-MM-DD"
   ```

2. **Remove a Task**:
   ```bash
   python cli.py remove 1
   ```

3. **Edit a Task**:
   ```bash
   python cli.py edit 1 --title "New Title" --description "New Description" --due_date "YYYY-MM-DD"
   ```

4. **List All Tasks**:
   ```bash
   python cli.py list
   ```

5. **Mark a Task as Completed**:
   ```bash
   python cli.py complete 1
   ```

## Contribution

If you'd like to contribute to this project, please fork the repository and submit a pull request. Feel free to open issues for bugs or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
