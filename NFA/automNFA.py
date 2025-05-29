# Custom exceptions to handle validation and parsing issues
class EmptyStringError(Exception):
    pass

class NoStartError(Exception):
    pass

class NoEndError(Exception):
    pass

# This NFA accepts all strings that contain at least two 'a's or two 'b's
def validate_input(file, inputFile=''):
    fin = open(f"{file}", "r")
    lines = fin.readlines()

    ct = 0
    alphabet = []                  # List of input symbols (e.g., ['a', 'b'])
    alphabet_converted = {}       # Map each symbol to a unique index
    nodes = []                    # States of the NFA
    rules = []                    # Transition rules as strings (e.g., q0-a-q1)
    start = ''                    # Start state
    accept = ''                   # Accept/final state

    # Parse configuration lines
    for line in lines:
        line = line.strip().split(":")
        if ct == 0:
            # Line 0: Alphabet symbols
            alphabet = line[1].strip().split(',')
            for i in range(len(alphabet)):
                alphabet_converted[alphabet[i]] = i
        elif ct == 1:
            # Line 1: States/nodes
            nodes = line[1].strip().split(",")
        elif ct == 2:
            # Line 2: Transition rules
            rules = line[1].strip().split(",")
        elif ct == 3:
            # Line 3: Start state
            if not line[1]:
                raise NoStartError("No start node specified.")
            if line[1].strip() not in nodes:
                raise ValueError("Invalid input! Start node must be in the list of nodes.")
            start = line[1].strip()
        else:
            # Line 4: Accept state
            if not line[1]:
                raise NoEndError("No end node specified.")
            if line[1].strip() not in nodes:
                raise ValueError("Invalid input! Accept node must be in the list of nodes.")
            accept = line[1].strip()
        ct += 1

    # Initialize transition table for each state
    qrules = {state: {} for state in nodes}

    # Read input string from second file
    fin1 = open(f"{inputFile}", "r")
    line = fin1.readline()
    line = line.strip().split(":")
    line = line[1].strip().split(',')  # Input string split into symbols
    nfa_input = line

    # Validate the input string
    if not line:
        raise EmptyStringError("Empty input not allowed.")
    for el in line:
        if el not in alphabet:
            raise ValueError("Invalid input! String must be in the alphabet.")

    # Rebuild transition rules into structured form: qrules[state][symbol] = set of next states
    for rule in rules:
        parts = rule.strip().split("-")
        if len(parts) != 3:
            raise ValueError("Invalid input! Rule must have 3 elements.")
        src, symbol, dst = parts

        # Normalize epsilon symbols to 'ε'
        if symbol in ['ε', 'Îε', 'Îµ']:
            symbol = 'ε'

        if symbol not in qrules[src]:
            qrules[src][symbol] = set()
        qrules[src][symbol].add(dst)

    print(qrules)  # Debug print: transition table structure

    fin.close()
    fin1.close()
    return (nfa_input, qrules, alphabet_converted, nodes, rules, start, accept)


# Global counter for number of accepted inputs
cnt = 0

# Compute the epsilon closure of a set of states
def epsilon_closure(qrules, states):
    """Returns the epsilon closure of a set of states."""
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for next_state in qrules.get(state, {}).get('ε', set()):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure


# Function to simulate an NFA with ε-transitions
def emulate(NFA):
    global cnt
    fin2 = open("NFA_rez.txt", "w", encoding="utf-8")  # Output log file

    # Unpack the parsed NFA
    nfa_input, qrules, alphabet_converted, nodes, rules, start, accept = NFA

    # Start from the ε-closure of the start state
    current_states = epsilon_closure(qrules, {start})
    print(f"Initial states (after ε-closure): {current_states}", file=fin2)

    # Process each symbol in the input string
    for symbol in nfa_input:
        next_states = set()
        for state in current_states:
            if symbol in qrules.get(state, {}):
                next_states = next_states.union(qrules[state][symbol])
        # Apply ε-closure again after transition
        current_states = epsilon_closure(qrules, next_states)
        print(f"After input '{symbol}': {current_states}", file=fin2)

    # If final states include the accept state, accept input
    if accept in current_states:
        cnt += 1
        print("Accepted", file=fin2)
    else:
        print("Rejected", file=fin2)

    fin2.close()
