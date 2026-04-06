# LiuAlgoTrader -- State Management

## Strategy Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Instantiated: Strategy loaded from tradeplan.toml
    Instantiated --> Creating: create() called
    
    state Creating {
        [*] --> SaveAlgoRun: Persist to DB
        SaveAlgoRun --> CheckConditions: Return True/False
    }
    
    Creating --> Active: create() returns True
    Creating --> Disabled: create() returns False
    
    state Active {
        [*] --> WaitingForData
        WaitingForData --> Processing: Data received
        Processing --> DecisionMade: run() / run_all()
        DecisionMade --> OrderSubmitted: Trade signal generated
        DecisionMade --> WaitingForData: No signal
        OrderSubmitted --> WaitingForData: Order executed
    }
    
    Active --> EndOfDay: Market closes
    EndOfDay --> RecordEndTime: Update algo_run
    RecordEndTime --> [*]
```

## Strategy Types

```mermaid
stateDiagram-v2
    [*] --> StrategyType
    
    state StrategyType {
        DAY_TRADE: Exit all positions by market close
        SWING: Hold positions overnight
    }
    
    StrategyType --> DAY_TRADE
    StrategyType --> SWING
```

## AlgoRun State

Each strategy execution is tracked as an `AlgoRun` in the database:

| Field | Description |
|-------|-------------|
| `algo_run_id` | Unique run identifier |
| `strategy_name` | Strategy name from tradeplan |
| `batch_id` | Batch grouping for related runs |
| `start_time` | Execution start timestamp |
| `end_time` | Execution end timestamp |
| `end_reason` | Why the run ended |
| `ref_algo_run_id` | Reference run for backtesting |

## Consumer Process State

```mermaid
stateDiagram-v2
    [*] --> Started: Process spawned
    Started --> Connected: DB connection established
    Connected --> StrategiesLoaded: Load from tradeplan
    StrategiesLoaded --> Listening: Wait for queue events
    
    state Listening {
        [*] --> WaitForEvent
        WaitForEvent --> EventReceived: Queue.get()
        EventReceived --> SkipCondition: Check data conditions
        SkipCondition --> ExecuteStrategies: Data valid
        SkipCondition --> WaitForEvent: Skip (bad data)
        ExecuteStrategies --> ProcessResults: Handle trade signals
        ProcessResults --> WaitForEvent
    }
    
    Listening --> Shutdown: Market close / error
    Shutdown --> EndTimeUpdate: Update all strategy end times
    EndTimeUpdate --> [*]
```

## Producer State

```mermaid
stateDiagram-v2
    [*] --> Initialized: Producer started
    Initialized --> DBConnected: Create DB connection
    DBConnected --> StreamConnected: Connect to data stream
    
    state Running {
        [*] --> Polling
        Polling --> CheckScanners: Check scanner queue
        CheckScanners --> NewSymbols: Scanner found symbols
        NewSymbols --> Subscribe: Subscribe to WebSocket
        Subscribe --> Polling
        CheckScanners --> Polling: No new symbols
        
        Polling --> DataReceived: WebSocket event
        DataReceived --> RouteToQueue: Hash symbol to queue
        RouteToQueue --> Polling
    }
    
    StreamConnected --> Running
    Running --> Disconnected: Stream error
    Disconnected --> Reconnecting: Auto-reconnect
    Reconnecting --> Running: Success
    Running --> Stopped: Market close
    Stopped --> [*]
```

## Trade State Machine

```mermaid
stateDiagram-v2
    [*] --> SignalGenerated: Strategy produces trade signal
    SignalGenerated --> Validated: Check position / balance
    Validated --> Submitted: Trader.submit_order()
    
    state "Execution" as exec {
        Submitted --> Filled: Order executed
        Submitted --> PartialFill: Partial execution
        PartialFill --> Filled: Complete
        Submitted --> Rejected: Broker rejects
    }
    
    Filled --> Persisted: Save to DB (NewTrade)
    Persisted --> Tracked: Update gain/loss
    Tracked --> [*]
    Rejected --> Logged: Log rejection
    Logged --> [*]
```

## Portfolio State

```mermaid
stateDiagram-v2
    [*] --> Created: Portfolio created in DB
    Created --> Active: Trades assigned
    
    state Active {
        [*] --> Calculating
        Calculating --> Valued: Compute portfolio value
        Valued --> Analyzing: Run analytics
        Analyzing --> Updated: Update stats
        Updated --> Calculating: New trade
    }
    
    Active --> Closed: All positions liquidated
    Closed --> Archived: End of day
    Archived --> [*]
```

## Database Schema State

Key database tables and their relationships:

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `algo_run` | Strategy execution tracking | algo_run_id, strategy_name, batch_id |
| `new_trades` | Individual trade records | trade_id, algo_run_id, symbol, side, qty, price |
| `trending_tickers` | Scanner-discovered symbols | batch_id, symbol, timestamp |
| `portfolio` | Portfolio definitions | portfolio_id, external_account_id |
| `accounts` | Account balances | account_id, balance |
| `gain_loss` | Profit/loss tracking | symbol, gain_loss, algo_run_id |
| `ticker_data` | Symbol metadata | symbol, data |
| `optimizer` | Optimization results | parameters, performance |

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [Workflow](workflow.md) — Event flows and processing pipelines
- [Development](development.md) — Development guide and best practices
