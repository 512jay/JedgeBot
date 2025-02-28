# Poetry Workflow for JedgeBot

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

## Installing Dependencies After Cloning
If you **clone the repo** on another machine (or for a collaborator):
```sh
 git clone https://github.com/512jay/JedgeBot.git
 cd JedgeBot
 poetry install
 poetry shell
```

---

## 🎯 Final Takeaways
- ✅ **Commit `pyproject.toml`** so dependencies are tracked.
- ✅ **Decide on `poetry.lock`** (keep for consistency, ignore for flexibility).
- ✅ **Use `poetry shell`** to activate the virtual environment.
- ✅ **Run scripts with `poetry run python`** if you don't want a full shell.
- ✅ **Ignore `.venv/` in Git** (everyone can generate their own).

Now, you have a **fully functional Poetry workflow!** 🚀

