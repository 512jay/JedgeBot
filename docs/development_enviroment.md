# Development Environment Setup

## Recommended Stack
- **Python Version**: `>=3.9,<4.0`
- **Package Management**: `Poetry`
- **Editor**: VS Code or PyCharm
- **Version Control**: Git (with GitHub)
- **Linting & Formatting**: `black`, `flake8`, `isort`
- **Testing Framework**: `pytest`
- **Logging**: `loguru`
- **Task Automation**: `Makefile`

---

## Environment Setup Steps

### ✅ 1. Install Poetry
#### Install Poetry (if not already installed):
```sh
curl -sSL https://install.python-poetry.org | python3 -
```
For Windows (PowerShell):
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Verify installation:
```sh
poetry --version
```

### ✅ 2. Clone the Repository & Set Python Version
```sh
git clone https://github.com/512jay/JedgeBot.git
cd JedgeBot
poetry env use C:\Python\Python311\python.exe
```

### ✅ 3. Remove Existing Virtual Environment (If Necessary)
If you need to start fresh:
```sh
poetry env remove python
```

### ✅ 4. Install Dependencies
```sh
poetry install
```

### ✅ 5. Activate the Virtual Environment
```sh
poetry shell
```
To run commands inside the environment without activating:
```sh
poetry run python jedgebot/main.py
```

### ✅ 6. Set Up Pre-Commit Hooks
To enforce formatting and linting:
```sh
poetry add --dev pre-commit
pre-commit install
```

### ✅ 7. Setup `.env` for API Keys (Security Best Practice)
Create a `.env` file:
```
TASTYTRADE_USERNAME=your_username
TASTYTRADE_PASSWORD=your_password
```
Use `dotenv` in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("TASTYTRADE_USERNAME")
password = os.getenv("TASTYTRADE_PASSWORD")
```

---

## Starting and Stopping Development

### 📌 When You’re Done for the Day
1. Save your changes:
   ```sh
   git add .
   git commit -m "WIP: Trading logic improvements"
   ```
2. Exit the Poetry shell:
   ```sh
   exit
   ```
3. Shut down your terminal.

---

### 📌 How to Start Again the Next Day
1. **Navigate to Your Project**
   ```sh
   cd path/to/JedgeBot
   ```
2. **Activate the Poetry Environment**
   ```sh
   poetry shell
   ```
   If you **don’t** want a shell but just want to run a command inside the environment:
   ```sh
   poetry run python jedgebot/main.py
   ```

---

## 🎯 Final Takeaways
- ✅ **All developers should use Poetry for consistency.**
- ✅ **Commit `pyproject.toml`** so dependencies are tracked.
- ✅ **Decide on `poetry.lock`** (keep for consistency, ignore for flexibility).
- ✅ **Use `poetry shell`** to activate the virtual environment.
- ✅ **Run scripts with `poetry run python`** if you don't want a full shell.
- ✅ **Ignore `.venv/` in Git** (everyone can generate their own virtual environment).

Now, you have a **fully functional Poetry workflow!** 🚀

