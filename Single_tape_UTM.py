#Run script
class TuringMachine:
    def __init__(self, states, tape, start_state, transitions, blank_symbol='_'):
        self.states = states
        self.tape = list(tape) + [blank_symbol] * 100  # Extend the tape
        self.head = 0
        self.current_state = start_state
        self.transitions = transitions
        self.blank_symbol = blank_symbol

    def step(self):
        """Perform a single step based on the current state and tape symbol."""
        symbol = self.tape[self.head]
        key = (self.current_state, symbol)

        if key not in self.transitions:
            return False  # Halt if no transition is found

        new_state, write_symbol, direction = self.transitions[key]
        self.tape[self.head] = write_symbol
        self.current_state = new_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        if self.head < 0:
            self.tape.insert(0, self.blank_symbol)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank_symbol)

        return True

    def run(self):
        """Run the Turing Machine until it halts."""
        while self.step():
            print(f"State: {self.current_state}, Head: {self.head}, Tape: {''.join(self.tape).strip(self.blank_symbol)}")
        print(f"Final Tape: {''.join(self.tape).strip(self.blank_symbol)}")


class UniversalTuringMachine:
    def __init__(self):
        self.machines = []

    def add_machine(self, states, tape, start_state, transitions):
        """Add a Turing Machine to the universal machine."""
        tm = TuringMachine(states, tape, start_state, transitions)
        self.machines.append(tm)

    def run_all(self):
        """Run all added Turing Machines sequentially."""
        for i, tm in enumerate(self.machines, start=1):
            print(f"\nRunning Turing Machine {i}:")
            tm.run()


# Define TM1: Binary increment
states1 = {'q0', 'q1', 'qhalt'}
tape1 = "1010"
start_state1 = 'q0'
transitions1 = {
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', '_'): ('q1', '1', 'L'),
    ('q1', '1'): ('q1', '1', 'L'),
    ('q1', '0'): ('q1', '0', 'L'),
    ('q1', '_'): ('qhalt', '_', 'R'),
}

# Define TM2: Reverse binary string
states2 = {'q0', 'q1', 'q2', 'qhalt'}
tape2 = "1101"
start_state2 = 'q0'
transitions2 = {
    ('q0', '1'): ('q1', '_', 'R'),
    ('q0', '0'): ('q2', '_', 'R'),
    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '_'): ('qhalt', '1', 'L'),
    ('q2', '1'): ('q2', '1', 'R'),
    ('q2', '0'): ('q2', '0', 'R'),
    ('q2', '_'): ('qhalt', '0', 'L'),
}

# Define TM3: Check even number of 1s
states3 = {'q0', 'q1', 'qhalt'}
tape3 = "1101"
start_state3 = 'q0'
transitions3 = {
    ('q0', '1'): ('q1', '_', 'R'),
    ('q0', '0'): ('q0', '0', 'R'),
    ('q0', '_'): ('qhalt', 'E', 'R'),
    ('q1', '1'): ('q0', '_', 'R'),
    ('q1', '0'): ('q1', '0', 'R'),
    ('q1', '_'): ('qhalt', 'O', 'R'),
}

# Create Universal TM and add machines
utm = UniversalTuringMachine()
utm.add_machine(states1, tape1, start_state1, transitions1)
utm.add_machine(states2, tape2, start_state2, transitions2)
utm.add_machine(states3, tape3, start_state3, transitions3)

# Run all machines
utm.run_all()
