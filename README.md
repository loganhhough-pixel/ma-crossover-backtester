# Moving Average Crossover Backtester
A Python backtester that simulates a 20/50-day moving average crossover strategy on SPY and benchmarks it against buy-and-hold.

## What it does
Downloads SPY data to compute the 20 and 50 day moving averages, simulates buying when the short MA crosses above the long MA and selling when it crosses below. Tracks the account's value daily and compares it to buy-and-hold. Starting with $10,000 and 0 shares. As of V2, every trade is charged a transaction fee.

## Results

**V2 (with 0.1% transaction costs)**

| | Value | Return |
|---|---|---|
| Strategy | $17,752.31 | +77.5% |
| Buy-and-hold | $27,190.60 | +172% |

Trades executed: 43  
Total fees paid: $599.45

**V1 (no transaction costs)** returned $18,532 (+85%) over the same period, 2015-2024.

## What transaction costs actually cost
Adding a 0.1% fee per trade dropped the final value by $780, but only $599 of that was fees. The remaining $181 is compounding - money spent on fees early in the run wasn't invested for the years that followed. Small drags grow.

The more interesting number is the trade count. 43 trades across nine years is about 4.8 round trips per year, which is far more churn than I expected from a 20/50 crossover. Every one of those is a sell-into-weakness followed by a buy-back-higher.

That reframes the underperformance. The strategy trails buy-and-hold by $9,438, and only $780 of that gap is trading costs. The whipsaw itself is roughly twelve times more expensive than the fees are. For a low-frequency strategy like this one, transaction costs are a real but secondary drag - the timing is what kills it.

## Underperformance
The strategy underperformed because of whipsaw, selling on dips and rebuying higher. Time out of market during recoveries. A strong bull market punishes any strategy that sits in cash.

## A bug I found
In the sell branch, I originally planned to have a new variable called old_cash and to find our new shares by doing shares - (cash - old_cash)/price instead of setting shares to 0. Due to floating point rounding left ~1e-15 instead of exact 0, which broke the shares == 0 check in the buy condition, so after the first sell, the strategy could never buy again. Which understated the strategy's final value by about $8,400. Fixed by assigning to zero directly.

## Limitations
A single ticker. Trades at close using signals computed from the same close (assumes instant execution). All-in/all-out, no position sizing. Transaction costs are modeled as a flat percentage, which ignores bid-ask spread and slippage.

## Next Steps
V3 will add Sharpe ratio, max drawdown, and plots. V4 will add out-of-sample testing. V5 will extend to multiple assets with configurable position sizing and parameter sweeps.

## Requirements
Python 3, yfinance, pandas

## How to run
```
pip install yfinance pandas
python backtest.py
```