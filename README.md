# 🧋 Boba Vending Machine - FSA Simulator

Complete implementation of a Finite State Automata (FSA) based vending machine simulator for boba tea transactions.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## 📋 Overview

This project implements a **Deterministic Finite Automata (DFA)** for simulating boba vending machine transactions with complete transaction flows including:

- 💰 **Dual Payment Methods**: Cash and non-cash (QR code) payment
- 🔄 **Retry Mechanisms**: Handle insufficient balance scenarios
- 💵 **Change Calculation**: Automatic change dispensing for cash payments
- 📊 **18 States**: Complete transaction state machine
- 🔤 **23 Input Symbols**: Full alphabet for all operations

## 🏗️ Project Architecture

```
.
├── backend/                          # REST API Server (Bun + Elysia)
│   ├── index.ts                      # Main API server
│   ├── src/fsm/
│   │   ├── types.ts                  # FSA type definitions
│   │   ├── transitions.ts            # State transition table
│   │   └── engine.ts                 # FSA processing engine
│   ├── package.json
│   └── README.md
│
├── cli/                              # Interactive CLI Client (Python)
│   ├── main.py                       # CLI entry point
│   ├── pyproject.toml                # Python dependencies
│   ├── src/boba_cli/
│   │   ├── main.py                   # Main application
│   │   ├── api_client.py             # Backend API client
│   │   ├── display.py                # Rich terminal UI
│   │   ├── interactive.py            # Interactive transaction mode
│   │   └── commands.py               # CLI commands
│   └── README.md
│
└── README.md                          # This file
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: [Bun](https://bun.sh) runtime (latest)
- **CLI**: Python 3.10+ and [uv](https://github.com/astral-sh/uv) package manager

### 1. Start the Backend

```bash
cd backend
bun install
bun run start
```

The API will be available at `http://localhost:3000`

### 2. Launch the CLI

In a new terminal:

```bash
cd cli
uv sync
uv run python main.py
# OR
uv run boba
```

## 📊 FSA Specification

### Formal Definition

**M = (Q, Σ, δ, S, F)** where:

- **Q** (States): 18 states {q0, q1, q2, ..., q17}
- **Σ** (Alphabet): 23 symbols {a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, 1, 2}
- **δ** (Transition Function): 37 state transitions
- **S** (Initial State): q0
- **F** (Final States): {q17}

### State Overview

| State | Description | Type |
|-------|-------------|------|
| q0 | Initial State | Initial |
| q1 | Select Product | - |
| q2 | Select Payment Method | - |
| q3 | Non-Cash Payment | - |
| q4 | Cash Payment | - |
| q5 | Calculate Balance (Non-Cash) | - |
| q6 | Input Cash 5000 | - |
| q7 | Input Cash 10000 | - |
| q8 | Check Balance (Non-Cash) | - |
| q9 | Calculate Balance (Cash) | - |
| q10 | Check Balance (Cash) | - |
| q11 | Return Money (Non-Cash) | - |
| q12 | Dispense Product (Non-Cash) | - |
| q13 | Dispense Product (Cash) | - |
| q14 | Return Money (Cash) | - |
| q15 | Calculate Change | - |
| q16 | Dispense Change | - |
| q17 | Transaction Complete | Final |

### Symbol Meanings

| Symbol | Description | Symbol | Description |
|--------|-------------|--------|-------------|
| a | Start transaction | n | Dispense product (non-cash) |
| b | Select product | o | Insufficient balance (cash) |
| c | Choose payment method | p | Refund non-cash payment |
| d | Non-cash payment | q | Dispense product (cash) |
| e | Insert Rp 5,000 | r | Calculate change |
| f | Insert Rp 10,000 | s | No change needed |
| g | Process non-cash payment | t | Change available |
| h | Scan QR code | u | Dispense change |
| i | Add Rp 10,000 | 1 | Add Rp 5,000 (additional) |
| j | Check balance | 2 | Add Rp 10,000 (additional) |
| k | Insufficient balance | | |
| l | Sufficient balance | | |
| m | Return to selection | | |

## 🧪 Example Transactions

### Non-Cash Payment (Simple)

```bash
# Input string: abdgjlrtu
# Result: Accept ✓

curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abdgjlrtu"}'
```

**Path:** q0 → q1 → q2 → q3 → q5 → q8 → q12 → q15 → q16 → q17

### Cash Payment with Retry

```bash
# Input string: abcehkmoqehkmstu
# Result: Accept ✓

curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abcehkmoqehkmstu"}'
```

**Path:** q0 → q1 → q2 → q4 → q6 → q9 → q10 → q13 → q14 → q4 → q6 → q9 → q10 → q13 → q15 → q16 → q17

### All Test Strings

| # | Input String | Result | Description |
|---|--------------|--------|-------------|
| 1 | `abdgjlrtu` | ✅ Accept | Non-cash, sufficient balance |
| 2 | `abcehkmstu` | ✅ Accept | Cash 5K, exact amount |
| 3 | `abcfikmstu` | ✅ Accept | Cash 10K, with change |
| 4 | `abdgjlnpgjlrtu` | ✅ Accept | Non-cash with retry |
| 5 | `abcehkmoqehkmstu` | ✅ Accept | Cash 5K with retry |
| 6 | `abcfikmoqfikmstu` | ✅ Accept | Cash 10K with retry |
| 7 | `abce1hkmoqehkmstu` | ✅ Accept | Cash 5K with additional deposit |
| 8 | `abcf2ikmoqfikmstu` | ✅ Accept | Cash 10K with additional deposit |

## 🎯 Features

### Backend API
- ✅ RESTful API with 7 endpoints
- ✅ Complete FSA implementation (18 states, 23 symbols, 37 transitions)
- ✅ Pure functional programming approach
- ✅ Type-safe with TypeScript
- ✅ Fast runtime with Bun + Elysia
- ✅ Stateless design

### CLI Client
- ✅ Interactive transaction mode (step-by-step guidance)
- ✅ Direct string testing
- ✅ FSA information browser
- ✅ State explorer with transitions
- ✅ Predefined test examples
- ✅ Beautiful Rich terminal UI
- ✅ Built-in help system

## 📚 Documentation

- **[Backend API Documentation](backend/README.md)** - Complete API reference with endpoints, examples, and specifications
- **[CLI User Guide](cli/README.md)** - Interactive CLI usage, commands, and examples

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/fsm/info` | FSA configuration |
| GET | `/fsm/states` | List all states |
| GET | `/fsm/states/:state` | Get state details |
| POST | `/fsm/process` | Process input string |
| POST | `/fsm/transition` | Execute single transition |
| POST | `/fsm/validate` | Validate transition |

## 🧬 Implementation Details

### Technology Stack

**Backend:**
- Runtime: Bun (JavaScript/TypeScript)
- Framework: Elysia (REST API)
- Language: TypeScript
- Style: Functional programming
- Lines of Code: 379 lines

**CLI:**
- Runtime: Python 3.10+
- Package Manager: uv
- UI Library: Rich
- HTTP Client: Requests
- Lines of Code: 763 lines

### Design Principles

1. **Pure Functions**: All FSA logic uses pure, side-effect-free functions
2. **Immutability**: State transitions never modify existing data
3. **Type Safety**: Complete TypeScript typing for compile-time guarantees
4. **Deterministic**: One transition per state-symbol pair (DFA property)
5. **Modular**: Clear separation between API, FSA engine, and CLI

## 🧪 Testing

### Test the Backend

```bash
cd backend
bun run start

# In another terminal:
curl http://localhost:3000/
curl http://localhost:3000/fsm/info
curl -X POST http://localhost:3000/fsm/process \
  -H "Content-Type: application/json" \
  -d '{"inputString": "abdgjlrtu"}'
```

### Test the CLI

```bash
cd cli
uv sync
uv run python main.py

# Follow the interactive menu:
# 1. Try interactive transaction mode
# 2. Test input strings
# 6. Run test examples
```

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Install Bun if not already installed
curl -fsSL https://bun.sh/install | bash

# Reinstall dependencies
cd backend
rm -rf node_modules
bun install
bun run start
```

### CLI Can't Connect

```bash
# Ensure backend is running first
cd backend
bun run start

# Then start CLI in new terminal
cd cli
uv sync
uv run python main.py
```

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000
# OR
netstat -tulpn | grep 3000

# Kill the process
kill -9 <PID>
```

## 📜 License

This project is licensed under the GNU General Public License v3.0 - see below for details.

```
Copyright (C) 2025 Reidho Satria

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

## 🔗 Related Resources

- **Bun Runtime**: https://bun.sh
- **Elysia Framework**: https://elysiajs.com
- **Python Rich Library**: https://rich.readthedocs.io
- **UV Package Manager**: https://github.com/astral-sh/uv
- **FSA Theory**: https://en.wikipedia.org/wiki/Finite-state_machine
