# Project Directory Structure

```
JedgeBot/                # Root project folder
│── jedgebot/            # Main Python package
│   ├── __init__.py      # Marks this as a package
│   ├── main.py          # Main bot logic
│   ├── brokers/         # Broker API interactions
│   ├── config/          # Configuration files
│   ├── execution/       # Order execution logic
│   ├── strategies/      # Trading strategies
│   ├── data/            # Market data processing
│   ├── logs/            # Logging system
│── docs/                # Documentation
│── tests/               # Unit tests
│── scripts/             # Utility scripts (optional)
│── .venv/               # Virtual environment (ignored in Git)
│── .gitignore           # Ignore unnecessary files
│── .env                 # API keys & secrets (DO NOT COMMIT)
│── LICENSE              # Open-source license
│── README.md            # Project description
│── poetry.lock          # Locked dependencies
│── pyproject.toml       # Poetry config & dependencies

```

## Folder Descriptions

- **brokers/**: Integration modules for various brokers (e.g., TastyTrade, Interactive Brokers).
- **config/**: Configuration files and settings.
- **data/**: Storage for datasets and logs.
- **docs/**: Project documentation.
- **execution/**: Order execution logic and related utilities.
- **strategies/**: Trading strategy implementations.
- **tests/**: Unit and integration tests.

## File Descriptions

- **.gitignore**: Specifies files and directories to be ignored by Git.
- **LICENSE**: The project's license information.
- **README.md**: Overview and setup instructions for JedgeBot.
- **main.py**: The main entry point for the bot.
- **requirements.txt**: List of Python dependencies.

---
