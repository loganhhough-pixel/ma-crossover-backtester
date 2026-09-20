# Moving Average Crossover Backtester
A Python backtester that simulates moving average crossover strategies on SPY, benchmarks them against buy-and-hold, and tests whether optimized parameters survive out-of-sample.

## What it does
Downloads SPY price data, computes two moving averages, and simulates buying when the short MA crosses above the long MA and selling when it crosses below. Tracks account value daily, charges a transaction fee on every trade, and reports risk-adjusted metrics alongside raw returns. The backtest is wrapped in a function that takes the MA windows as parameters, which makes it possible to sweep hundreds of combinations and test them on held-out data.

## Out-of-sample test

This is the main result.

I split the data into a training period (2015-2020) and a test period (2021-2024) that the parameter search never saw. On the training period I swept 144 combinations — short windows from 10 to 50, long windows from 50 to 200 — and picked the best performer. That was 15/70, which turned $10,000 into $18,507 on training data.

Then I ran 15/70 on the test period.

| Strategy | Test period result | Return |
|---|---|---|
| 15/70 (search winner) | $9,438 | -5.6% |
| 20/50 (convention) | $9,370 | -6.3% |
| Buy & hold | $13,474 | +34.7% |

The optimized parameters lost money on data they hadn't seen, while simply holding SPY returned 34.7%.

Two separate failures are worth keeping distinct:

**The optimization was worthless.** On training data, 15/70 beat 20/50 by $1,424. On test data, by $68 — indistinguishable from zero. Whatever advantage the search found did not exist outside the period it searched.

**The strategy itself doesn't work.** Both parameter sets lost money while the market gained a third. This isn't only a tuning problem.

## Why the search found noise

The parameter surface is not smooth. Holding the short window at 15 and varying the long window:

| Long window | Training result |
|---|---|
| 50 | $17,084 |
| 60 | $18,450 |
| 70 | $18,507 |
| 80 | $15,379 |
| 90 | $15,456 |
| 100 | $13,261 |

A ten-day change drops performance by $3,100. If these parameters captured something real about how markets behave, neighboring values would perform similarly. They don't. The peaks are artifacts of which specific price movements happened to fall on which side of a crossover during that window.

Two other patterns from the sweep: long windows are systematically worse across the board, since slower signals mean more time sitting in cash. And 50/50 returns exactly $10,000 — identical windows mean the MAs are always equal, neither condition fires, and no trades happen. A useful sanity check that the logic behaves.

One more thing about the test period. 2021-2024 contains the 2022 bear market, which is exactly the regime a trend-following strategy is supposed to handle — get out before the worst of it. It didn't. It whipsawed through the chop and then missed the 2023 recovery.

## Full period results

Running 20/50 across the entire 2015-2024 range with 0.1% transaction costs:

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
The raw return gap makes the strategy look worse than the risk-adjusted numbers do. Buy-and-hold more than doubles the strategy's return, but its Sharpe ratio is only about 13% higher. The strategy sits in cash for long stretches, and cash has no volatility, so both the numerator and denominator shrink together.

The drawdown tells the other half. The strategy's worst peak-to-trough loss was -29.6% against buy-and-hold's -33.7%, so it did provide some downside protection. But four percentage points of protection cost ninety-five percentage points of return.

The -29.6% figure also shows the limits of a 50-day signal. The strategy was still in the market for most of the COVID crash — by the time the long MA crossed down, the damage was mostly done. The protection it offers is bounded by its own lag.

## What transaction costs actually cost
Adding a 0.1% fee per trade dropped the final value by $780, but only $599 of that was fees. The remaining $181 is compounding — money spent on fees early wasn't invested for the years that followed.

The more interesting number is the trade count. 43 trades across nine years is about 4.8 round trips per year, far more churn than I expected from a 20/50 crossover. The strategy trails buy-and-hold by $9,438, and only $780 of that gap is trading costs. The whipsaw itself is roughly twelve times more expensive than the fees are.

## A bug I found
In the sell branch, I originally planned to have a new variable called old_cash and to find our new shares by doing shares - (cash - old_cash)/price instead of setting shares to 0. Due to floating point rounding left ~1e-15 instead of exact 0, which broke the shares == 0 check in the buy condition, so after the first sell, the strategy could never buy again. Which understated the strategy's final value by about $8,400. Fixed by assigning to zero directly.

## Limitations
A single ticker. Trades at close using signals computed from the same close, which assumes instant execution. All-in/all-out, no position sizing. Transaction costs are a flat percentage, ignoring bid-ask spread and slippage. Sharpe is computed against a zero risk-free rate.

The train/test split is a single split at one date. A more rigorous approach would use walk-forward validation across multiple windows, since one holdout period could itself be unrepresentative.

## Next Steps
V5 will extend the engine to multiple assets with configurable position sizing.

## Requirements
Python 3, yfinance, pandas, numpy, matplotlib

## How to run
```
pip install yfinance pandas numpy matplotlib
python backtest.py
```