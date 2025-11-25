# 🧋 Boba Vending Machine CLI

Interactive command-line interface for the Boba Vending Machine Finite State Automata (FSA) simulator.

## Overview

This Python CLI provides a user-friendly way to interact with the Boba Vending Machine FSA backend. It offers both interactive transaction mode and direct string testing capabilities, making it easy to understand and demonstrate FSA-based transaction systems.

## Features

- 🛒 **Interactive Transaction Mode** - Step-by-step guided transaction process
- 🧪 **String Testing** - Directly test input sequences against the FSA
- 📊 **FSA Information** - View complete automata configuration
- 📝 **State Browser** - List and inspect all FSA states
- ✨ **Test Examples** - Run predefined valid transaction sequences
- 🎨 **Beautiful UI** - Rich terminal interface with colors and tables
- ❓ **Built-in Help** - Comprehensive documentation and symbol reference

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Backend API running at `http://localhost:3000`

### Installation

1. **Navigate to the CLI directory:**
   ```bash
   cd cli
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

### Running the Application

**Option 1: Using Python directly**
```bash
uv run python main.py
```

**Option 2: Using the boba command**
```bash
uv run boba
```

**Option 3: Activate virtual environment**
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

## Usage

### Main Menu

When you start the application, you'll see the main menu:

```
┌────────┬──────────────────────────────────────────────┐
│ Option │ Description                                  │
├────────┼──────────────────────────────────────────────┤
│ 1      │ 🛒 Start Transaction (Interactive Mode)      │
│ 2      │ 🧪 Test Input String                         │
│ 3      │ 📊 View FSA Information                      │
│ 4      │ 📝 List All States                           │
│ 5      │ 🔍 View State Details                        │
│ 6      │ ✨ Run Test Examples                         │
│ 7      │ ❓ Help & Documentation                      │
│ 0      │ 🚪 Exit                                       │
└────────┴──────────────────────────────────────────────┘
```

### 1. Interactive Transaction Mode

Perfect for first-time users! The interactive mode guides you through a complete transaction step-by-step:

1. Select option **1** from the main menu
2. Follow the prompts to:
   - Start the transaction
   - Select a product
   - Choose payment method (cash or non-cash)
   - Complete payment
   - Receive your boba!

**Example Flow:**
```
Current State: q0 - Initial State
Available Actions:
1. Start Transaction

Current State: q1 - Select Product
Available Actions:
1. Select Product

Current State: q2 - Select Payment Method
Available Actions:
1. Select Non-Cash Payment
2. Select Cash Payment

... and so on
```

### 2. Test Input String

For advanced users who want to test specific input sequences:

1. Select option **2**
2. Enter a string of symbols (e.g., `abdgjlrtu`)
3. View the complete transaction path and result

**Valid Test Strings:**
```
abdgjlrtu       → Non-cash payment, sufficient balance
abcehkmstu      → Cash payment (5K), exact amount
abcfikmstu      → Cash payment (10K), with change
abdgjlnpgjlrtu  → Non-cash with retry after insufficient balance
```

### 3. View FSA Information

Displays the complete FSA configuration:
- Initial state
- Final states
- Total number of states
- Alphabet (all valid symbols)
- FSA type (DFA)

### 4. List All States

Browse all 18 states with their descriptions and types (Initial/Final).

### 5. View State Details

Inspect a specific state to see:
- State description
- Available transitions
- Next states for each valid symbol

### 6. Run Test Examples

Execute predefined test cases to see how different transaction flows work:
- Run individual test cases
- Run all tests at once
- View detailed transaction paths

### 7. Help & Documentation

View comprehensive help including:
- Symbol meanings
- Usage tips
- Transaction flow explanation
- FSA state information

## Symbol Reference

| Symbol | Description                  | Balance Change |
|--------|------------------------------|----------------|
| a      | Start transaction            | -              |
| b      | Select product               | -              |
| c      | Choose payment method        | -              |
| d      | Non-cash payment             | -              |
| e      | Insert Rp 5,000             | +5,000         |
| f      | Insert Rp 10,000            | +10,000        |
| g      | Process non-cash payment     | -              |
| h      | Scan QR code                 | +15,000        |
| i      | Add Rp 10,000               | +10,000        |
| j      | Check balance                | -              |
| k      | Insufficient balance         | -              |
| l      | Sufficient balance           | -              |
| m      | Return to selection          | -              |
| n      | Dispense product (non-cash)  | -              |
| o      | Insufficient cash balance    | -              |
| p      | Refund non-cash payment      | -              |
| q      | Dispense product (cash)      | -              |
| r      | Calculate change             | -              |
| s      | No change needed             | -              |
| t      | Change available             | -              |
| u      | Dispense change              | -              |
| 1      | Add Rp 5,000 (additional)   | +5,000         |
| 2      | Add Rp 10,000 (additional)  | +10,000        |

## Project Structure

```
cli/
├── main.py                          # Entry point
├── pyproject.toml                   # Project configuration
├── uv.lock                          # Dependency lock file
├── README.md                        # This file
└── src/
    └── boba_cli/
        ├── __init__.py              # Package initialization
        ├── main.py                  # Main application logic
        ├── api_client.py            # API communication
        ├── display.py               # Terminal UI components
        ├── interactive.py           # Interactive transaction mode
        └── commands.py              # Command handlers
```

## Example Transactions

### Non-Cash Payment (Simple)

**Input String:** `abdgjlrtu`

**Path:**
1. q0 → Start (a)
2. q1 → Select Product (b)
3. q2 → Choose Payment (d)
4. q3 → Non-Cash Payment (g)
5. q5 → Calculate Balance (j)
6. q8 → Check Balance (l)
7. q12 → Dispense Product (r)
8. q15 → Calculate Change (t)
9. q16 → Dispense Change (u)
10. q17 → Complete ✓

### Cash Payment with Change

**Input String:** `abcfikmstu`

**Path:**
1. q0 → q1 (a) - Start transaction
2. q1 → q2 (b) - Select product
3. q2 → q4 (c) - Choose cash payment
4. q4 → q7 (f) - Insert Rp 10,000
5. q7 → q9 (i) - Scan QR / Complete cash input
6. q9 → q10 (k) - Check balance (insufficient)
7. q10 → q13 (m) - Balance sufficient, dispense
8. q13 → q15 (s) - No change needed
9. q15 → q16 (t) - Change available
10. q16 → q17 (u) - Dispense change
11. q17 → Complete ✓

## Troubleshooting

### "Cannot connect to backend API"

**Solution:** Ensure the backend server is running:
```bash
cd ../backend
bun install
bun run start
```

The backend should be accessible at `http://localhost:3000`.

### "Module not found" error

**Solution:** Install dependencies:
```bash
uv sync
```

### Virtual environment issues

**Solution:** Recreate the virtual environment:
```bash
rm -rf .venv
uv sync
```

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the application
python main.py
```

### Adding New Features

The codebase is modular:
- **api_client.py** - Add new API endpoints
- **display.py** - Add new UI components
- **commands.py** - Add new menu commands
- **interactive.py** - Modify transaction flow

## Technical Details

- **Runtime:** Python 3.10+
- **Package Manager:** uv
- **UI Library:** Rich (terminal formatting)
- **HTTP Client:** Requests
- **Architecture:** Modular, functional design
- **API Communication:** RESTful HTTP/JSON

## License

GPLv3

## Related

- [Backend API Documentation](../backend/README.md)