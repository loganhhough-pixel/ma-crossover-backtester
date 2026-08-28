import yfinance as yf
import pandas as pd

data = yf.download("SPY", start="2015-01-01", end="2024-01-01", auto_adjust=True)
data.columns = data.columns.droplevel(1)

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()

cash = 10000
shares = 0

account_worth = []
for i in range(len(data)):
    price_today = data["Close"].iloc[i]
    short_ma = data["MA20"].iloc[i]
    long_ma = data["MA50"].iloc[i]

    if short_ma > long_ma and shares == 0:
        shares = cash/price_today
        cash = cash - shares*price_today

    elif long_ma > short_ma and shares != 0:
        cash = cash + shares*price_today
        shares = 0

    account_worth.append(cash + shares * price_today)

print(account_worth[-1])

first_price = data["Close"].iloc[0]
last_price = data["Close"].iloc[-1]
hold_shares = 10000/first_price
hold_value = hold_shares * last_price
print(hold_value)