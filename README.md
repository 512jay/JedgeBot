# JedgeBot 🚀📈

JedgeBot is a professional-grade **algorithmic trading system** designed for **portfolio managers, traders, and fintech developers**. Built for **scalability, efficiency, and customization**, it provides tools for **real-time execution, backtesting, strategy optimization, and AI-driven insights**.

## 📌 **Key Features**
✅ **Real-Time Market Data Streaming** – Efficiently handles live price feeds & portfolio updates.
✅ **Automated Order Execution** – Supports **stocks, options, and multi-broker trading**.
✅ **Strategy Development Framework** – Implement, test, and optimize trading strategies.
✅ **Backtesting Engine** – Evaluate strategies using **historical market data**.
✅ **Advanced UI Dashboard** – Intuitive **React + FastAPI interface with TradingView charts**.
✅ **AI-Driven Trade Optimization** – Intelligent insights for smarter decision-making.
✅ **Cloud & Local Deployment** – Run JedgeBot on **personal machines or cloud servers**.
✅ **Security & Compliance** – Role-based access control, audit logs, tax reporting.

---

## 🏗 **Development Roadmap**
JedgeBot is structured into four progressive phases:

### **🔹 Phase 1: Core Trading System**
✅ **Live market data streaming & order execution**
✅ **Basic trading dashboard & logging system**

### **🔹 Phase 2: Strategy Development & UI**
✅ **First trading strategies (Wheel Strategy, Momentum Trading)**
✅ **Improved UI & real-time portfolio tracking**

### **🔹 Phase 3: Backtesting & Analytics**
✅ **Historical data integration & performance tracking**
✅ **Strategy optimization & simulation tools**

### **🔹 Phase 4: Scaling & Monetization**
✅ **AI-powered trade recommendations & cloud execution**
✅ **Enterprise-grade security, compliance, and reporting tools**
✅ **Subscription model & strategy marketplace**

🚀 **Full roadmap & details:** [JedgeBot Roadmap](https://github.com/512jay/JedgeBot/wiki/JedgeBot-Roadmap)

---

## 📌 **Installation & Setup**

### ✅ **1. Clone the Repository**
```sh
git clone https://github.com/512jay/JedgeBot.git
cd JedgeBot
```

### ✅ **2. Set Up Poetry Environment**
```sh
poetry install
poetry shell
```

### ✅ **3. Run the Project**
```sh
poetry run python jedgebot/main.py
```

For full setup details, check the **[Development Environment Guide](https://github.com/512jay/JedgeBot/wiki/Development-Environment-Setup)**.

---

## 🎯 **How to Contribute**
JedgeBot is an open-source project, and contributions are welcome!

### ✅ **1. Fork & Clone the Repository**
```sh
git clone https://github.com/512jay/JedgeBot.git
cd JedgeBot
git checkout -b feature/new-feature
```

### ✅ **2. Follow Coding Standards**
JedgeBot follows **PEP 8** and enforces clean, readable code:
```sh
black .
flake8
isort .
```

### ✅ **3. Submit a Pull Request**
- Link relevant issues.
- Ensure tests pass (`pytest tests/`).
- Follow commit message guidelines.

📌 **Full Contribution Guide:** [JedgeBot Contributor's Guide](https://github.com/512jay/JedgeBot/wiki/Contributors-Guide)

---

## 🌍 **Join the Community**
🔹 **GitHub Discussions** – Ask questions & suggest new features.
🔹 **Follow our Progress** – [JedgeBot Project Board](https://github.com/512jay/JedgeBot/projects)
🔹 **Stay Updated** – Join **Discord/Slack (Coming Soon!)**

We’re excited to have you contribute to JedgeBot! 🚀


# Manual preflight
poetry run pre-commit run --all-files

# Only backend check
poetry run python scripts/preflight.py

# Frontend vite production build
cd frontend && npm run check
