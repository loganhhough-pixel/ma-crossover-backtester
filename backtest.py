import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

portfolio = pd.Series(account_worth, index=data.index)
daily_returns = portfolio.pct_change()

mean = daily_returns.mean()
std = daily_returns.std()

sharpe = (mean/std) * np.sqrt(252)

first_price = data["Close"].iloc[0]
last_price = data["Close"].iloc[-1]
hold_shares = 10000/first_price
hold_value = hold_shares * last_price
hold_worth = hold_shares * data["Close"]

hold_returns = hold_worth.pct_change()
hold_mean = hold_returns.mean()
hold_std = hold_returns.std()
hold_sharpe = (hold_mean/hold_std) * np.sqrt(252)

running_max = portfolio.cummax()
drawdown = (portfolio - running_max) / running_max
max_drawdown = drawdown.min()

hold_running_max = hold_worth.cummax()
hold_drawdown = (hold_worth - hold_running_max) / hold_running_max
hold_max_drawdown = hold_drawdown.min()

print(f"Strategy:    ${account_worth[-1]:,.2f}")
print(f"Buy & hold:  ${hold_value:,.2f}")
print(f"Trades:      {trade_counter}")
print(f"Total fees:  ${total_fees:,.2f}")
print(f"Sharpe:      {sharpe:.2f}")
print(f"Hold Sharpe:    {hold_sharpe:.2f}")
print(f"Max DD:      {max_drawdown:.1%}")
print(f"Hold Max DD: {hold_max_drawdown:.1%}")

plt.plot(portfolio, label="Strategy")
plt.plot(hold_worth, label="Buy & Hold")
plt.title("MA Crossover vs Buy & Hold — SPY 2015-2024")
plt.xlabel("Time")
plt.ylabel("Account Value ($)")
plt.legend()
plt.savefig("equity_curve.png", dpi=150, bbox_inches="tight")
plt.show()