# **JedgeBot**

## **Overview**
JedgeBot is an automated trading bot designed to execute multiple trading strategies across different brokers and asset classes, starting with the **Wheel Strategy** on the **S&P 500**. The bot is built using **Python** and integrates with multiple brokers, including:

- **TastyTrade** (Options trading)
- **Interactive Brokers (IBKR)** (Stocks, Options, Futures)
- **Kraken** (Cryptocurrency trading)
- **Robinhood** (Crypto trading API only)
- **MetaTrader 5 (MT5)** (Forex & CFD trading)

Future strategies will expand beyond the Wheel Strategy to include additional **options, stock, and crypto trading approaches**.

---

## **Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/512jay/JedgeBot.git
cd JedgeBot
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Set Up API Keys**
Create a `.env` file and add your broker credentials:
```plaintext
TASTYTRADE_API_KEY=your_api_key
IBKR_API_KEY=your_api_key
KRAKEN_API_KEY=your_api_key
MT5_SERVER=your_mt5_server
MT5_LOGIN=your_mt5_login
MT5_PASSWORD=your_mt5_password
```

### **4️⃣ Run the Bot (Local Mode)**
```bash
python main.py
```

---

## **Supported Trading Strategies**
1. **Wheel Strategy** (SPY options)
2. **Covered Calls & Cash-Secured Puts**
3. **Trend-Following Crypto Trading**
4. **Mean Reversion Strategy**
5. **Arbitrage Trading (Crypto & Stocks)**
6. **Forex Trading via MT5**

More strategies will be added as the project evolves.

---

## **Contributing**
If you're interested in contributing, feel free to submit a **pull request** or suggest new features in the **Issues section**.

---

## **License**
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## **Future Plans**
- **Add AI/ML-based trade predictions**.
- **Mobile app integration**.
- **Auto-trading across multiple brokers simultaneously**.
- **Cloud-based execution for 24/7 automation**.

For a detailed roadmap and milestones, visit the **Milestones section** of the repository.

