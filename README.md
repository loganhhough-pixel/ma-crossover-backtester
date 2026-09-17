# Moving Average Crossover Backtester
A Python backtester that simulates a 20/50-day moving average crossover strategy on SPY and benchmarks it against buy-and-hold.

## What it does
Downloads SPY data to compute the 20 and 50 day moving averages, simulates buying when the short MA crosses above the long MA and selling when it crosses below. Tracks the account's value daily and compares it to buy-and-hold. Starting with $10,000 and 0 shares. Every trade is charged a transaction fee, and the engine reports risk-adjusted performance alongside raw returns.

## Results

2015-2024, SPY, 0.1% transaction cost per trade.

| | Strategy | Buy & Hold |
|---|---|---|
| Final value | $17,752.30 | $27,190.59 |
| Return | +77.5% | +172% |
| Sharpe ratio | 0.62 | 0.71 |
| Max drawdown | -29.6% | -33.7% |

Trades executed: 43  
Total fees paid: $599.45

![Equity curve](equity_curve.png)

## What the metrics say
The raw return gap makes the strategy look far worse than the risk-adjusted numbers do. Buy-and-hold more than doubles the strategy's return, but its Sharpe ratio is only about 13% higher. The strategy sits in cash for long stretches, and cash has no volatility, so both the numerator and denominator of the Sharpe shrink together.

The drawdown tells the other half. The strategy's worst peak-to-trough loss was -29.6% against buy-and-hold's -33.7%, so it did provide some downside protection. But four percentage points of protection cost ninety-five percentage points of return. In a nine-year bull market that is a bad trade.

The -29.6% figure also shows the limits of a 50-day signal. The strategy was still in the market for most of the COVID crash — by the time the long MA crossed down, the damage was mostly done. The protection it offers is bounded by its own lag.

## What transaction costs actually cost
Adding a 0.1% fee per trade dropped the final value by $780, but only $599 of that was fees. The remaining $181 is compounding — money spent on fees early in the run wasn't invested for the years that followed.

The more interesting number is the trade count. 43 trades across nine years is about 4.8 round trips per year, far more churn than I expected from a 20/50 crossover. The strategy trails buy-and-hold by $9,438, and only $780 of that gap is trading costs. The whipsaw itself is roughly twelve times more expensive than the fees are.

## A bug I found
In the sell branch, I originally planned to have a new variable called old_cash and to find our new shares by doing shares - (cash - old_cash)/price instead of setting shares to 0. Due to floating point rounding left ~1e-15 instead of exact 0, which broke the shares == 0 check in the buy condition, so after the first sell, the strategy could never buy again. Which understated the strategy's final value by about $8,400. Fixed by assigning to zero directly.

## Limitations
A single ticker. Trades at close using signals computed from the same close (assumes instant execution). All-in/all-out, no position sizing. Transaction costs are modeled as a flat percentage, ignoring bid-ask spread and slippage. Sharpe is computed against a zero risk-free rate. Parameters (20/50) were chosen conventionally, not fitted, and have not been tested out-of-sample.

## Next Steps
V4 will add out-of-sample testing — fitting parameters on a training window and evaluating on held-out data. V5 will extend to multiple assets with configurable position sizing and parameter sweeps.

## Requirements
Python 3, yfinance, pandas, numpy, matplotlib

## How to run
```
pip install yfinance pandas numpy matplotlib
python backtest.py
```