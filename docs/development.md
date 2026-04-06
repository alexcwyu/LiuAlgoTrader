# LiuAlgoTrader -- Development Guide

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Broker API keys (Alpaca, Tradier, or Gemini)

### Installation

```bash
pip install liualgotrader
```

### From Source

```bash
git clone https://github.com/amor71/LiuAlgoTrader.git
cd LiuAlgoTrader
pip install -e .
```

### Database Setup

Configure PostgreSQL connection via environment variables or configuration file. The framework manages schema creation automatically.

## Configuration

### tradeplan.toml

The trade plan defines scanners and strategies:

```toml
[scanners]
[scanners.momentum]
provider = "polygon"
min_volume = 500000
min_gap = 3.5
recurrence = 5  # minutes

[strategies]
[strategies.MyStrategy]
filename = "./my_strategy.py"
schedule = [
    {start = "09:30", duration = 360}  # 6 hours from market open
]
```

## Building a Strategy

### Minimal Strategy

```python
from liualgotrader.strategies.base import Strategy, StrategyType
from liualgotrader.common.data_loader import DataLoader
from datetime import datetime
from typing import Dict, Optional, Tuple

class MyStrategy(Strategy):
    def __init__(self, batch_id: str, schedule: list, data_loader: DataLoader, **kwargs):
        super().__init__(
            name="MyStrategy",
            type=StrategyType.DAY_TRADE,
            batch_id=batch_id,
            schedule=schedule,
            data_loader=data_loader,
        )

    async def run(
        self,
        symbol: str,
        shortable: bool,
        position: float,
        now: datetime,
        minute_history: dict,
        portfolio_value: float = None,
        debug: bool = False,
        backtesting: bool = False,
    ) -> Tuple[bool, Dict]:
        # Access historical data
        close = minute_history["close"]
        
        if close[-1] > close[-2] * 1.02:  # 2% price increase
            return True, {
                "side": "buy",
                "qty": 100,
                "type": "limit",
                "limit_price": close[-1],
            }
        
        return False, {}
```

### Portfolio-Wide Strategy (run_all)

```python
class PortfolioStrategy(Strategy):
    async def should_run_all(self):
        return True

    async def run_all(
        self,
        symbols_position: Dict[str, float],
        data_loader: DataLoader,
        now: datetime,
        portfolio_value: float = None,
        trader = None,
        debug: bool = False,
        backtesting: bool = False,
        **kwargs,
    ) -> Dict[str, Dict]:
        results = {}
        for symbol, position in symbols_position.items():
            # Cross-symbol analysis logic
            results[symbol] = {"side": "buy", "qty": 10}
        return results
```

## Building a Scanner

```python
from liualgotrader.scanners.base import Scanner
from liualgotrader.common.data_loader import DataLoader
from datetime import datetime, timedelta
from typing import List, Optional

class MyScanner(Scanner):
    def __init__(
        self,
        data_loader: DataLoader,
        recurrence: Optional[timedelta] = None,
        target_strategy_name: Optional[str] = None,
        min_volume: int = 100000,
        **kwargs,
    ):
        super().__init__(
            name="MyScanner",
            data_loader=data_loader,
            recurrence=recurrence,
            target_strategy_name=target_strategy_name,
        )
        self.min_volume = min_volume

    async def run(self, back_time: datetime = None) -> List[str]:
        # Discover symbols meeting criteria
        snapshot = await self.data_loader.data_api.get_market_snapshot(
            lambda x: x.get("volume", 0) > self.min_volume
        )
        return [s["symbol"] for s in snapshot]
```

## Running the System

### Live Trading

```bash
# Start the trader (producer + consumers)
liu trader

# Start scanners separately
liu scanner

# Start market miner (data collection)
liu miner
```

### Backtesting

```bash
# Run backtest for a specific batch
liu backtester --batch-id <batch_id> --start 2024-01-01 --end 2024-03-31
```

### Optimization

```bash
liu optimizer --strategy MyStrategy --params '{"threshold": [0.01, 0.05, 0.1]}'
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `liu trader` | Start live trading system |
| `liu scanner` | Run market scanners |
| `liu backtester` | Run backtesting |
| `liu optimizer` | Hyperparameter optimization |
| `liu miner` | Market data mining |
| `liu portfolio` | Portfolio analytics |

## Financial Calculations

Built-in financial calculations in `src/liualgotrader/fincalcs/`:

| Module | Functions |
|--------|-----------|
| `src/liualgotrader/fincalcs/vwap.py` | Volume-weighted average price |
| `src/liualgotrader/fincalcs/trends.py` | Trend detection and analysis |
| `src/liualgotrader/fincalcs/candle_patterns.py` | Candlestick pattern recognition |
| `src/liualgotrader/fincalcs/support_resistance.py` | Support/resistance level detection |
| `src/liualgotrader/fincalcs/resample.py` | Time series resampling |
| `src/liualgotrader/fincalcs/data_conditions.py` | Data quality checks (skip conditions) |

## Data Providers

| Provider | Module | Capabilities |
|----------|--------|-------------|
| Alpaca | `src/liualgotrader/data/alpaca.py` | Stocks: real-time + historical |
| Polygon | `src/liualgotrader/data/polygon.py` | Stocks: real-time + historical |
| Finnhub | `src/liualgotrader/data/finnhub.py` | Stocks: real-time |
| Tradier | `src/liualgotrader/data/tradier.py` | Stocks: real-time + historical |
| Gemini | `src/liualgotrader/data/gemini.py` | Crypto: real-time + historical |
| Static | `src/liualgotrader/data/static.py` | CSV/file-based data |

## Important Notes

- Strategies must inherit from `Strategy` base class
- Scanners must inherit from `Scanner` base class
- All strategy/scanner methods are async
- Database connection pool is shared via `config.db_conn_pool`
- Use `tlog()` for framework logging (not standard logging)
- Symbol names are lowercased internally
- Each consumer process has its own event loop

## Configuration Reference

### tradeplan.toml -- Scanner Section

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | str | -- | Data provider for scanner (`"polygon"`, `"alpaca"`, `"finnhub"`) |
| `min_volume` | int | -- | Minimum daily volume threshold |
| `min_gap` | float | -- | Minimum gap percentage for momentum scanner |
| `recurrence` | int | -- | Re-scan interval in minutes |
| `target_strategy_name` | str | None | Route discovered symbols to specific strategy |

### tradeplan.toml -- Strategy Section

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | str | -- | Path to Python file containing Strategy subclass |
| `schedule` | list | -- | Trading windows: `[{start = "HH:MM", duration = minutes}]` |
| Custom keys | any | -- | Passed as `**kwargs` to strategy constructor |

### config.py Runtime Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_stop` | float | `0.95` | Default stop-loss as fraction of entry price |
| `risk` | float | `0.001` | Portfolio fraction to allocate per position |
| `group_margin` | float | `0.02` | Group margin threshold |
| `market_liquidation_end_time_minutes` | int | `15` | Minutes before market close to liquidate positions |
| `proc_factor` | float | `2.0` | CPU multiplier for consumer process count (env: `CPU_FACTOR`) |
| `num_consumers` | int | `0` | Override consumer count; 0 = auto (env: `NUM_CONSUMERS`) |
| `polygon_seconds_timeout` | int | `60` | Polygon API request timeout in seconds |
| `finnhub_websocket_limit` | int | `50` | Max concurrent Finnhub WebSocket subscriptions |

## Troubleshooting

### `asyncpg.exceptions.ConnectionDoesNotExistError` or database connection failures
Verify the `DSN` environment variable contains a valid PostgreSQL connection string. The format is `postgresql://user:password@host:port/dbname`. Ensure PostgreSQL is running and the database exists. LiuAlgoTrader creates tables automatically on first run.

### `ModuleNotFoundError` for strategy file
The `filename` in `tradeplan.toml` is resolved relative to the working directory, not the TOML file location. Set `TRADEPLAN_DIR` to the directory containing both the TOML and strategy files, or use absolute paths.

### Scanner finds no symbols
Check that the data provider API key is configured correctly. The momentum scanner requires `min_volume` and `min_gap` thresholds that may filter out all symbols in low-volatility markets. Lower the thresholds for testing.

### Consumer processes crash silently
Each consumer runs in a separate process with its own event loop. Check PostgreSQL logs for connection pool exhaustion -- each consumer acquires its own pool connections. Reduce `NUM_CONSUMERS` or increase PostgreSQL `max_connections`.

### `liu trader` hangs at startup
The producer waits for scanner results before pumping data. If no scanners are configured or all scanners return empty results, the system appears idle. Add debug logging with `LIU_DEBUG_ENABLED=1` to see scanner activity.

### Backtester reports no trades for a batch
Ensure the `--batch-id` matches an existing batch in the database. Batch IDs are generated during live trading runs and stored in the `algo_run` table. Use `liu portfolio` to list available batch IDs.

### Symbol names are case-sensitive
LiuAlgoTrader lowercases symbol names internally. Strategy code should handle lowercase symbols. When querying the database, use lowercase symbol names in WHERE clauses.

### Rate limiting from data providers
Polygon and Finnhub enforce API rate limits. The framework does not auto-retry on 429 responses. Reduce scanner `recurrence` frequency and avoid running multiple instances against the same API key.

## Security Considerations

- **Database credentials**: The `DSN` environment variable contains the PostgreSQL connection string including username and password. Never log or print this value. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault) in production.
- **Broker API keys**: All broker credentials (`APCA_API_KEY_ID`, `APCA_API_SECRET_KEY`, `TRADIER_ACCESS_TOKEN`, etc.) should be set via environment variables, not configuration files. Rotate keys periodically.
- **Paper trading first**: Set `APCA_API_BASE_URL` to `https://paper-api.alpaca.markets` during development. For Tradier, use `https://sandbox.tradier.com/v1/`. This prevents accidental real-money trades.
- **Database access control**: The PostgreSQL database stores all trade history, portfolio values, and strategy parameters. Restrict network access and use SSL connections (`sslmode=require` in DSN).
- **Git commit tracking**: LiuAlgoTrader associates trade runs with git commit hashes for auditability. Ensure your trading repository does not contain credentials in its commit history.
- **Multiprocessing isolation**: Consumer processes inherit the parent's environment including all API keys. Ensure the execution environment is hardened -- do not run the trader as root or with unnecessary privileges.
- **Strategy code injection**: The `filename` parameter in `tradeplan.toml` dynamically loads and executes Python files. Only load strategy files from trusted sources. Validate file paths and do not accept user-supplied strategy paths in production.

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [Workflow](workflow.md) — Event flows and processing pipelines
- [State Management](state-management.md) — State lifecycle and data models
