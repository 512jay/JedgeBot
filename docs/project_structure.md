# JedgeBot Project Structure

```
JedgeBot/
│   ├── .flake8
│   ├── LICENSE
│   ├── README.md
│   ├── __init__.py
│   ├── alembic
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   ├── versions
│   ├── alembic.ini
│   ├── backend
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── clients_routes.py
│   │   │   ├── http_utils.py
│   │   │   ├── password_reset_routes.py
│   │   ├── broker
│   │   │   ├── __init__.py
│   │   │   ├── base_broker.py
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
│   │   │   ├── data_fetcher.py
│   │   │   ├── data_processor.py
│   │   │   ├── database
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auth_db.py
│   │   │   │   │   ├── auth_queries.py
│   │   │   │   │   ├── auth_services.py
│   │   │   │   │   ├── models.py
│   │   │   │   │   ├── password_reset_models.py
│   │   │   │   │   ├── password_reset_service.py
│   │   │   │   ├── business
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── initialize_business_db.py
│   │   │   │   ├── market
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── trading_base.py
│   │   │   │   │   ├── trading_database.py
│   │   │   │   │   ├── trading_models.py
│   │   ├── execution
│   │   │   ├── __init__.py
│   │   │   ├── order_manager.py
│   │   ├── main.py
│   │   ├── strategies
│   │   │   ├── __init__.py
│   │   │   ├── arbitrage.py
│   │   │   ├── mean_reversion.py
│   │   │   ├── trend_follow.py
│   │   │   ├── wheel_strategy.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── logging.py
│   │   │   ├── security_utils.py
│   ├── docker-compose.yml
│   ├── docker-entrypoint-initdb.d
│   │   ├── create_auth_db.sql
│   ├── docs
│   │   ├── business_plan.md
│   │   ├── database_schema.md
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
│   │   │   ├── images
│   │   │   │   ├── leftlogin.jpg
│   │   │   │   ├── registrationleft.jpg
│   │   │   │   ├── registrationleft.webp
│   │   │   │   ├── welcomejedgebot.jpg
│   │   │   │   ├── welcomejedgebot.webp
│   │   │   ├── logo.webp
│   │   │   ├── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── App.jsx
│   │   │   ├── api
│   │   │   │   ├── api_client.js
│   │   │   │   ├── auth_api.js
│   │   │   ├── assets
│   │   │   │   ├── react.svg
│   │   │   ├── components
│   │   │   │   ├── DashboardCards.jsx
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
│   │   │   │   ├── Clients.jsx
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── Home.jsx
│   │   │   │   ├── Landing.jsx
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── PortfolioManagerOverview.jsx
│   │   │   │   ├── Profile.jsx
│   │   │   │   ├── Register.jsx
│   │   │   │   ├── ResetPassword.jsx
│   │   │   │   ├── Settings.jsx
│   │   │   ├── styles
│   │   │   │   ├── AccountLevelView.css
│   │   │   │   ├── ClientPortfolioView.css
│   │   │   │   ├── Home.css
│   │   │   │   ├── Landing.css
│   │   │   │   ├── PortfolioManagerOverview.css
│   │   │   │   ├── Sidebar.css
│   │   │   │   ├── global.css
│   │   ├── vite.config.js
│   ├── generate_structure.py
│   ├── jedgebot
│   │   ├── broker
│   │   ├── common
│   │   ├── execution
│   │   ├── utils
│   ├── launch_app.py
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
│   ├── testdb.py
│   ├── tests
│   │   ├── unit
│   │   │   ├── __init__.py
│   │   │   ├── auth
│   │   │   ├── execution
│   │   │   │   ├── test_orders.py
│   │   │   ├── test_base_broker.py
```
