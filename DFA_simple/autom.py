# Custom exception raised when the input string is empty
class EmptyStringError(Exception):
    pass

# Custom exception raised when no start state is defined in the automaton file
class NoStartError(Exception):
    pass

# Custom exception raised when no accept state is defined in the automaton file
class NoEndError(Exception):
    pass

def validate_input(file, inputFile):
    # Open automaton description and input files
    fin = open(f"{file}", "r")
    fin1 = open(f"{inputFile}", "r")

    lines = fin.readlines()
    ct = 0  # Counter to track which section of the config we're parsing

    numbers = []      # Input number sequence
    alphabet = []     # Allowed symbols (e.g., [0, 1])
    nodes = []        # States (e.g., q0, q1)
    rules = []        # Transitions (e.g., q0-0-q1)
    q0rules = [0, 0]  # Transition rules when in state q0, indexed by input symbol
    q1rules = [0, 0]  # Transition rules when in state q1, indexed by input symbol
    start = ''        # Start state
    accept = ''       # Accept (final) state

    # Parse automaton configuration
    for line in lines:
        line = line.strip().split(":")
        if ct == 0:
            # Line 0: Defines the input alphabet (e.g., 0 1)
            alphabet = [int(j) for j in line[1].strip().split()]
        elif ct == 1:
            # Line 1: Defines the states (e.g., q0,q1)
            nodes = line[1].strip().split(",")
        elif ct == 2:
            # Line 2: Defines transition rules
            rules = line[1].strip().split(",")
        elif ct == 3:
            # Line 3: Defines the start state
            if not line[1]:
                raise NoStartError("No start node specified.")
            if line[1].strip() not in nodes:
                raise ValueError("Invalid input! Start node must be in the list of nodes.")
            start = line[1].strip()
        else:
            # Line 4: Defines the accept (final) state
            if not line[1]:
                raise NoEndError("No end node specified.")
            if line[1].strip() not in nodes:
                raise ValueError("Invalid input! Accept node must be in the list of nodes.")
            accept = line[1].strip()
        ct += 1

    # Parse the input string from the second file
    line = fin1.readline()
    line = line.strip().split(":")

    # Validate that only 0s and 1s are present
    if not all(char in "01 " for char in line[1].strip()):
        raise ValueError("Invalid input! Only 0s and 1s are allowed.")

    tokens = line[1].split()

    # Ensure all symbols are either '0' or '1', separated by space
    if not all(token in {"0", "1"} for token in tokens):
        raise ValueError("Invalid input! Numbers must be separated by spaces.")

    # Convert valid tokens to integers
    numbers = [int(j) for j in tokens]

    fin.close()
    fin1.close()

    # Parse transition rules and populate q0rules/q1rules accordingly
    for rule in rules:
        rule = rule.strip().split("-")
        if len(rule) != 3:
            raise ValueError("Invalid input! Each rule must have exactly 3 elements.")
        if int(rule[1]) not in alphabet:
            raise ValueError("Invalid input! Only 0s and 1s are allowed.")

        # Store transitions separately for q0 and q1
        if rule[0] == 'q0':
            q0rules[int(rule[1])] = rule[2]
        else:
            q1rules[int(rule[1])] = rule[2]

    return numbers, q0rules, q1rules, start, accept


def emulate(numbers, q0rules, q1rules, start, accept):
    # Simulates the DFA operation on the input string
    print(q0rules)  # Debug: show transitions from q0
    print(q1rules)  # Debug: show transitions from q1

    current_state = start
    print(current_state)  # Initial state

    for el in numbers:
        # Apply the transition based on current state and input symbol
        if current_state == 'q0':
            current_state = q0rules[el]
        else:
            current_state = q1rules[el]
        print(current_state)  # Debug: show state after each input

    if not numbers:
        raise EmptyStringError("Empty string")

    # Final decision: is the current state the accept state?
    if current_state == accept:
        print(f"Sirul se termina cu 1")  # Accepted
    else:
        print(f"Sirul se termina cu 0, not accepted")  # Rejected
