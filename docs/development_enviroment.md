# Development Environment Setup

## Recommended Stack
- **Python Version**: `>=3.9`
- **Package Management**: `pip + virtualenv` or `poetry`
- **Editor**: VS Code or PyCharm
- **Version Control**: Git (with GitHub)
- **Linting & Formatting**: `black`, `flake8`, `isort`
- **Testing Framework**: `pytest`
- **Logging**: `loguru`
- **Task Automation**: `Makefile`

---

## Environment Setup Steps

### ✅ 1. Create a Virtual Environment
#### Using `venv`:
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```
#### Using `poetry`:
```bash
poetry new jedgebot
cd jedgebot
poetry shell
```

### ✅ 2. Install Required Packages
```bash
pip install requests websockets pandas numpy loguru pytest black flake8 isort
```

### ✅ 3. Set Up Pre-Commit Hooks
To enforce formatting and linting:
```bash
pip install pre-commit
pre-commit install
```

### ✅ 4. Setup `.env` for API Keys (Security Best Practice)
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
