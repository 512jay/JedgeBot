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
│   │   │   ├── 04553e1d9a84_add_is_email_verified_and_email_.py
│   │   │   ├── 6f28cb8d274e_create_password_reset_tokens_table.py
│   │   │   ├── a1e3e950dc21_create_user_profiles_table.py
│   │   │   ├── a3f1add06d8a_add_is_email_verified.py
│   │   │   ├── ce2eb894601a_upgrade_password_reset_tokens_table_to_.py
│   ├── alembic.ini
│   ├── backend
│   │   ├── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── clients_routes.py
│   │   │   ├── http_utils.py
│   │   ├── auth
│   │   │   ├── __init__.py
│   │   │   ├── auth_models.py
│   │   │   ├── auth_queries.py
│   │   │   ├── auth_routes.py
│   │   │   ├── auth_schemas.py
│   │   │   ├── auth_services.py
│   │   │   ├── constants.py
│   │   │   ├── dependencies.py
│   │   │   ├── password
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── routes.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   ├── tests
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── test_password_reset_service.py
│   │   │   ├── tests
│   │   │   │   ├── test_auth_routes.py
│   │   │   │   ├── test_auth_services.py
│   │   │   │   ├── test_dependencies.py
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
│   │   │   │   ├── base.py
│   │   │   │   ├── db.py
│   │   │   │   ├── models.py
│   │   ├── dev
│   │   │   ├── __init__.py
│   │   │   ├── cleanup.py
│   │   │   ├── roadmaps
│   │   │   │   ├── auth_roadmap.md
│   │   │   │   ├── completed
│   │   │   │   │   ├── email_verification_roadmap.md
│   │   │   ├── routes.py
│   │   ├── main.py
│   │   ├── notifications
│   │   │   ├── email_service.py
│   │   ├── user
│   │   │   ├── __init__.py
│   │   │   ├── user_models.py
│   │   │   ├── user_routes.py
│   │   │   ├── user_schemas.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── logging.py
│   │   │   ├── security_utils.py
│   ├── check_db_env.py
│   ├── conftest.py
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
│   │   ├── dev
│   │   │   ├── roadmaps
│   │   │   │   ├── Dashboar_Role_Routing.md
│   │   │   │   ├── completed
│   │   │   │   │   ├── email_verification_frontend.md
│   │   │   │   ├── ut_roadmap.md
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
│   │   │   ├── __tests__
│   │   │   │   ├── main.text.jsx
│   │   │   ├── api
│   │   │   │   ├── api_client.js
│   │   │   ├── assets
│   │   │   │   ├── react.svg
│   │   │   ├── components
│   │   │   │   ├── common
│   │   │   │   │   ├── ToastMessage.jsx
│   │   │   │   ├── layout
│   │   │   │   │   ├── LoadingScreen.jsx
│   │   │   │   │   ├── Sidebar.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   ├── routing
│   │   │   │   │   ├── PrivateRoute.jsx
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
│   │   │   │   ├── useAuth.js
│   │   │   ├── features
│   │   │   │   ├── app
│   │   │   │   │   ├── App.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── App.test.jsx
│   │   │   │   │   │   ├── AppLayout.test.jsx
│   │   │   │   ├── auth
│   │   │   │   │   ├── ForgotPassword.jsx
│   │   │   │   │   ├── Login.jsx
│   │   │   │   │   ├── Register.jsx
│   │   │   │   │   ├── ResetPassword.jsx
│   │   │   │   │   ├── VerifyEmail.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── ForgotPassword.test.jsx
│   │   │   │   │   │   ├── Login.test.jsx
│   │   │   │   │   │   ├── Register.test.jsx
│   │   │   │   │   │   ├── auth_api.test.js
│   │   │   │   │   ├── auth_api.js
│   │   │   │   ├── clients
│   │   │   │   ├── dashboard
│   │   │   │   │   ├── Dashboard.jsx
│   │   │   │   │   ├── DashboardCards.jsx
│   │   │   │   │   ├── __tests__
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
│   ├── psql_connect.sh
│   ├── pyproject.toml
│   ├── python
│   ├── run.py
│   ├── run_maintenance.py
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
│   │   ├── cleanup_test_users.py
│   │   ├── run_rate_limit_manual.py
│   │   ├── start_market_data_stream.py
│   │   ├── validate_output.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── integration
│   │   │   ├── __init__.py
│   │   │   ├── auth
│   │   │   │   ├── __init__.py
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   ├── user_factory.py
│   ├── vitest.config.js
│   ├── x_generate_structure.py
```
