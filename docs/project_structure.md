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
│   │   │   ├── 73c2de2ee829_fix_password_reset_table_base.py
│   │   │   ├── ac6a215aa1f4_include_password_reset_token_table.py
│   │   │   ├── ef329bc9120d_initial_auth_schema_with_role_column.py
│   │   │   ├── f6df294f76d5_add_cascade_delete_to_password_reset_.py
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
│   │   ├── core
│   │   │   ├── rate_limit.py
│   │   │   ├── settings.py
│   │   ├── data
│   │   │   ├── __init__.py
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
│   │   ├── main.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── logging.py
│   │   │   ├── security_utils.py
│   ├── check_db_env.py
│   ├── coverage
│   │   ├── base.css
│   │   ├── block-navigation.js
│   │   ├── clover.xml
│   │   ├── coverage-final.json
│   │   ├── favicon.png
│   │   ├── index.html
│   │   ├── prettify.css
│   │   ├── prettify.js
│   │   ├── sort-arrow-sprite.png
│   │   ├── sorter.js
│   │   ├── src
│   │   │   ├── App.jsx.html
│   │   │   ├── api
│   │   │   │   ├── api_client.js.html
│   │   │   │   ├── auth_api.js.html
│   │   │   │   ├── index.html
│   │   │   ├── components
│   │   │   │   ├── DashboardCards.jsx.html
│   │   │   │   ├── Navbar.jsx.html
│   │   │   │   ├── Sidebar.jsx.html
│   │   │   │   ├── TitleManager.jsx.html
│   │   │   │   ├── index.html
│   │   │   │   ├── ui
│   │   │   │   │   ├── Button.jsx.html
│   │   │   │   │   ├── Card.jsx.html
│   │   │   │   │   ├── PieChart.jsx.html
│   │   │   │   │   ├── Table.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   ├── index.html
│   │   │   ├── main.jsx.html
│   │   │   ├── pages
│   │   │   │   ├── AccountLevelView.jsx.html
│   │   │   │   ├── ClientPortfolioView.jsx.html
│   │   │   │   ├── Clients.jsx.html
│   │   │   │   ├── Dashboard.jsx.html
│   │   │   │   ├── ForgotPassword.jsx.html
│   │   │   │   ├── Home.jsx.html
│   │   │   │   ├── Landing.jsx.html
│   │   │   │   ├── Login.jsx.html
│   │   │   │   ├── PortfolioManagerOverview.jsx.html
│   │   │   │   ├── Profile.jsx.html
│   │   │   │   ├── Register.jsx.html
│   │   │   │   ├── ResetPassword.jsx.html
│   │   │   │   ├── Settings.jsx.html
│   │   │   │   ├── index.html
│   ├── docker-compose.yml
│   ├── docker-entrypoint-initdb.d
│   │   ├── create_auth_db.sql
│   ├── docs
│   │   ├── api_password_reset_endpoints.md
│   │   ├── business_plan.md
│   │   ├── database_schema.md
│   │   ├── development_enviroment.md
│   │   ├── github_workflow.md
│   │   ├── legal_strategy.md
│   │   ├── marketing_plan.md
│   │   ├── password_reset.md
│   │   ├── password_reset_index.md
│   │   ├── poetry_workflow.md
│   │   ├── project_structure.md
│   │   ├── roadmap.md
│   │   ├── test_password_reset_coverage.md
│   │   ├── testing_strategy.md
│   ├── frontend
│   │   ├── .vite
│   │   │   ├── deps
│   │   │   │   ├── _metadata.json
│   │   │   │   ├── package.json
│   │   ├── README.md
│   │   ├── eslint.config.js
│   │   ├── index.html
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
│   │   │   ├── __tests__
│   │   │   │   ├── ForgotPassword.test.jsx
│   │   │   │   ├── Login.test.jsx
│   │   │   │   ├── Register.test.jsx
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
│   │   │   │   ├── ForgotPassword.jsx
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
│   │   ├── test-utils
│   │   │   ├── setup.js
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
│   │   ├── run_rate_limit_manual.py
│   │   ├── start_market_data_stream.py
│   │   ├── validate_output.py
│   ├── tests
│   │   ├── conftest.py
│   │   ├── integration
│   │   │   ├── __init__.py
│   │   │   ├── auth
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_auth_services.py
│   │   │   │   ├── test_password_reset_flow.py
│   │   │   │   ├── test_password_reset_token_validation.py
│   │   ├── unit
│   │   │   ├── __init__.py
│   │   │   ├── auth
│   │   │   │   ├── test_auth_routes.py
│   │   │   ├── test_base_broker.py
│   ├── vitest.config.js
```
