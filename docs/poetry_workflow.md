# Poetry Quick Reference for JedgeBot

## 📌 Daily Development Workflow

### ✅ Starting Work
1. **Navigate to the project:**
   ```sh
   cd path/to/JedgeBot
   ```
2. **Activate the Poetry Environment:**
   ```sh
   poetry shell
   ```
3. **Run the application:**
   ```sh
   poetry run python jedgebot/main.py
   ```

---

### ✅ Ending Work for the Day
1. **Save changes:**
   ```sh
   git add .
   git commit -m "WIP: Development updates"
   ```
2. **Exit the Poetry shell:**
   ```sh
   exit
   ```
3. **Shut down your terminal.**

---

## 📌 Setting Up Poetry (First-Time Setup)
1. **Install Poetry (if not already installed):**
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   For Windows (PowerShell):
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```
2. **Clone the repository and install dependencies:**
   ```sh
   git clone https://github.com/512jay/JedgeBot.git
   cd JedgeBot
   poetry install
   ```

---

## 📌 Handling Dependencies
- **Install a new dependency:**
  ```sh
  poetry add package_name
  ```
- **Install a development dependency:**
  ```sh
  poetry add --dev package_name
  ```
- **Remove a dependency:**
  ```sh
  poetry remove package_name
  ```
- **Update dependencies:**
  ```sh
  poetry update
  ```

---

## 📌 Final Takeaways
- ✅ **Commit `pyproject.toml`** to track dependencies.
- ✅ **Decide on `poetry.lock`** (keep for consistency, ignore for flexibility).
- ✅ **Use `poetry shell`** for activating the virtual environment.
- ✅ **Run scripts with `poetry run python`** if you don’t want a full shell.
- ✅ **Ignore `.venv/` in Git** (everyone can generate their own virtual environment).

This guide provides a **quick reference** for working with Poetry in JedgeBot! 🚀

