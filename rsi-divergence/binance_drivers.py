import json, math, requests

class Asset:
    """Gathers/manages data to detect RSI divergence for unique trading pairs.

    Attributes:
        interval: Desired time frame (string).
        symbol: Desired trading pair (string).
    """
    
    a = 1 / 14

    def __init__(self, interval, symbol):
        """Collect initial short term price and RSI history."""

        self.rsi = []
        self.prices = []
        self.prev_gain_ema = 0
        self.prev_loss_ema = 0

        r = requests.get("https://api.binance.com/api/v1/klines", 
                         params={
                             "interval": interval, 
                             "symbol": symbol, 
                             "limit": 165
                         })
        for candle in json.loads(r.text):
            self.prices.append(float(candle[4]))

        # Initial EMA (SMA)
        for i in range(1, 15):
            change = self.prices[i] - self.prices[i - 1]
            if change > 0:
                self.prev_gain_ema += change
            else:
                self.prev_loss_ema += -change
        
        self.rsi.append(
            100 - (100 / (1 + self.prev_gain_ema / self.prev_loss_ema))
        )
        
        for i in range(15, len(self.prices)):
            change = self.prices[i] - self.prices[i - 1]

            if change > 0:
                u = change
                d = 0
            else:
                u = 0
                d = -change

            cur_gain_ema = a * u + (1 - a) * self.prev_gain_ema
            cur_loss_ema = a * d + (1 - a) * self.prev_loss_ema

            self.prev_gain_ema = cur_gain_ema 
            self.prev_loss_ema = cur_loss_ema

            self.rsi.append(100 - (100 / (1 + cur_gain_ema / cur_loss_ema)))
    
    def calculate_rsi(self):
        """Calculate and append current RSI.
        
        This method should be called once at the start of every new time 
        interval. 
        """

        change = self.prices[-1] - self.prices[-2]

        if change > 0:
            u = change
            d = 0
        else:
            u = 0
            d = -change

        cur_gain_ema = a * u + (1 - a) * self.prev_gain_ema
        cur_loss_ema = a * d + (1 - a) * self.prev_loss_ema

        self.prev_gain_ema = cur_gain_ema 
        self.prev_loss_ema = cur_loss_ema
        
        self.rsi.append(100 - (100 / (1 + cur_gain_ema / cur_loss_ema)))
       
      
def find_lows(prices, rsi_array):
    price_lows = []
    rsi_lows = []
    # Price lows
    for i in range(14, len(self.prices)):
        
        if i == 0 and self.prices[i] <= self.prices[i + 1]:
            price_lows.append(self.prices[i]) 
        elif i == len(self.prices) - 1 and self.prices[i] <= self.prices[i - 1]:
            price_lows.append(self.prices[i])
        elif self.prices[i - 1] >= self.prices[i] <= self.prices[i + 1]:
            price_lows.append(self.prices[i])
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


def find_divergence(price_lows, rsi_lows):
    min_price = math.inf
    min_rsi = 0

    for i in range(len(price_lows)):

        if -1 < price_lows[i] < min_price and -1 < rsi_lows[i] < 30:
            min_price = price_lows[i]
            min_rsi = rsi_lows[i]

    return (min_price, min_rsi) 




bitcoin_usdt = Asset("15m", "BTCUSDT")

print(bitcoin_usdt.closing_prices)
print(bitcoin_usdt.rsi)

"""
lows = find_lows(closing_prices, calculate_rsi(closing_prices))
print(find_divergence(lows[0], lows[1]))
"""