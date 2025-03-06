# JedgeBot Project Structure

```
JedgeBot/
│   ├── LICENSE
│   ├── README.md
│   ├── __init__.py
│   ├── docs
│   │   ├── business_plan.md
│   │   ├── development_enviroment.md
│   │   ├── github_workflow.md
│   │   ├── legal_strategy.md
│   │   ├── marketing_plan.md
│   │   ├── poetry_workflow.md
│   │   ├── project_structure.md
│   │   ├── roadmap.md
│   │   ├── testing_strategy.md
│   ├── generate_structure.py
│   ├── jedgebot
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── request_utils.py
│   │   ├── broker
│   │   │   ├── __init__.py
│   │   │   ├── base_broker.py
│   │   │   ├── tastytrade
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data_handler.py
│   │   │   │   ├── services
│   │   │   │   │   ├── account.py
│   │   │   │   │   ├── api_client.py
│   │   │   │   │   ├── authentication.py
│   │   │   │   │   ├── customer.py
│   │   │   │   │   ├── market_data.py
│   │   │   │   │   ├── order.py
│   │   │   │   ├── tastytrade.py
│   │   ├── config
│   │   │   ├── settings.py
│   │   ├── config.toml
│   │   ├── data
│   │   │   ├── __init__.py
│   │   │   ├── data_fetcher.py
│   │   │   ├── data_processor.py
│   │   ├── execution
│   │   │   ├── __init__.py
│   │   │   ├── order_manager.py
│   │   │   ├── risk_manager.py
│   │   │   ├── trade_monitor.py
│   │   ├── strategies
│   │   │   ├── __init__.py
│   │   │   ├── arbitrage.py
│   │   │   ├── mean_reversion.py
│   │   │   ├── trend_follow.py
│   │   │   ├── wheel_strategy.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── logging_utils.py
│   ├── log_setup.py
│   ├── logs
│   ├── notes
│   │   ├── OpenBB.md
│   │   ├── PortfolioManagmentRoadMap.md
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── run.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── account_info.py
│   │   ├── account_stream.py
│   │   ├── balances.py
│   │   ├── get_first_account_number.py
│   │   ├── logs
│   ├── tests
│   │   ├── unit
│   │   │   ├── __init__.py
│   │   │   ├── test_base_broker.py
```
