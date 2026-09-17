import yfinance as yf
import pandas as pd

data = yf.download("SPY", start="2015-01-01", end="2024-01-01", auto_adjust=True)
data.columns = data.columns.droplevel(1)

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()

cash = 10000
shares = 0

transaction_cost_rate = 0.001
trade_counter = 0
total_fees = 0

account_worth = []

for i in range(len(data)):
    price_today = data["Close"].iloc[i]
    short_ma = data["MA20"].iloc[i]
    long_ma = data["MA50"].iloc[i]

    if short_ma > long_ma and shares == 0:
        shares = cash/(price_today * (1 + transaction_cost_rate))
        cost = price_today * shares
        fee = cost * transaction_cost_rate
        total_fees += fee
        cash -= (cost + fee)
        trade_counter += 1

    elif long_ma > short_ma and shares !=0:
        gross = price_today * shares
        fee = gross * transaction_cost_rate
        total_fees += fee
        cash = gross - fee
        shares = 0
        trade_counter += 1

    account_worth.append(cash+shares*price_today)

first_price = data["Close"].iloc[0]
last_price = data["Close"].iloc[-1]
hold_shares = 10000/first_price
hold_value = hold_shares * last_price

print(f"Strategy:    ${account_worth[-1]:,.2f}")
print(f"Buy & hold:  ${hold_value:,.2f}")
print(f"Trades:      {trade_counter}")
print(f"Total fees:  ${total_fees:,.2f}")