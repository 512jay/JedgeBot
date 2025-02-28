from jedgebot.brokers.tastytrade_api import TastyTradeAPI


def main():
    tasty = TastyTradeAPI()
    balance = tasty.get_balance()
    print("Account Balance:", balance)

    # Example order: Buy 1 SPY Call Option at $1.50
    order_response = tasty.place_order("SPY 20240228 500 C", 1, "BUY", "LIMIT", 1.50)
    print("Order Response:", order_response)

if __name__ == "__main__":
    main()
