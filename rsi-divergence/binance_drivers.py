import json, requests

def price_history(interval, symbol):
    price_array = []
    payload = {"interval": interval, "symbol": symbol, "limit": 100}

    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)
 
    for c in json.loads(r.text):
        price_array.append(c[4])
       
    return price_array

"""def calculate_rsi(interval, period, symbol):
    init_avg_gain = 0
    init_avg_loss = 0
    payload = {"interval": interval, "symbol": symbol, "limit": period}
    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)
    candles = json.loads(r.text)

    for i in range(len(candles)):
        print("1")
"""
