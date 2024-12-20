class ThreeTapeTuringMachine:
    def __init__(self, encoded_tm, input_string):
        # Validate encoded TM format
        self.validate_encoded_tm(encoded_tm)

        # Tape 1: Encoded TM
        self.tape1 = list(encoded_tm) + ['_'] * 100  # Extend with blanks
        self.head1 = 0

        # Tape 2: Input string (simulated TM's tape)
        self.tape2 = list(input_string) + ['_'] * 100
        self.head2 = 0

        # Tape 3: Working tape for intermediate computations
        self.tape3 = ['_'] * 200
        self.head3 = 0

        self.current_state = 'q0'  # Start state of the simulated TM

    def validate_encoded_tm(self, encoded_tm):
        """Check if the encoded TM string is well-formed."""
        if not encoded_tm.strip():
            raise ValueError("Encoded TM is empty.")
        if '(' not in encoded_tm or ')' not in encoded_tm:
            raise ValueError("Encoded TM must contain transitions enclosed in parentheses.")
        if encoded_tm.count('(') != encoded_tm.count(')'):
            raise ValueError("Mismatched parentheses in encoded TM.")

    def decode_transition(self):
        """Decode the next transition from tape 1."""
        while self.head1 < len(self.tape1) and self.tape1[self.head1] != '(':
            self.head1 += 1

        if self.head1 >= len(self.tape1):  # End of tape reached without finding '('
            raise ValueError("Malformed encoded TM: Missing '(' for transition start.")

        self.head1 += 1  # Skip '('
        transition = ""
        while self.head1 < len(self.tape1) and self.tape1[self.head1] != ')':
            transition += self.tape1[self.head1]
            self.head1 += 1

        if self.head1 >= len(self.tape1):  # End of tape reached without finding ')'
            raise ValueError("Malformed encoded TM: Missing ')' for transition end.")

        self.head1 += 1  # Skip ')'
        return transition.split(',')

    def step(self):
        """Simulate one step of the Universal Turing Machine."""
        # Read current state and symbol under Tape 2's head
        symbol = self.tape2[self.head2]

        # Search for a matching transition on Tape 1
        self.head1 = 0
        while True:
            try:
                transition = self.decode_transition()
            except ValueError:
                break  # No more transitions to check

            current_state, read_symbol, new_state, write_symbol, direction = transition

            if current_state == self.current_state and read_symbol == symbol:
                # Match found; apply the transition
                self.current_state = new_state
                self.tape2[self.head2] = write_symbol

                if direction == 'R':
                    self.head2 += 1
                elif direction == 'L':
                    self.head2 -= 1

                # Expand the tape if needed
                if self.head2 >= len(self.tape2):
                    self.tape2.append('_')
                elif self.head2 < 0:
                    self.tape2.insert(0, '_')
                    self.head2 = 0

                return True  # Successfully executed a transition

        # Halting condition: No matching transition
        print(f"Halting: No transition for state {self.current_state} and symbol {symbol}")
        return False

    def run(self):
        """Run the Turing Machine until it halts."""
        while self.step():
            print(f"State: {self.current_state}, Head2: {self.head2}, Tape2: {''.join(self.tape2).strip('_')}")

# Example encoded TM: Adds 1 to a binary number
encoded_tm = "(q0,1,q0,1,R)(q0,0,q0,0,R)(q0,_,q1,1,L)(q1,1,q1,1,L)(q1,_,qhalt,_,R)"

# Input binary number
input_string = "10100"

three_tape_tm = ThreeTapeTuringMachine(encoded_tm, input_string)
three_tape_tm.run()
