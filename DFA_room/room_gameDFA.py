# Custom exception for empty input string
class EmptyStringError(Exception):
    pass

# Custom exception for missing start state in configuration
class NoStartError(Exception):
    pass

# Custom exception for missing accept state in configuration
class NoEndError(Exception):
    pass


# Function to validate input and parse DFA configuration and input
def validate_input(file, inputFile=''):
    fin = open(f"{file}", "r")
    lines = fin.readlines()

    ct = 0  # Keeps track of which config line we're processing
    alphabet = []              # List of valid input symbols
    alphabet_converted = {}    # Maps each symbol to its index (e.g., {'up': 0, 'right': 1, ...})
    nodes = []                 # List of states/nodes in the DFA
    rules = []                 # List of transition rules in raw format
    start = ''                 # Start state
    accept = ''                # Accept (goal) state

    # Parse the configuration lines
    for line in lines:
        line = line.strip().split(":")
        if ct == 0:
            # Line 0: Alphabet (comma-separated)
            alphabet = line[1].strip().split(',')
            for i in range(len(alphabet)):
                alphabet_converted[alphabet[i]] = i
        elif ct == 1:
            # Line 1: States (comma-separated)
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
            # Line 4: Accept (goal) state
            if not line[1]:
                raise NoEndError("No end node specified.")
            if line[1].strip() not in nodes:
                raise ValueError("Invalid input! Accept node must be in the list of nodes.")
            accept = line[1].strip()
        ct += 1

    # Initialize transition table: qrules[state] = list of transitions indexed by symbol index
    qrules = {}
    for i in range(len(nodes)):
        qrules[nodes[i]] = [0] * len(alphabet)

    # If no input file provided, return DFA structure for random generation
    if inputFile == '':
        return (qrules, alphabet_converted, nodes, rules, start, accept)

    # Read the DFA input string (comma-separated)
    fin1 = open(f"{inputFile}", "r")
    line = fin1.readline()
    line = line.strip().split(":")
    line = line[1].strip().split(',')
    dfa_input = line

    # Validate input is not empty
    if not line:
        raise EmptyStringError("Empty input not allowed.")

    # Validate all symbols in input belong to the defined alphabet
    if not all(el in alphabet for el in line):
        raise ValueError("Invalid input! Input must be in the alphabet.")

    # Convert transition rules into the structured transition table (qrules)
    for rule in rules:
        rule = rule.strip().split("-")
        if len(rule) > 3:
            raise ValueError("Invalid input! Rule must have 3 elements.")
        qrules[rule[0]][alphabet_converted[rule[1]]] = rule[2]

    # Optional debug prints for confirmation
    print(alphabet_converted)
    print(dfa_input)

    fin.close()
    fin1.close()

    # 1 = up, 2 = right, 3 = down, 4 = left (used in directional alphabets, like game movement)
    return (dfa_input, qrules, alphabet_converted, nodes, rules, start, accept)


# Global win counter (number of accepted runs)
cnt = 0

# Function to emulate DFA execution for a single input sequence
def emulate(DFA):
    global cnt
    fin2 = open("map.txt", "a")  # Append results to map.txt (e.g., for logging game outcomes)

    # Unpack DFA components
    dfa_input, qrules, alphabet_converted, nodes, rules, start, accept = DFA

    current_node = start  # Start from the initial node

    # Simulate DFA transitions for each input symbol
    for el in dfa_input:
        # If there’s no transition defined, stay in the same state
        if qrules[current_node][alphabet_converted[el]] == 0:
            print("Player Stays!", file=fin2)
        else:
            # Transition to the next state
            current_node = qrules[current_node][alphabet_converted[el]]
            print(f"Player Moves to {current_node}", file=fin2)

    # Check if the final state is the accept state
    if current_node == accept:
        cnt += 1
        print("Player Wins!", file=fin2)
    else:
        print("Player Loses!", file=fin2)

    fin2.close()
