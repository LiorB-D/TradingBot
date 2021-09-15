import alpaca_trade_api as tradeapi
import numpy as np
import time



SEC_KEY = 'bcO995J1nB2W7iWbzIkXv4foX0GKaQJAYT8pX1fN'
PUB_KEY = 'PKRQE96HW8BM6TO9V13V'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)

symb = "SPY"
pos_held = False
hours_to_test = 2
print("Checking Price")
market_data = api.get_barset(symb, 'minute', limit=(60 * hours_to_test))

close_list = []
for bar in market_data[symb]:
    close_list.append(bar.c)



print("Open: " + str(close_list[0]))
print("Close: " + str(close_list[60 * hours_to_test - 1]))


close_list = np.array(close_list, dtype=np.float64)
startBal = 2000
balance = startBal
buys = 0
sells = 0



for i in range(4, 60 * hours_to_test):
    ma = np.mean(close_list[i-4:i+1])
    last_price = close_list[i]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held:
        print("Buy")
        balance -= last_price
        pos_held = True
        buys += 1
    elif ma - 0.1 > last_price and pos_held:
        print("Sell")
        balance += last_price
        pos_held = False
        sells += 1
    print(balance)
    time.sleep(0.01)

print("")
print("Buys: " + str(buys))
print("Sells: " + str(sells))

if buys > sells:
    balance += close_list[60 * hours_to_test - 1]
    

print("Final Balance: " + str(balance))

print("Profit if held: " + str(close_list[60 * hours_to_test - 1] - close_list[0]))
print("Profit from algorithm: " + str(balance - startBal))


