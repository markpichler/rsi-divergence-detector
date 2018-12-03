import json, requests

def price_history(interval, symbol):
   
    price_array = []
    payload = {"interval": interval, "symbol": symbol, "limit": 30}

    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)
 
    for c in json.loads(r.text):
        price_array.append(c[4])
    
    
    return price_array



def find_lows(data):
    lows = []
    for i in range(len(data)):
        # Assumes data array len is greater than 1
        if i == 0 and data[i] <= data[i + 1]:
            lows.append(data[i]) 
        elif i == len(data) - 1 and data[i] <= data[i - 1]:
            lows.append(data[i])
        elif data[i - 1] >= data[i] <= data[i + 1]:
            lows.append(data[i])
        else:
            lows.append(-1)

    return lows




"""def calculate_rsi(interval, period, symbol):
    init_avg_gain = 0
    init_avg_loss = 0
    payload = {"interval": interval, "symbol": symbol, "limit": period}
    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)
    candles = json.loads(r.text)

    for i in range(len(candles)):
        print("1")
"""
print(find_lows(price_history("15m", "BTCUSDT")))