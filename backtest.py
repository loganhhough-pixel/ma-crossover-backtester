import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = yf.download("SPY", start="2015-01-01", end="2024-01-01", auto_adjust=True)
data.columns = data.columns.droplevel(1)

train = yf.download("SPY", start="2015-01-01", end="2021-01-01", auto_adjust=True)
train.columns = train.columns.droplevel(1)

test = yf.download("SPY", start="2021-01-01", end="2024-01-01", auto_adjust=True)
test.columns = test.columns.droplevel(1)

def run_backtest(data, short_window, long_window, position_size=1.0):
    data["MA_short"] = data["Close"].rolling(short_window).mean()
    data["MA_long"] = data["Close"].rolling(long_window).mean()

    cash = 10000
    shares = 0

    transaction_cost_rate = 0.001
    trade_counter = 0
    total_fees = 0

    account_worth = []

    for i in range(len(data)):
        price_today = data["Close"].iloc[i]
        short_ma = data["MA_short"].iloc[i]
        long_ma = data["MA_long"].iloc[i]

        if short_ma > long_ma and shares == 0:
            shares = (cash * position_size)/(price_today * (1 + transaction_cost_rate))
            cost = price_today * shares
            fee = cost * transaction_cost_rate
            total_fees += fee
            cash -= (cost + fee)
            trade_counter += 1

        elif long_ma > short_ma and shares !=0:
            gross = price_today * shares
            fee = gross * transaction_cost_rate
            total_fees += fee
            cash += gross - fee
            shares = 0
            trade_counter += 1

        account_worth.append(cash+shares*price_today)

    portfolio = pd.Series(account_worth, index=data.index)
    daily_returns = portfolio.pct_change()
    mean = daily_returns.mean()
    std = daily_returns.std()
    sharpe = (mean/std) * np.sqrt(252)

    running_max = portfolio.cummax()
    drawdown = (portfolio - running_max) / running_max
    max_drawdown = drawdown.min()

    return account_worth[-1], sharpe, max_drawdown, trade_counter, total_fees, portfolio

tickers = ["SPY", "QQQ", "AAPL", "MSFT", "GLD"]

for ticker in tickers:
    prices = yf.download(ticker, start="2015-01-01", end="2024-01-01", auto_adjust=True)
    prices.columns = prices.columns.droplevel(1)
    
    value, sharpe, dd, trades, fees, portfolio = run_backtest(prices, 20, 50)
    
    hold = (10000 / prices["Close"].iloc[0]) * prices["Close"].iloc[-1]
    
    print(f"{ticker}:  strategy ${value:,.0f}  hold ${hold:,.0f}  Sharpe {sharpe:.2f}  DD {dd:.1%}  {trades} trades")

for size in [1.0, 0.75, 0.5, 0.25]:
    value, sharpe, dd, trades, fees, portfolio = run_backtest(data, 20, 50, size)
    print(f"Size {size}:  ${value:,.0f}  Sharpe {sharpe:.2f}  DD {dd:.1%}")

value, sharpe, dd, trades, fees, portfolio = run_backtest(data, 20, 50)
hold_worth = (10000 / data["Close"].iloc[0]) * data["Close"]

plt.figure(figsize=(12, 6))
plt.plot(portfolio, label="MA Crossover (20/50)")
plt.plot(hold_worth, label="Buy & Hold")
plt.title("MA Crossover vs Buy & Hold — SPY 2015-2024")
plt.xlabel("Date")
plt.ylabel("Account Value ($)")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("equity_curve.png", dpi=150, bbox_inches="tight")
plt.show()