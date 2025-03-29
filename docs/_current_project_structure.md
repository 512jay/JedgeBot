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
│   ├── coverage
│   │   ├── base.css
│   │   ├── block-navigation.js
│   │   ├── clover.xml
│   │   ├── coverage-final.json
│   │   ├── favicon.png
│   │   ├── frontend
│   │   │   ├── index.html
│   │   │   ├── src
│   │   │   │   ├── api
│   │   │   │   │   ├── api_client.js.html
│   │   │   │   │   ├── index.html
│   │   │   │   ├── components
│   │   │   │   │   ├── common
│   │   │   │   │   │   ├── ToastMessage.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── layout
│   │   │   │   │   │   ├── LoadingScreen.jsx.html
│   │   │   │   │   │   ├── Sidebar.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── layouts
│   │   │   │   │   │   ├── DashboardLayout.jsx.html
│   │   │   │   │   │   ├── PublicLayout.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── routing
│   │   │   │   │   │   ├── PrivateRoute.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── ui
│   │   │   │   │   │   ├── Button.jsx.html
│   │   │   │   │   │   ├── Card.jsx.html
│   │   │   │   │   │   ├── PieChart.jsx.html
│   │   │   │   │   │   ├── Table.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   ├── context
│   │   │   │   │   ├── AuthProvider.jsx.html
│   │   │   │   │   ├── auth-context.js.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── useAuth.js.html
│   │   │   │   ├── features
│   │   │   │   │   ├── app
│   │   │   │   │   │   ├── App.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── pages
│   │   │   │   │   │   │   ├── NotFound.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── auth
│   │   │   │   │   │   ├── ForgotPassword.jsx.html
│   │   │   │   │   │   ├── Login.jsx.html
│   │   │   │   │   │   ├── Register.jsx.html
│   │   │   │   │   │   ├── ResetPassword.jsx.html
│   │   │   │   │   │   ├── VerifyEmail.jsx.html
│   │   │   │   │   │   ├── auth_api.js.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── dashboard
│   │   │   │   │   │   ├── Dashboard.jsx.html
│   │   │   │   │   │   ├── DashboardCards.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── views
│   │   │   │   │   │   │   ├── ClientDashboard.jsx.html
│   │   │   │   │   │   │   ├── EnterpriseDashboard.jsx.html
│   │   │   │   │   │   │   ├── FreeDashboard.jsx.html
│   │   │   │   │   │   │   ├── ManagerDashboard.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── landing
│   │   │   │   │   │   ├── About.jsx.html
│   │   │   │   │   │   ├── Contact.jsx.html
│   │   │   │   │   │   ├── Landing.jsx.html
│   │   │   │   │   │   ├── Pricing.jsx.html
│   │   │   │   │   │   ├── WaitlistForm.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   ├── index.html
│   │   │   │   ├── main.jsx.html
│   │   │   │   ├── routes
│   │   │   │   │   ├── AppRoutes.jsx.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── routes.js.html
│   │   │   │   ├── test-utils
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── renderWithProviders.jsx.html
│   │   │   │   ├── utils
│   │   │   │   │   ├── apiClient.js.html
│   │   │   │   │   ├── authHelpers.js.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── setupTestUser.js.html
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
│   │   ├── auth_roadmap.md
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
│   │   ├── coverage
│   │   │   ├── base.css
│   │   │   ├── block-navigation.js
│   │   │   ├── clover.xml
│   │   │   ├── coverage-final.json
│   │   │   ├── favicon.png
│   │   │   ├── frontend
│   │   │   │   ├── index.html
│   │   │   │   ├── src
│   │   │   │   │   ├── api
│   │   │   │   │   │   ├── api_client.js.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── components
│   │   │   │   │   │   ├── common
│   │   │   │   │   │   │   ├── ToastMessage.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── layout
│   │   │   │   │   │   │   ├── LoadingScreen.jsx.html
│   │   │   │   │   │   │   ├── Sidebar.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── layouts
│   │   │   │   │   │   │   ├── DashboardLayout.jsx.html
│   │   │   │   │   │   │   ├── PublicLayout.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── routing
│   │   │   │   │   │   │   ├── PrivateRoute.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── ui
│   │   │   │   │   │   │   ├── Button.jsx.html
│   │   │   │   │   │   │   ├── Card.jsx.html
│   │   │   │   │   │   │   ├── PieChart.jsx.html
│   │   │   │   │   │   │   ├── Table.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── context
│   │   │   │   │   │   ├── AuthProvider.jsx.html
│   │   │   │   │   │   ├── auth-context.js.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── useAuth.js.html
│   │   │   │   │   ├── features
│   │   │   │   │   │   ├── app
│   │   │   │   │   │   │   ├── App.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   │   ├── pages
│   │   │   │   │   │   │   │   ├── NotFound.jsx.html
│   │   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── auth
│   │   │   │   │   │   │   ├── ForgotPassword.jsx.html
│   │   │   │   │   │   │   ├── Login.jsx.html
│   │   │   │   │   │   │   ├── Register.jsx.html
│   │   │   │   │   │   │   ├── ResetPassword.jsx.html
│   │   │   │   │   │   │   ├── VerifyEmail.jsx.html
│   │   │   │   │   │   │   ├── auth_api.js.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── dashboard
│   │   │   │   │   │   │   ├── Dashboard.jsx.html
│   │   │   │   │   │   │   ├── DashboardCards.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   │   ├── views
│   │   │   │   │   │   │   │   ├── ClientDashboard.jsx.html
│   │   │   │   │   │   │   │   ├── EnterpriseDashboard.jsx.html
│   │   │   │   │   │   │   │   ├── FreeDashboard.jsx.html
│   │   │   │   │   │   │   │   ├── ManagerDashboard.jsx.html
│   │   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── landing
│   │   │   │   │   │   │   ├── About.jsx.html
│   │   │   │   │   │   │   ├── Contact.jsx.html
│   │   │   │   │   │   │   ├── Landing.jsx.html
│   │   │   │   │   │   │   ├── Pricing.jsx.html
│   │   │   │   │   │   │   ├── WaitlistForm.jsx.html
│   │   │   │   │   │   │   ├── index.html
│   │   │   │   │   ├── index.html
│   │   │   │   │   ├── main.jsx.html
│   │   │   │   │   ├── routes
│   │   │   │   │   │   ├── AppRoutes.jsx.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── routes.js.html
│   │   │   │   │   ├── test-utils
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── renderWithProviders.jsx.html
│   │   │   │   │   │   ├── setup.js.html
│   │   │   │   │   ├── utils
│   │   │   │   │   │   ├── apiClient.js.html
│   │   │   │   │   │   ├── authHelpers.js.html
│   │   │   │   │   │   ├── index.html
│   │   │   │   │   │   ├── setupTestUser.js.html
│   │   │   │   ├── tailwind.config.js.html
│   │   │   ├── index.html
│   │   │   ├── prettify.css
│   │   │   ├── prettify.js
│   │   │   ├── sort-arrow-sprite.png
│   │   │   ├── sorter.js
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
│   │   │   │   ├── layouts
│   │   │   │   │   ├── DashboardLayout.jsx
│   │   │   │   │   ├── Footer.jsx
│   │   │   │   │   ├── Header.jsx
│   │   │   │   │   ├── LoadingScreen.jsx
│   │   │   │   │   ├── PublicLayout.jsx
│   │   │   │   │   ├── Sidebar.jsx
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
│   │   │   │   ├── AuthProvider.jsx
│   │   │   │   ├── auth-context.js
│   │   │   │   ├── useAuth.js
│   │   │   ├── features
│   │   │   │   ├── app
│   │   │   │   │   ├── App.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── App.test.jsx
│   │   │   │   │   ├── pages
│   │   │   │   │   │   ├── NotFound.jsx
│   │   │   │   ├── auth
│   │   │   │   │   ├── ForgotPassword.jsx
│   │   │   │   │   ├── Login.jsx
│   │   │   │   │   ├── Register.jsx
│   │   │   │   │   ├── ResetPassword.jsx
│   │   │   │   │   ├── VerifyEmail.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── ForgotPassword.test.jsx
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
│   │   │   │   │   ├── About.jsx
│   │   │   │   │   ├── Contact.jsx
│   │   │   │   │   ├── Landing.jsx
│   │   │   │   │   ├── Pricing.jsx
│   │   │   │   │   ├── WaitlistForm.jsx
│   │   │   │   │   ├── __tests__
│   │   │   │   │   │   ├── Landing.test.jsx
│   │   │   │   ├── profile
│   │   │   │   │   ├── Profile.jsx
│   │   │   │   ├── settings
│   │   │   ├── images
│   │   │   │   ├── 404.png
│   │   │   │   ├── about.jpg
│   │   │   │   ├── contact.jpg
│   │   │   │   ├── hero
│   │   │   │   │   ├── contact.jpg
│   │   │   │   │   ├── forgot.jpg
│   │   │   │   │   ├── landing.jpg
│   │   │   │   │   ├── leftlogin.jpg
│   │   │   │   │   ├── login.webp
│   │   │   │   │   ├── register.jpg
│   │   │   │   │   ├── welcomejedgebot.jpg
│   │   │   │   │   ├── welcomejedgebot.webp
│   │   │   │   ├── landing-side.jpg
│   │   │   │   ├── logo.webp
│   │   │   │   ├── pricing.jpg
│   │   │   │   ├── raw
│   │   │   │   │   ├── DALL·E 2025-03-28 10.59.48 - A whimsical, wordless illustration representing forgetting a password, designed for a SaaS trading platform. The scene features a puzzled character se.webp
│   │   │   │   │   ├── DALL·E 2025-03-28 11.13.35 - A modern, wordless illustration representing resetting a password, designed for a SaaS trading platform. The scene features a relieved character succe.webp
│   │   │   │   │   ├── DALL·E 2025-03-28 12.34.54 - A sleek, wordless illustration representing a login page for a SaaS trading platform. The scene features a confident character entering a secure porta.webp
│   │   │   │   │   ├── DALL·E 2025-03-28 21.05.34 - A modern and minimalistic illustration representing the concept of registration. The image features a clipboard with a checklist being filled out, a d.webp
│   │   │   │   │   ├── leftlogin.jpg
│   │   │   │   │   ├── pexels-alesiakozik-6771426.jpg
│   │   │   │   │   ├── pexels-fauxels-3184416.jpg
│   │   │   │   │   ├── pexels-ibertola-2681319.jpg
│   │   │   │   │   ├── pexels-karolina-grabowska-4386433.jpg
│   │   │   │   │   ├── pexels-rdne-7648057.jpg
│   │   │   │   │   ├── pexels-snapwire-618613.jpg
│   │   │   │   │   ├── welcomejedgebot.webp
│   │   │   │   ├── registration.jpg
│   │   │   │   ├── registrationleft.jpg
│   │   │   │   ├── registrationleft.webp
│   │   │   ├── main.jsx
│   │   │   ├── pages
│   │   │   │   ├── TestCentering.jsx
│   │   │   ├── routes
│   │   │   │   ├── AppRoutes.jsx
│   │   │   │   ├── PrivateRoute.jsx
│   │   │   │   ├── routes.js
│   │   │   ├── styles
│   │   │   │   ├── Landing.css
│   │   │   │   ├── Sidebar.css
│   │   │   │   ├── global.css
│   │   │   ├── test-utils
│   │   │   │   ├── renderWithProviders.jsx
│   │   │   │   ├── setup.js
│   │   │   ├── utils
│   │   │   │   ├── __tests__
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
│   │   ├── Landing-Waitlist-Roadmap.md
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
│   │   ├── add-or-correct-path-comments.js
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
│   │   ├── convert-public-image-refs.js
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
│   ├── zscript.sh
```
