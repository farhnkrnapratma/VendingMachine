# Boba Vending Machine - Finite State Automata

Complete FSA implementation with REST API and interactive CLI for simulating a Boba tea vending machine transaction system.

## Technical Stack

- **Runtime**: Bun (latest)
- **Framework**: Elysia
- **Language**: TypeScript
- **Programming Style**: Functional
- **Architecture**: Modular with max 150 lines per file

## FSA Specification

### Formal Definition

**M = (Q, Σ, δ, S, F)** where:

- **Q**: Set of states = {q0, q1, q2, ..., q17}
- **Σ**: Input alphabet = {a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, 1, 2}
- **δ**: Transition function (see transition table)
- **S**: Initial state = q0
- **F**: Final states = {q17}

### State Descriptions

```
q0  → Initial State
q1  → Select Product
q2  → Select Payment Method
q3  → Non-Cash Payment
q4  → Cash Payment
q5  → Calculate Balance (Non-Cash)
q6  → Input Cash 5000
q7  → Input Cash 10000
q8  → Check Balance (Non-Cash)
q9  → Calculate Balance (Cash)
q10 → Check Balance (Cash)
q11 → Return Money (Non-Cash)
q12 → Dispense Product (Non-Cash)
q13 → Dispense Product (Cash)
q14 → Return Money (Cash)
q15 → Calculate Change
q16 → Dispense Change
q17 → Transaction Complete (Final State)
```

### State Transition Diagram (ASCII)

```
                    ┌───────────────────┐
                    │   q17 (Final)     │
                    │  Transaction Done │
                    └─────────▲─────────┘
                              │ u
                    ┌─────────┴─────────┐
                    │   q16             │
                    │ Dispense Change   │
                    └─────────▲─────────┘
                              │ t
                    ┌─────────┴─────────┐
                    │   q15             │
                    │ Calculate Change  │
                    └───────▲─────▲─────┘
                          r │     │ r
              ┌─────────────┘     └────────────┐
              │                                │
    ┌─────────┴─────────┐          ┌───────────┴────────┐
    │   q12             │          │   q13              │
    │ Dispense (Non-$)  │          │ Dispense (Cash)    │
    └─────────▲─────────┘          └───────────▲────────┘
            n │                              q │
    ┌─────────┴─────────┐          ┌───────────┴────────┐
    │   q8              │          │   q10              │
    │ Check Balance($)  │          │ Check Balance(¥)   │
    └───┬─────────────▲─┘          └────┬──────────▲────┘
      k │           l │                o│         n│
    ┌───▼─────────┐   │          ┌──────▼────┐     │
    │   q11       │   │          │   q14     │     │
    │ Return ($)  │   │          │Return (¥) │     │
    └───┬─────────┘   │          └──────┬────┘     │
      p │             │                s│          │
    ┌───▼─────────────┴─┐          ┌────▼──────────┴─────┐
    │   q5              │          │   q9                │
    │ Calculate Bal($)  │          │ Calculate Bal(¥)    │
    └─────────▲─────────┘          └─────────▲───────────┘
            g │                          h,i │
    ┌─────────┴─────────┐          ┌─────────┴───────────┐
    │   q3              │          │   q6        q7      │
    │ Non-Cash Payment  ├──────────┤  5K (1)     10K (2) │
    └───────────────────┘    d     └─────────────────────┘
              │                              ▲
            d │                          e,f │
              │                              │
    ┌─────────▼─────────┐          ┌─────────┴───────────┐
    │   q2              │          │   q4                │
    │ Payment Selection ├──────────┤  Cash Payment       │
    └─────────▲─────────┘    c     └─────────────────────┘
            b │
    ┌─────────┴─────────┐
    │   q1              │
    │ Select Product    │
    └─────────▲─────────┘
            a │
    ┌─────────┴─────────┐
    │   q0              │
    │  Initial State    │
    └───────────────────┘
```

## Quick Start

### 1. Start the Backend API

```bash
cd backend
bun install
bun run start
```

The API will be available at `http://localhost:3000`

### 2. Use the CLI Client

In a new terminal:

```bash
cd cli
bun run start
```

Follow the interactive menu to explore the FSA!

## API Endpoints

### 1. Get API Information

```bash
curl http://localhost:3000/
```

**Response**: API overview and available endpoints

### 2. Get FSA Configuration

```bash
curl http://localhost:3000/fsm/info
```

**Response**:
```json
{
  "initialState": "q0",
  "finalStates": ["q17"],
  "totalStates": 18,
  "alphabetSize": 23,
  "alphabet": ["a", "b", "c", ...],
  "type": "Deterministic Finite Automata (DFA)"
}
```

### 3. List All States

```bash
curl http://localhost:3000/fsm/states
```

**Response**: Array of all states with descriptions

### 4. Get State Details

```bash
curl http://localhost:3000/fsm/states/q0
```

**Response**:
```json
{
  "state": "q0",
  "description": "Initial State",
  "isFinal": false,
  "isInitial": true,
  "availableTransitions": [{"symbol": "a", "nextState": "q1", "description": "a → q1"}]
}
```

### 5. Process Input String

```bash
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abdgjlrtu"}'
```

**Response** (Success - 200):
```json
{
  "success": true,
  "inputString": "abdgjlrtu",
  "accepted": true,
  "finalState": "q17",
  "path": ["q0", "q1", "q2", "q3", "q5", "q8", "q12", "q15", "q16", "q17"],
  "transitions": [...],
  "message": "String accepted - Transaction completed successfully"
}
```

**Response** (Rejected - 200):
```json
{
  "success": false,
  "inputString": "abcfimot",
  "accepted": false,
  "finalState": "q4",
  "path": [...],
  "message": "String rejected - Invalid transaction sequence"
}
```

### 6. Execute Single Transition

```bash
curl -X POST http://localhost:3000/fsm/transition \
  -H "Content-Type: application/json" \
  -d '{"currentState": "q0", "symbol": "a"}'
```

**Response** (Valid - 200):
```json
{
  "success": true,
  "transition": {
    "from": "q0",
    "symbol": "a",
    "to": "q1",
    "symbolDescription": "Start",
    "fromDescription": "Initial State",
    "toDescription": "Select Product"
  }
}
```

**Response** (Invalid - 422):
```json
{
  "error": "No valid transition",
  "currentState": "q0",
  "symbol": "z",
  "availableTransitions": [...]
}
```

### 7. Validate Transition

```bash
curl -X POST http://localhost:3000/fsm/validate \
  -H "Content-Type: application/json" \
  -d '{"fromState": "q0", "symbol": "a", "toState": "q1"}'
```

**Response**:
```json
{
  "valid": true,
  "expected": "q1",
  "provided": "q1",
  "message": "Valid transition"
}
```

## Test Cases

The following input strings should be **ACCEPTED**:

```bash
# Test Case 1: Non-cash payment, sufficient balance
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abdgjlrtu"}'

# Test Case 2: Cash payment with exact amount
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcehkmstu"}'

# Test Case 3: Cash payment with 10K input
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcfikmstu"}'

# Test Case 4: Non-cash with retry after insufficient balance
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abdgjlnpgjlrtu"}'

# Test Case 5: Cash 5K with retry
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcehkmoqehkmstu"}'

# Test Case 6: Cash 10K with retry
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcfikmoqfikmstu"}'

# Test Case 7: Cash 5K with additional deposit
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abce1hkmoqehkmstu"}'

# Test Case 8: Cash 10K with additional deposit
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcf2ikmoqfikmstu"}'
```

## Error Codes

- **200**: Success - Valid request, includes both accepted and rejected strings
- **400**: Bad Request - Missing or invalid parameters
- **404**: Not Found - Invalid state
- **422**: Unprocessable Entity - No valid transition exists

## Project Structure

```
.
├── backend/                    # Backend REST API
│   ├── index.ts               # Main API server (Elysia)
│   ├── src/fsm/
│   │   ├── types.ts           # Type definitions (81 lines)
│   │   ├── transitions.ts     # Transition table (57 lines)
│   │   └── engine.ts          # FSA engine (102 lines)
│   └── package.json
│
├── cli/                        # Interactive CLI Client (Python)
│   ├── main.py                # Entry point
│   ├── pyproject.toml         # Project configuration
│   ├── src/boba_cli/
│   │   ├── main.py            # Main application logic
│   │   ├── api_client.py      # API communication
│   │   ├── display.py         # Terminal UI components
│   │   ├── interactive.py     # Interactive transaction mode
│   │   └── commands.py        # Command handlers
│   └── README.md              # CLI documentation
│
└── README.md                  # This file
```

## CLI Features

The interactive CLI provides:

1. **Process Input Strings** - Test any string against the FSA
2. **View FSM Information** - Display complete configuration
3. **List All States** - Browse all 18 states with descriptions
4. **View State Details** - Inspect individual states and transitions
5. **Execute Single Transitions** - Step through transitions manually
6. **Test Examples** - Run predefined test cases
7. **Interactive Mode** - Navigate the FSA step-by-step
8. **Help & Documentation** - API reference and examples

See [cli/README.md](cli/README.md) for detailed CLI documentation.

## Implementation Notes

- **Functional Programming**: All core logic uses pure functions
- **Immutability**: State transitions don't modify existing data
- **Type Safety**: Full TypeScript typing for all FSA components
- **DFA Properties**: Deterministic (one transition per state-symbol pair)
- **No External State Management**: Uses pure functional approach
- **File Size**: Each file ≤ 154 lines
- **Modular Design**: Separate backend and CLI packages

## Components

### Backend API (379 lines total)
- RESTful endpoints for all FSA operations
- Elysia framework with Bun runtime
- Stateless, functional design

### CLI Client (Python-based)
- Interactive terminal interface
- Rich terminal UI with colors and tables
- Real-time API communication
- Step-by-step navigation mode

## License

GPLv3