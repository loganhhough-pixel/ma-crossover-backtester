# Moving Average Crossover Backtester
A Python backtester that simulates a 20/50-day moving average crossover strategy on SPY and benchmarks it against buy-and-hold.

## What it does
Downloads SPY data to compute the 20 and 50 day moving averages, simulates buying when the short MA crosses above the long MA and selling when it crosses below. Tracks the account's value daily and compares it to buy-and-hold. Starting with $10,000 and 0 shares.

## Results
The strategy resulted in $18,532 (+85%), buy-and-hold resulted in $27,190 (+172%) over a 9 year span of 2015-2024.

## Underperformance
The strategy underperformed because of whipsaw, selling on dips and rebuying higher. Time out of market during recoveries. A strong bull market punishes any strategy that sits in cash.

## A bug I found
In the sell branch, I originally planned to have a new variable called old_cash and to find our new shares by doing shares - (cash - old_cash)/price instead of setting shares to 0. Due to floating point rounding left ~1e-15 instead of exact 0, which broke the shares == 0 in the buy condition, so after the first sell, the strategy could never buy again. Which understated the strategy's final value by about $8,400. Fixed by assigning to zero directly.

## Limitations
No transaction costs. A single ticker. Trades at close using signals computed from the same close (assumes instant execution). All-in/all-out, no position sizing.

## Next Steps
My next version will include transaction costs. The one following that will include sharpe ratio, max drawdown, plots. The one following that will include out-of-sample testing.

## Requirements
Python 3, yfinance, pandas

## How to run
```
pip install yfinance pandas
python backtest.py
```