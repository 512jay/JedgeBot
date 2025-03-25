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
│   │   │   ├── dev_routes.py
│   │   │   ├── http_utils.py
│   │   │   ├── password_reset_routes.py
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── auth_db.py
│   │   │   ├── auth_queries.py
│   │   │   ├── auth_services.py
│   │   │   ├── models.py
│   │   │   ├── password_reset_models.py
│   │   │   ├── password_reset_service.py
│   │   │   ├── schemas.py
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
│   │   ├── main.py
│   │   ├── users
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
│   │   ├── frontend
│   │   │   ├── index.html
│   │   │   ├── src
│   │   │   │   ├── App.jsx.html
│   │   │   │   ├── api
│   │   │   │   │   ├── api_client.js.html
│   │   │   │   │   ├── auth_api.js.html
│   │   │   │   │   ├── index.html
│   │   │   │   ├── components
│   │   │   │   │   ├── DashboardCards.jsx.html
│   │   │   │   │   ├── auth
│   │   │   │   │   │   ├── PrivateRoute.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── layout
│   │   │   │   │   │   ├── LoadingScreen.jsx.html
│   │   │   │   │   │   ├── Sidebar.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── ui
│   │   │   │   │   │   ├── Button.jsx.html
│   │   │   │   │   │   ├── Card.jsx.html
│   │   │   │   │   │   ├── PieChart.jsx.html
│   │   │   │   │   │   ├── Table.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   ├── context
│   │   │   │   │   ├── AuthContext.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   │   ├── index.html
│   │   │   │   ├── main.jsx.html
│   │   │   │   ├── pages
│   │   │   │   │   ├── Dashboard.jsx.html
│   │   │   │   │   ├── ForgotPassword.jsx.html
│   │   │   │   │   ├── Landing.jsx.html
│   │   │   │   │   ├── Login.jsx.html
│   │   │   │   │   ├── Register.jsx.html
│   │   │   │   │   ├── ResetPassword.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   │   ├── routes
│   │   │   │   │   ├── AppRoutes.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   │   ├── test-utils
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── renderWithProviders.jsx.html
│   │   │   │   ├── utils
│   │   │   │   │   ├── apiClient.js.html
│   │   │   │   │   ├── authHelpers.js.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── setupTestUser.js.html
│   │   │   │   ├── views
│   │   │   │   │   ├── ClientDashboard.jsx.html
│   │   │   │   │   ├── EnterpriseDashboard.jsx.html
│   │   │   │   │   ├── FreeDashboard.jsx.html
│   │   │   │   │   ├── ManagerDashboard.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   ├── tailwind.config.js.html
│   │   ├── index.html
│   │   ├── prettify.css
│   │   ├── prettify.js
│   │   ├── sort-arrow-sprite.png
│   │   ├── sorter.js
│   ├── docker-compose.yml
│   ├── docker-entrypoint-initdb.d
│   │   ├── create_auth_db.sql
│   ├── docs
│   │   ├── _current_project_structure.md
│   │   ├── api_password_reset_endpoints.md
│   │   ├── backend_project_structure.md
│   │   ├── business_plan.md
│   │   ├── database
│   │   │   ├── adding_database_table.md
│   │   │   ├── database_schema.md
│   │   ├── development_enviroment.md
│   │   ├── frontend_project_structure.md
│   │   ├── github_workflow.md
│   │   ├── launch_app.md
│   │   ├── legal_strategy.md
│   │   ├── marketing_plan.md
│   │   ├── password_reset.md
│   │   ├── password_reset_index.md
│   │   ├── poetry_workflow.md
│   │   ├── roadmap.md
│   │   ├── test_password_reset_coverage.md
│   │   ├── testing_guide.md
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
│   │   │   │   ├── logo.webp
│   │   │   │   ├── registrationleft.jpg
│   │   │   │   ├── registrationleft.webp
│   │   │   │   ├── welcomejedgebot.jpg
│   │   │   │   ├── welcomejedgebot.webp
│   │   │   ├── vite.svg
│   │   ├── src
│   │   │   ├── App.css
│   │   │   ├── __tests__
│   │   │   │   ├── App.test.jsx
│   │   │   │   ├── main.text.jsx
│   │   │   ├── api
│   │   │   │   ├── api_client.js
│   │   │   ├── assets
│   │   │   │   ├── react.svg
│   │   │   ├── components
│   │   │   │   ├── layout
│   │   │   │   │   ├── LoadingScreen.jsx
│   │   │   │   │   ├── Sidebar.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── Sidebar.test.jsx
│   │   │   │   ├── ui
│   │   │   │   │   ├── Button.jsx
│   │   │   │   │   ├── Card.jsx
│   │   │   │   │   ├── PieChart.jsx
│   │   │   │   │   ├── Table.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── Button.test.jsx
│   │   │   │   │   │   ├── Card.test.jsx
│   │   │   │   │   │   ├── PieChart.test.jsx
│   │   │   │   │   │   ├── Table.test.jsx
│   │   │   ├── context
│   │   │   │   ├── AuthContext.jsx
│   │   │   ├── features
│   │   │   │   ├── app
│   │   │   │   │   ├── App.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── AppLayout.test.jsx
│   │   │   │   ├── auth
│   │   │   │   │   ├── ForgotPassword.jsx
│   │   │   │   │   ├── Login.jsx
│   │   │   │   │   ├── PrivateRoute.jsx
│   │   │   │   │   ├── Register.jsx
│   │   │   │   │   ├── ResetPassword.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── ForgotPassword.test.jsx
│   │   │   │   │   │   ├── Login.test.jsx
│   │   │   │   │   │   ├── Register.test.jsx
│   │   │   │   │   │   ├── ResetPassword.test.jsx
│   │   │   │   │   │   ├── auth_api.test.js
│   │   │   │   │   ├── auth_api.js
│   │   │   │   ├── clients
│   │   │   │   ├── dashboard
│   │   │   │   │   ├── Dashboard.jsx
│   │   │   │   │   ├── DashboardCards.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── Dashboard.test.jsx
│   │   │   │   │   │   ├── DashboardCards.test.jsx
│   │   │   │   │   ├── views
│   │   │   │   │   │   ├── ClientDashboard.jsx
│   │   │   │   │   │   ├── EnterpriseDashboard.jsx
│   │   │   │   │   │   ├── FreeDashboard.jsx
│   │   │   │   │   │   ├── ManagerDashboard.jsx
│   │   │   │   ├── enterprise
│   │   │   │   ├── landing
│   │   │   │   │   ├── Landing.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── Landing.test.jsx
│   │   │   │   ├── settings
│   │   │   ├── index.css
│   │   │   ├── main.jsx
│   │   │   ├── routes
│   │   │   │   ├── AppRoutes.jsx
│   │   │   ├── styles
│   │   │   │   ├── Landing.css
│   │   │   │   ├── Sidebar.css
│   │   │   │   ├── global.css
│   │   │   ├── test-utils
│   │   │   │   ├── renderWithProviders.jsx
│   │   │   │   ├── setup.js
│   │   │   ├── utils
│   │   │   │   ├── __tests__
│   │   │   │   │   ├── api_client.test.js
│   │   │   │   ├── apiClient.js
│   │   │   │   ├── authHelpers.js
│   │   │   │   ├── setupTestUser.js
│   │   ├── tailwind.config.js
│   │   ├── vite.config.js
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
│   │   ├── utils
│   │   │   ├── user_factory.py
│   ├── vitest.config.js
│   ├── x_generate_structure.py
```
