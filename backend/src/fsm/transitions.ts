// FSA Transition Table - Corrected based on research paper test cases
import type { TransitionTable, FSAConfig, State, InputSymbol } from './types';

export const transitionTable: TransitionTable = {
  q0: { a: 'q1' },
  q1: { b: 'q2' },
  q2: { c: 'q4', d: 'q3' },
  q3: { d: 'q3', g: 'q5' },
  q4: { e: 'q6', f: 'q7' },
  q5: { j: 'q8' },
  q6: { '1': 'q6', h: 'q9' },
  q7: { '2': 'q7', i: 'q9' },
  q8: { k: 'q11', l: 'q12' },
  q9: { k: 'q10' },
  q10: { m: 'q13', o: 'q14' },
  q11: { p: 'q3' },
  q12: { n: 'q11', r: 'q15' },
  q13: { s: 'q15', r: 'q15', o: 'q14', q: 'q14' },
  q14: { s: 'q4', q: 'q4' },
  q15: { t: 'q16' },
  q16: { u: 'q17' },
  q17: {}
};

export const allStates: ReadonlyArray<State> = [
  'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
  'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17'
];

export const alphabet: ReadonlyArray<InputSymbol> = [
  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
  'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', '1', '2'
];

export const fsaConfig: FSAConfig = {
  states: allStates,
  alphabet,
  initialState: 'q0',
  finalStates: ['q17'],
  transitions: transitionTable
};

// Helper function to get valid transitions for a state
export const getValidTransitionsForState = (state: State): Partial<Record<InputSymbol, State>> =>
  transitionTable[state] || {};

// Helper function to check if a symbol is valid
export const isValidSymbol = (symbol: string): symbol is InputSymbol =>
  alphabet.includes(symbol as InputSymbol);

// Helper function to check if a state is final
export const isFinalState = (state: State): boolean =>
  fsaConfig.finalStates.includes(state);

// Helper function to get next state
export const getNextState = (currentState: State, symbol: InputSymbol): State | null =>
  transitionTable[currentState]?.[symbol] ?? null;
