import json
from backend.broker.tastytrade.tastytrade import TastyTradeClient

tasty = TastyTradeClient()
accounts = tasty.get_accounts()
print(json.dumps(accounts, indent=4))
