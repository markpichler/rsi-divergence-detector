import json, math, requests

def get_price_history(interval, symbol):
    closing_prices = []

    payload = {"interval": interval, "symbol": symbol, "limit": 115}

    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)

    for candle in json.loads(r.text):
        # TODO: See if json.loads() can return numbers instead of strings
        closing_prices.append(float(candle[4]))
    
    return closing_prices 


def find_lows(closing_prices, rsi_array):
    price_lows = []
    rsi_lows = []
    # Price lows
    for i in range(14, len(closing_prices)):
        
        if i == 0 and closing_prices[i] <= closing_prices[i + 1]:
            price_lows.append(closing_prices[i]) 
        elif i == len(closing_prices) - 1 and closing_prices[i] <= closing_prices[i - 1]:
            price_lows.append(closing_prices[i])
        elif closing_prices[i - 1] >= closing_prices[i] <= closing_prices[i + 1]:
            price_lows.append(closing_prices[i])
        else:
            price_lows.append(-1)
    
    # RSI lows
    for i in range(len(rsi_array)):
        if i == 0 and rsi_array[i] <= rsi_array[i + 1]:
            rsi_lows.append(rsi_array[i]) 
        elif i == len(rsi_array) - 1 and rsi_array[i] <= rsi_array[i - 1]:
            rsi_lows.append(rsi_array[i])
        elif rsi_array[i - 1] >= rsi_array[i] <= rsi_array[i + 1]:
            rsi_lows.append(rsi_array[i])
        else:
            rsi_lows.append(-1)

    return (price_lows, rsi_lows)

def calculate_rsi(closing_prices):
    
    total_gains = 0
    total_losses = 0
    a = 1 / 14
    rsi = []

    # Initial EMA (SMA)
    for i in range(1, 15):

        change = float(closing_prices[i]) - float(closing_prices[i - 1])
        if change > 0:
            total_gains += change
        else:
            total_losses += -change
    
    prev_gain_ema = total_gains / 14
    prev_loss_ema = total_losses / 14
    rs = prev_gain_ema / prev_loss_ema
    rsi.append(100 - (100 / (1 + rs)))
    
    for i in range(15, len(closing_prices)):
        change = float(closing_prices[i]) - float(closing_prices[i - 1])

        if change > 0:
            u = change
            d = 0
        else:
            u = 0
            d = -change

        cur_gain_ema = a * u + (1 - a) * prev_gain_ema
        cur_loss_ema = a * d + (1 - a) * prev_loss_ema

        prev_gain_ema = cur_gain_ema 
        prev_loss_ema = cur_loss_ema

        rs = cur_gain_ema / cur_loss_ema
        rsi.append(100 - (100 / (1 + rs)))

    return rsi



def find_divergence(price_lows, rsi_lows):
    min_price = math.inf
    min_rsi = 0

    for i in range(len(price_lows)):
    
        if -1 < price_lows[i] < min_price and -1 < rsi_lows[i] < 30:
            min_price = price_lows[i]
            min_rsi = rsi_lows[i]

    return (min_price, min_rsi) 




closing_prices = get_price_history("15m", "BTCUSDT")

lows = find_lows(closing_prices, calculate_rsi(closing_prices))
print(find_divergence(lows[0], lows[1]))