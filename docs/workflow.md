# LiuAlgoTrader -- Workflow

## Trading Day Workflow

```mermaid
sequenceDiagram
    participant SC as Scanners
    participant P as Producer
    participant Q as Queues
    participant C as Consumer
    participant S as Strategy
    participant T as Trader
    participant DB as PostgreSQL

    Note over SC,DB: Pre-market / Market Open
    
    SC->>SC: Run scanner (momentum, custom)
    SC->>P: Push discovered symbols via scanner_queue
    P->>P: Subscribe to WebSocket streams for new symbols
    P->>DB: Save trending tickers

    loop Market Data Streaming
        P->>P: Receive WebSocket event (SEC_AGG, MIN_AGG, TRADE)
        P->>Q: Route event to consumer queue (hash by symbol)
        Q->>C: Consumer receives event
        
        loop For each strategy
            C->>S: Execute strategy.run(symbol, data)
            
            alt Strategy returns trade signal
                S-->>C: {side: 'buy', qty: 100, type: 'limit'}
                C->>T: Submit order via trader
                T->>DB: Persist trade record
            else No signal
                Note over S: Skip
            end
        end
    end

    Note over SC,DB: Market Close
    C->>S: Notify end of trading
    S->>DB: Update algo_run end time
```

## Scanner Iteration Flow

```mermaid
sequenceDiagram
    participant SR as ScannerRunner
    participant SC as Scanner
    participant DL as DataLoader
    participant SQ as ScannerQueue
    participant P as Producer

    SR->>SC: scanner.run()
    SC->>DL: Query market data
    DL-->>SC: Symbol data
    SC->>SC: Filter by criteria
    SC-->>SR: List of symbols
    SR->>SQ: Push symbol details (JSON)
    
    P->>SQ: Poll for new symbols
    SQ-->>P: New symbol list
    P->>P: Subscribe to WebSocket streams
    
    opt Recurrence configured
        Note over SR: Wait recurrence interval
        SR->>SC: scanner.run() again
    end
```

## Backtesting Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant BT as Backtester
    participant DB as PostgreSQL
    participant S as Strategy
    participant DL as DataLoader

    U->>BT: Run backtest (batch_id, strategy, date_range)
    BT->>DB: Load historical trades for batch
    BT->>DL: Load market data for date range
    
    loop For each trading day
        loop For each minute bar
            BT->>S: strategy.run(symbol, data, now)
            S-->>BT: Trade decision
            BT->>BT: Simulate execution
            BT->>DB: Record simulated trade
        end
    end
    
    BT->>U: Return results with analytics
```

## Strategy Execution Modes

```mermaid
graph TB
    subgraph "run() Mode - Per Symbol"
        R1[Receive data for single symbol]
        R2[Apply strategy logic]
        R3[Return trade decision]
        R1 --> R2 --> R3
    end

    subgraph "run_all() Mode - Portfolio"
        RA1[Receive all symbol positions]
        RA2[Cross-symbol analysis]
        RA3[Return portfolio-wide decisions]
        RA1 --> RA2 --> RA3
    end

    C[Consumer] --> |should_run_all() = False| R1
    C --> |should_run_all() = True| RA1
```

## Optimization Workflow

```mermaid
sequenceDiagram
    participant U as User
    participant O as Optimizer
    participant BT as Backtester
    participant S as Strategy
    participant DB as PostgreSQL

    U->>O: Define hyperparameter space
    
    loop For each parameter combination
        O->>S: Create strategy with params
        O->>BT: Run backtest
        BT-->>O: Performance metrics
        O->>O: Record results
    end
    
    O->>DB: Store optimization results
    O->>U: Return best parameters
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Market Data Sources"
        WS[WebSocket Streams]
        REST[REST APIs]
        CSV[Static CSV]
    end

    subgraph "Data Layer"
        SF[StreamingFactory]
        DF[DataFactory]
        DL[DataLoader]
    end

    subgraph "Processing"
        P[Producer]
        MPQ[Multiprocessing Queues]
        C[Consumers]
    end

    subgraph "Persistence"
        DB[(PostgreSQL)]
        TR[Trades Table]
        AN[Analytics Table]
        PS[Portfolio Stats]
    end

    WS --> SF
    REST --> DF
    CSV --> DF
    SF --> P
    DF --> DL
    DL --> C
    P --> MPQ
    MPQ --> C
    C --> DB
    DB --> TR
    DB --> AN
    DB --> PS
```

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [State Management](state-management.md) — State lifecycle and data models
- [Development](development.md) — Development guide and best practices
