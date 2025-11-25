// FSA Type Definitions

export type State =
  | 'q0' | 'q1' | 'q2' | 'q3' | 'q4' | 'q5' | 'q6' | 'q7' | 'q8' | 'q9'
  | 'q10' | 'q11' | 'q12' | 'q13' | 'q14' | 'q15' | 'q16' | 'q17';

export type InputSymbol =
  | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l'
  | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | '1' | '2';

export type TransitionTable = Record<State, Partial<Record<InputSymbol, State>>>;

export interface FSAConfig {
  readonly states: ReadonlyArray<State>;
  readonly alphabet: ReadonlyArray<InputSymbol>;
  readonly initialState: State;
  readonly finalStates: ReadonlyArray<State>;
  readonly transitions: TransitionTable;
}

export interface TransitionResult {
  readonly currentState: State;
  readonly inputSymbol: InputSymbol;
  readonly nextState: State | null;
  readonly isValid: boolean;
}

export interface ProcessResult {
  readonly inputString: string;
  readonly accepted: boolean;
  readonly finalState: State;
  readonly path: ReadonlyArray<State>;
  readonly transitions: ReadonlyArray<TransitionResult>;
}

export const STATE_DESCRIPTIONS: Record<State, string> = {
  q0: 'Initial State',
  q1: 'Select Product',
  q2: 'Select Payment Method',
  q3: 'Non-Cash Payment',
  q4: 'Cash Payment',
  q5: 'Calculate Balance (Non-Cash)',
  q6: 'Input Cash 5000',
  q7: 'Input Cash 10000',
  q8: 'Check Balance (Non-Cash)',
  q9: 'Calculate Balance (Cash)',
  q10: 'Check Balance (Cash)',
  q11: 'Return Money (Non-Cash)',
  q12: 'Dispense Product (Non-Cash)',
  q13: 'Dispense Product (Cash)',
  q14: 'Return Money (Cash)',
  q15: 'Calculate Change',
  q16: 'Dispense Change',
  q17: 'Transaction Complete'
};

export const SYMBOL_DESCRIPTIONS: Record<InputSymbol, string> = {
  a: 'Start',
  b: 'Select Product',
  c: 'Select Payment Method',
  d: 'Non-Cash',
  e: 'Cash Input 5000',
  f: 'Cash Input 10000',
  g: 'Calculate Balance',
  h: 'Scan QR',
  i: 'Add Cash 10000',
  j: 'Balance Check',
  k: 'Insufficient Balance',
  l: 'Sufficient Balance',
  m: 'Return to Selection',
  n: 'Dispense Product',
  o: 'Insufficient Balance (Cash)',
  p: 'Return Money',
  q: 'Dispense Product (Cash)',
  r: 'Calculate Change',
  s: 'No Change',
  t: 'Change Available',
  u: 'Dispense Change',
  '1': 'Add Cash 5000',
  '2': 'Add Cash 10000'
};
