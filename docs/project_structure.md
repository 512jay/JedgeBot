# JedgeBot Project Structure

```
JedgeBot/
│   ├── .flake8
│   ├── LICENSE
│   ├── README.md
│   ├── __init__.py
│   ├── backend
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── main.py
│   │   │   ├── request_utils.py
│   │   ├── broker
│   │   │   ├── __init__.py
│   │   │   ├── broker_api.py
│   │   │   ├── tastytrade
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data_handler.py
│   │   │   │   ├── services
│   │   │   │   │   ├── account.py
│   │   │   │   │   ├── account_streaming.py
│   │   │   │   │   ├── api_client.py
│   │   │   │   │   ├── authentication.py
│   │   │   │   │   ├── customer.py
│   │   │   │   │   ├── market_data_streaming.py
│   │   │   │   │   ├── order.py
│   │   │   │   │   ├── quote_token_manager.py
│   │   │   │   ├── tastytrade.py
│   │   │   │   ├── utilities.py
│   │   ├── common
│   │   │   ├── __init__.py
│   │   │   ├── enums.py
│   │   ├── data
│   │   │   ├── __init__.py
│   │   │   ├── auth.db
│   │   │   ├── data_fetcher.py
│   │   │   ├── data_processor.py
│   │   ├── execution
│   │   │   ├── __init__.py
│   │   │   ├── orders.py
│   │   ├── strategies
│   │   │   ├── __init__.py
│   │   │   ├── arbitrage.py
│   │   │   ├── mean_reversion.py
│   │   │   ├── trend_follow.py
│   │   │   ├── wheel_strategy.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── logging.py
│   ├── data
│   │   ├── auth.db
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
│   ├── frontend
│   │   ├── .vite
│   │   │   ├── deps
│   │   │   │   ├── _metadata.json
│   │   │   │   ├── package.json
│   │   ├── README.md
│   │   ├── eslint.config.js
│   │   ├── index.html
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── public
│   │   │   ├── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── App.jsx
│   │   │   ├── api
│   │   │   │   ├── auth.js
│   │   │   ├── api.jsx
│   │   │   ├── assets
│   │   │   │   ├── react.svg
│   │   │   ├── components
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── TitleManager.jsx
│   │   │   │   ├── ui
│   │   │   │   │   ├── Button.jsx
│   │   │   │   │   ├── Card.jsx
│   │   │   │   │   ├── PieChart.jsx
│   │   │   │   │   ├── Table.jsx
│   │   │   ├── index.css
│   │   │   ├── main.jsx
│   │   │   ├── pages
│   │   │   │   ├── AccountLevelView.jsx
│   │   │   │   ├── ClientPortfolioView.jsx
│   │   │   │   ├── Home.jsx
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── LoginRegister.jsx
│   │   │   │   ├── PortfolioManagerOverview.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   ├── ResetPassword.jsx
│   │   │   ├── styles
│   │   │   │   ├── AccountLevelView.css
│   │   │   │   ├── ClientPortfolioView.css
│   │   │   │   ├── Home.css
│   │   │   │   ├── PortfolioManagerOverview.css
│   │   │   │   ├── Sidebar.css
│   │   ├── vite.config.js
│   ├── generate_structure.py
│   ├── jedgebot
│   │   ├── broker
│   │   ├── common
│   │   ├── execution
│   │   ├── utils
│   ├── logs
│   ├── notes
│   │   ├── PortfolioManagmentRoadMap.md
│   ├── package-lock.json
│   ├── package.json
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── python
│   ├── run.py
│   ├── scripts
│   │   ├── __init__.py
│   │   ├── archive
│   │   │   ├── __init__.py
│   │   │   ├── account_info.py
│   │   │   ├── account_stream.py
│   │   │   ├── balances.py
│   │   │   ├── get_first_account_number.py
│   │   │   ├── market_data_stream_script_1.py
│   │   │   ├── market_data_streaming_script.py
│   │   │   ├── start_streaming.py
│   │   ├── btc_stream.py
│   │   ├── start_market_data_stream.py
│   ├── start_jedgebot.py
│   ├── tests
│   │   ├── unit
│   │   │   ├── __init__.py
│   │   │   ├── execution
│   │   │   │   ├── test_orders.py
│   │   │   ├── test_base_broker.py
```
