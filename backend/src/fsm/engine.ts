// FSA Engine - Functional Programming Implementation
import type { State, InputSymbol, TransitionResult, ProcessResult } from './types';
import { fsaConfig, getNextState, isFinalState, isValidSymbol } from './transitions';

// Pure function to process a single transition
export const processTransition = (
  currentState: State,
  symbol: InputSymbol
): TransitionResult => {
  const nextState = getNextState(currentState, symbol);
  return {
    currentState,
    inputSymbol: symbol,
    nextState,
    isValid: nextState !== null
  };
};

// Pure function to process an input string through the FSA
export const processString = (inputString: string): ProcessResult => {
  const symbols = inputString.split('').filter(char => char.trim());

  // Validate all symbols first
  const invalidSymbols = symbols.filter(s => !isValidSymbol(s));
  if (invalidSymbols.length > 0) {
    return {
      inputString,
      accepted: false,
      finalState: fsaConfig.initialState,
      path: [fsaConfig.initialState],
      transitions: []
    };
  }

  // Process transitions using reduce for functional approach
  const result = symbols.reduce(
    (acc, symbol) => {
      const transition = processTransition(acc.currentState, symbol as InputSymbol);

      if (!transition.isValid || transition.nextState === null) {
        return { ...acc, hasError: true };
      }

      return {
        currentState: transition.nextState,
        path: [...acc.path, transition.nextState],
        transitions: [...acc.transitions, transition],
        hasError: acc.hasError
      };
    },
    {
      currentState: fsaConfig.initialState,
      path: [fsaConfig.initialState] as State[],
      transitions: [] as TransitionResult[],
      hasError: false
    }
  );

  const finalState = result.currentState;
  const accepted = isFinalState(finalState) && result.transitions.every(t => t.isValid);

  const { path, transitions } = result;

  return {
    inputString,
    accepted,
    finalState,
    path,
    transitions
  };
};

// Pure function to get available transitions from current state
export const getAvailableTransitions = (state: State): ReadonlyArray<{
  symbol: InputSymbol;
  nextState: State;
  description: string;
}> => {
  const stateTransitions = fsaConfig.transitions[state] || {};

  return Object.entries(stateTransitions)
    .filter(([_, nextState]) => nextState !== undefined)
    .map(([symbol, nextState]) => ({
      symbol: symbol as InputSymbol,
      nextState: nextState as State,
      description: `${symbol} → ${nextState}`
    }));
};

// Pure function to validate a transition
export const validateTransition = (
  fromState: State,
  symbol: InputSymbol,
  toState: State
): boolean => {
  const expectedNextState = getNextState(fromState, symbol);
  return expectedNextState === toState;
};

// Pure function to check if string is accepted
export const isStringAccepted = (inputString: string): boolean =>
  processString(inputString).accepted;
