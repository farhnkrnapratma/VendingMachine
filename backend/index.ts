// Main API - Elysia REST API for Boba Vending Machine FSA
import { Elysia } from 'elysia';
import { processString, getAvailableTransitions, validateTransition } from './src/fsm/engine';
import { fsaConfig } from './src/fsm/transitions';
import { STATE_DESCRIPTIONS, SYMBOL_DESCRIPTIONS } from './src/fsm/types';
import type { State, InputSymbol } from './src/fsm/types';

const app = new Elysia()
  .get('/', () => ({
    message: 'Boba Vending Machine FSA API',
    version: '1.0.0',
    endpoints: {
      'GET /': 'API information',
      'GET /fsm/info': 'FSA configuration details',
      'POST /fsm/process': 'Process input string through FSA',
      'GET /fsm/states': 'List all states with descriptions',
      'GET /fsm/states/:state': 'Get state details and available transitions',
      'POST /fsm/transition': 'Execute single state transition',
      'POST /fsm/validate': 'Validate a transition'
    }
  }))

  .get('/fsm/info', () => ({
    initialState: fsaConfig.initialState,
    finalStates: fsaConfig.finalStates,
    totalStates: fsaConfig.states.length,
    alphabetSize: fsaConfig.alphabet.length,
    alphabet: fsaConfig.alphabet,
    type: 'Deterministic Finite Automata (DFA)'
  }))

  .get('/fsm/states', () =>
    fsaConfig.states.map(state => ({
      state,
      description: STATE_DESCRIPTIONS[state],
      isFinal: fsaConfig.finalStates.includes(state),
      isInitial: state === fsaConfig.initialState
    }))
  )

  .get('/fsm/states/:state', ({ params: { state }, set }) => {
    if (!fsaConfig.states.includes(state as State)) {
      set.status = 404;
      return { error: 'State not found', validStates: fsaConfig.states };
    }

    const typedState = state as State;
    return {
      state: typedState,
      description: STATE_DESCRIPTIONS[typedState],
      isFinal: fsaConfig.finalStates.includes(typedState),
      isInitial: typedState === fsaConfig.initialState,
      availableTransitions: getAvailableTransitions(typedState)
    };
  })

  .post('/fsm/process', ({ body, set }) => {
    const { inputString } = body as { inputString: string };

    if (!inputString || typeof inputString !== 'string') {
      set.status = 400;
      return { error: 'inputString is required and must be a string' };
    }

    const result = processString(inputString);

    return {
      success: result.accepted,
      ...result,
      message: result.accepted
        ? 'String accepted - Transaction completed successfully'
        : 'String rejected - Invalid transaction sequence'
    };
  })

  .post('/fsm/transition', ({ body, set }) => {
    const { currentState, symbol } = body as { currentState: State; symbol: InputSymbol };

    if (!currentState || !symbol) {
      set.status = 400;
      return { error: 'currentState and symbol are required' };
    }

    if (!fsaConfig.states.includes(currentState)) {
      set.status = 404;
      return { error: 'Invalid state', validStates: fsaConfig.states };
    }

    if (!fsaConfig.alphabet.includes(symbol)) {
      set.status = 400;
      return { error: 'Invalid symbol', validSymbols: fsaConfig.alphabet };
    }

    const nextState = fsaConfig.transitions[currentState]?.[symbol];

    if (!nextState) {
      set.status = 422;
      return {
        error: 'No valid transition',
        currentState,
        symbol,
        availableTransitions: getAvailableTransitions(currentState)
      };
    }

    return {
      success: true,
      transition: {
        from: currentState,
        symbol,
        to: nextState,
        symbolDescription: SYMBOL_DESCRIPTIONS[symbol],
        fromDescription: STATE_DESCRIPTIONS[currentState],
        toDescription: STATE_DESCRIPTIONS[nextState]
      }
    };
  })

  .post('/fsm/validate', ({ body }) => {
    const { fromState, symbol, toState } = body as {
      fromState: State;
      symbol: InputSymbol;
      toState: State;
    };

    const isValid = validateTransition(fromState, symbol, toState);
    const expectedState = fsaConfig.transitions[fromState]?.[symbol];

    return {
      valid: isValid,
      expected: expectedState,
      provided: toState,
      message: isValid ? 'Valid transition' : 'Invalid transition'
    };
  })

  .listen(3000);

console.log(`🚀 Boba Vending Machine FSA API running at http://localhost:${app.server?.port}`);
