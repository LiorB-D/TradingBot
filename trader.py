import alpaca_trade_api as tradeapi
import numpy as np
import time


'''
    This is a trading script that you can run in the cloud and customize with your own trading algorithms

    The example uses the Alpaca Trading API, which is a free algorithmic trading platform that allows for paper trading
    You can setup a free account on Alpaca here: https://alpaca.markets/

    Alternatively, edit the getMarketData, Buy, and Sell functions to connect your own APIS
'''


SEC_KEY = ''
PUB_KEY = ''
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key_id= PUB_KEY, secret_key=SEC_KEY, base_url=BASE_URL)


def get_data():
    # Returns a an numpy array of the closing prices of the past 5 minutes
    market_data = api.get_barset(symb, 'minute', limit=5)
    
    close_list = []
    for bar in market_data[symb]:
        close_list.append(bar.c)
    
    close_list = np.array(close_list, dtype=np.float64)

    return close_list

def buy(q, s): # Returns nothing, makes call to buy stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
def sell(q, s): # Returns nothing, makes call to sell stock
    api.submit_order(
        symbol=s,
        qty=q,
        side='sell',
        type='market',
        time_in_force='gtc'
    )

symb = "SPY" # Ticker of stock you want to trade
pos_held = False

while True:
    print("")
    print("Checking Price")
    
    close_list = get_data()

    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    # Make buy/sell decision
    # This algorithm buys or sells when the moving average crosses the most recent closing price 

    if ma + 0.1 < last_price and not pos_held: # Buy when moving average is ten cents below the last price
        print("Buy")
        buy(1, symb)
        pos_held = True
    
    elif ma - 0.1 > last_price and pos_held: # Sell when moving average is ten cents above the last price
        print("Sell")
        sell(1, symb)
        pos_held = False
    
    time.sleep(60)

