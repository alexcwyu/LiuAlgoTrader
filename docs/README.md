# LiuAlgoTrader

**Algorithmic day-trading framework with producer-consumer architecture, scanners, and database-backed analytics.**

| Field | Details |
|-------|---------|
| Language | Python (asyncio) |
| License | MIT |
| Author | amor71 |
| GitHub | [amor71/LiuAlgoTrader](https://github.com/amor71/LiuAlgoTrader) |
| Docs | [liualgotrader.readthedocs.io](https://liualgotrader.readthedocs.io/) |

## Overview

LiuAlgoTrader is a scalable algorithmic day-trading framework built around a producer-consumer architecture with multiprocessing. It features real-time market scanners, pluggable trading strategies, database-backed trade persistence via PostgreSQL, and comprehensive backtesting and optimization capabilities. The framework supports Alpaca, Tradier, and Gemini brokers.

## Key Features

### Trading Capabilities
- Producer-consumer architecture with multiprocessing for scalability
- Real-time market scanning with pluggable scanner classes
- Day-trade and swing strategy types
- Portfolio management with external account support
- Fractional share trading support
- Hyperparameter optimization for strategy tuning

### Architecture
- Producer pumps market data to consumer processes via multiprocessing queues
- Consumers execute strategies on streaming data independently
- Scanner processes discover new trading opportunities on recurring schedules
- Database-backed trade persistence (PostgreSQL with asyncpg)
- TOML-based trade plan configuration

### Supported Venues
- **Alpaca**: Stocks (primary broker)
- **Tradier**: Stocks
- **Gemini**: Crypto

### Data Management
- Real-time streaming data via WebSocket (second aggregates, minute aggregates, trades)
- Historical data loading through DataLoader abstraction
- Data providers: Alpaca, Polygon, Finnhub, Tradier, Gemini
- Portfolio analytics and trade reprocessing

### Risk Management
- Strategy-level schedule enforcement (trading windows)
- Position tracking per symbol
- Trade logging with git commit association
- Gain/loss tracking and analytics

## Architecture Summary

```
Scanners (discover symbols)
    |
    v
Producer (subscribe to market data, pump to consumers)
    |
    v (multiprocessing queues)
Consumers (execute strategies on streaming data)
    |
    v
Database (PostgreSQL - trades, analytics, portfolio)
```

## Component Table

| Component | Location | Purpose |
|-----------|----------|---------|
| Producer | `src/liualgotrader/producer.py` | Market data pump to consumer processes |
| Consumer | `src/liualgotrader/consumer.py` | Strategy execution on streaming data |
| Strategy (base) | `src/liualgotrader/strategies/base.py` | Abstract strategy class (day-trade/swing) |
| Scanner (base) | `src/liualgotrader/scanners/base.py` | Abstract market scanner class |
| MomentumScanner | `src/liualgotrader/scanners/momentum.py` | Built-in momentum scanner |
| DataAPI (base) | `src/liualgotrader/data/data_base.py` | Abstract data provider interface |
| Trader (base) | `src/liualgotrader/trading/base.py` | Abstract broker interface |
| DataLoader | `src/liualgotrader/common/data_loader.py` | DataFrame-like data access |
| AlgoRun | `src/liualgotrader/models/algo_run.py` | Algorithm run tracking |
| Portfolio | `src/liualgotrader/models/portfolio.py` | Portfolio management |
| TradePlan | `src/liualgotrader/models/tradeplan.py` | TOML trade plan loading |
| Optimizer | `src/liualgotrader/backtesting/optimizer.py` | Hyperparameter optimization |
| EnhancedBacktest | `src/liualgotrader/enhanced_backtest.py` | Enhanced backtesting engine |
| FinCalcs | `src/liualgotrader/fincalcs/` | Financial calculations (VWAP, trends, patterns) |

## Quick Start

LiuAlgoTrader requires PostgreSQL and broker API keys for live trading. Below is a strategy definition and minimal `tradeplan.toml` to illustrate the framework's structure.

### 1. Strategy Definition (`my_strategy.py`)

```python
from liualgotrader.strategies.base import Strategy, StrategyType
from liualgotrader.common.data_loader import DataLoader
from datetime import datetime
from typing import Dict, Tuple

class MyStrategy(Strategy):
    """Simple momentum strategy: buy on 2% price increase."""

    def __init__(self, batch_id: str, schedule: list,
                 data_loader: DataLoader, **kwargs):
        super().__init__(
            name="MyStrategy",
            type=StrategyType.DAY_TRADE,
            batch_id=batch_id,
            schedule=schedule,
            data_loader=data_loader,
        )
        self.threshold = kwargs.get("threshold", 0.02)

    async def run(
        self, symbol: str, shortable: bool, position: float,
        now: datetime, minute_history: dict,
        portfolio_value: float = None, debug: bool = False,
        backtesting: bool = False,
    ) -> Tuple[bool, Dict]:
        close = minute_history["close"]
        if len(close) < 2:
            return False, {}
        change = (close[-1] - close[-2]) / close[-2]
        if change > self.threshold and position == 0:
            return True, {
                "side": "buy", "qty": 100,
                "type": "limit", "limit_price": close[-1],
            }
        return False, {}
```

### 2. Trade Plan (`tradeplan.toml`)

```toml
# Scanners discover symbols to trade
[scanners]
[scanners.momentum]
provider = "polygon"
min_volume = 500000
min_gap = 3.5
recurrence = 5  # re-scan every 5 minutes

# Strategies execute trades on discovered symbols
[strategies]
[strategies.MyStrategy]
filename = "./my_strategy.py"
threshold = 0.02
schedule = [
    {start = "09:30", duration = 360}
]
```

### 3. Required Environment Variables

```bash
# PostgreSQL connection (required)
export DSN="postgresql://user:password@localhost:5432/liualgotrader"

# Broker selection (required)
export LIU_BROKER="alpaca"           # Options: alpaca, tradier, gemini

# Alpaca credentials (when LIU_BROKER=alpaca)
export APCA_API_BASE_URL="https://paper-api.alpaca.markets"
export APCA_API_KEY_ID="your-key"
export APCA_API_SECRET_KEY="your-secret"

# Data provider (optional, defaults to alpaca)
export DATA_CONNECTOR="alpaca"       # Options: alpaca, polygon, finnhub, tradier, gemini

# Start the trader
liu trader
```

### All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DSN` | Yes | `""` | PostgreSQL connection string |
| `LIU_BROKER` | No | `"alpaca"` | Broker: `alpaca`, `tradier`, `gemini` |
| `DATA_CONNECTOR` | No | `"alpaca"` | Data provider: `alpaca`, `polygon`, `finnhub`, `tradier`, `gemini` |
| `APCA_API_BASE_URL` | When Alpaca | -- | Alpaca API base URL (paper or live) |
| `APCA_API_KEY_ID` | When Alpaca | `""` | Alpaca API key ID |
| `APCA_API_SECRET_KEY` | When Alpaca | `""` | Alpaca API secret key |
| `ALPACA_DATA_FEED` | No | `"sip"` | Alpaca data feed (`sip` or `iex`) |
| `ALPACA_STREAM_URL` | No | None | Custom Alpaca stream URL |
| `TRADIER_BASE_URL` | When Tradier | `"https://sandbox.tradier.com/v1/"` | Tradier API base URL |
| `TRADIER_WS_URL` | When Tradier | `"wss://ws.tradier.com/v1/"` | Tradier WebSocket URL |
| `TRADIER_ACCOUNT_NUMBER` | When Tradier | None | Tradier account number |
| `TRADIER_ACCESS_TOKEN` | When Tradier | None | Tradier access token |
| `POLYGON_API_KEY` | When Polygon | None | Polygon.io API key |
| `FINNHUB_API_KEY` | When Finnhub | None | Finnhub API key |
| `FINNHUB_BASE_URL` | When Finnhub | None | Finnhub API base URL |
| `TRADEPLAN_DIR` | No | `"."` | Directory containing `tradeplan.toml` |
| `LIU_TRACE_ENABLED` | No | `0` | Enable trace logging (`1` to enable) |
| `LIU_DEBUG_ENABLED` | No | `0` | Enable debug logging (`1` to enable) |
| `GCP_STACKDRIVER` | No | `0` | Enable GCP Stackdriver logging (`1` to enable) |
| `CPU_FACTOR` | No | `2.0` | CPU multiplier for consumer process count |
| `NUM_CONSUMERS` | No | `0` | Override consumer process count (0 = auto) |

## Links

- [Architecture](architecture.md) -- System design and component diagrams
- [Workflow](workflow.md) -- Event flows and key workflows
- [State Management](state-management.md) -- State machines and lifecycle
- [Development](development.md) -- Setup, standards, and strategy development
