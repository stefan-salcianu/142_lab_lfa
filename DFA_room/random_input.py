import random
import room_gameDFA as rgD 
# Function to generate and simulate random input strings for a DFA
def generate(DFA):
    # Unpack DFA components
    qrules, alphabet_converted, nodes, rules, start, accept = DFA

    # Build transition table from rules: fill qrules[state][symbol_index] = next_state
    for rule in rules:
        rule = rule.strip().split("-")
        if len(rule) > 3:
            raise ValueError("Invalid input! Rule must have 3 elements.")
        qrules[rule[0]][alphabet_converted[rule[1]]] = rule[2]

    cnt = iterations = 1000  # Total number of simulations to run

    # Run 1000 randomized simulations
    while iterations > 0:
        input = []  # This will hold the generated random input string
        alphabet = list(alphabet_converted.keys())  # Original symbols (e.g., ['0', '1', 'a', 'b'])

        pathcnt = random.randint(8, 15)  # Length of the random input (between 8 and 15 symbols)
        while pathcnt > 0:
            choice = random.choice(alphabet)  # Random symbol from the alphabet
            input.append(choice)
            pathcnt -= 1

        # Run the DFA emulator with the randomly generated input
        rgD.emulate((input, qrules, alphabet_converted, nodes, rules, start, accept))

        iterations -= 1

    # Write final statistics to a file: total games played and how many were accepted
    print(f"Games played:{cnt}\n Games won:{rgD.cnt}", file=open("map.txt", "a"))
