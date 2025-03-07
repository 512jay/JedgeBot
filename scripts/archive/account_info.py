import json
from jedgebot.broker.tastytrade.tastytrade import TastyTradeClient

tasty = TastyTradeClient()
accounts = tasty.get_accounts()
print(json.dumps(accounts, indent=4))
