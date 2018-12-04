import json, requests

def get_price_history(interval, symbol):
    closing_prices = []

    payload = {"interval": interval, "symbol": symbol, "limit": 115}

    r = requests.get("https://api.binance.com/api/v1/klines", params=payload)

    for candle in json.loads(r.text):
        # TODO: See if json.loads() can return numbers instead of strings
        closing_prices.append(candle[4])
    
    return closing_prices 


def find_lows(closing_prices):
    lows = []
    for i in range(len(closing_prices)):
        # Assumes closing_prices array len is greater than 1
        if i == 0 and closing_prices[i] <= closing_prices[i + 1]:
            lows.append(closing_prices[i]) 
        elif i == len(closing_prices) - 1 and closing_prices[i] <= closing_prices[i - 1]:
            lows.append(closing_prices[i])
        elif closing_prices[i - 1] >= closing_prices[i] <= closing_prices[i + 1]:
            lows.append(closing_prices[i])
        else:
            lows.append(-1)

    return lows

def calculate_rsi(closing_prices):
    # init_avg_gain = 0
    # init_avg_loss = 0
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


print(calculate_rsi(get_price_history("15m", "BTCUSDT")))