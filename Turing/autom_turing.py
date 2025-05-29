# Function to load a Turing Machine configuration from a file
def load_turing_config(file_path):
    # Open the config file and read all non-empty, non-comment lines
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    # Initialize the configuration dictionary
    config = {
        "alphabet": [],         # List of symbols the machine can read/write
        "states": [],           # List of all possible states
        "transitions": {},      # Dictionary of transitions: (state, symbol) -> (new_state, new_symbol, direction)
        "tape": [],             # Initial tape contents
        "start": "",            # Start state
        "accept": "",           # Accept state
        "blank": "_"            # Symbol used for blank tape cells
    }

    mode = None  # Used to start parsing transitions when the line 'transitions:' is reached

    # Parse each line from the file and populate the config dictionary
    for line in lines:
        if line.startswith("alphabet:"):
            config["alphabet"] = line.split(":")[1].replace(" ", "").split(",")
        elif line.startswith("blank:"):
            config["blank"] = line.split(":")[1].strip()
        elif line.startswith("states:"):
            config["states"] = line.split(":")[1].replace(" ", "").split(",")
        elif line.startswith("start:"):
            config["start"] = line.split(":")[1].strip()
        elif line.startswith("accept:"):
            config["accept"] = line.split(":")[1].strip()
        elif line.startswith("tape:"):
            # Tape symbols are separated by spaces; commas are stripped out for safety
            config["tape"] = line.split(":")[1].strip().replace(",", "").split()
        elif line.startswith("transitions:"):
            # Switch parsing mode to transitions
            mode = "transitions"
        elif mode == "transitions":
            # Parse a transition rule: (current_state, read_symbol) -> (next_state, write_symbol, direction)
            left, right = line.split("->")
            current_state, read_symbol = [x.strip() for x in left.split(",")]
            next_state, write_symbol, direction = [x.strip() for x in right.split(",")]
            config["transitions"][(current_state, read_symbol)] = (next_state, write_symbol, direction)

    return config


# Function to emulate the Turing Machine based on the given configuration
def emulate(config):
    current_state = config['start']             # Start in the initial state
    tape = config['tape']                       # Work with the given tape
    transitions = config['transitions']         # Load transition table
    blank = config['blank']                     # Blank symbol (usually "_")
    current_index = 0                           # Tape head starts at the beginning of the tape

    # Continue executing transitions until the accept state is reached
    while current_state != config['accept']:
        # Extend tape leftward if head goes off the beginning
        if current_index < 0:
            tape.insert(0, blank)
            current_index = 0
        # Extend tape rightward if head moves beyond the current tape
        elif current_index >= len(tape):
            tape.append(blank)

        read_symbol = tape[current_index]  # Read the current symbol under the head

        key = (current_state, read_symbol)  # Form the transition key

        # If no valid transition exists for this (state, symbol), halt with error
        if key not in transitions:
            print(f"No transition found for state {current_state} and symbol {read_symbol}.")
            break

        # Apply the transition: update state, write new symbol, move head
        next_state, write_symbol, direction = transitions[key]

        tape[current_index] = write_symbol  # Write symbol to tape
        current_state = next_state          # Move to next state

        # Move the tape head in the correct direction
        if direction == "R":
            current_index += 1
        elif direction == "L":
            current_index -= 1
        else:
            raise ValueError(f"Invalid direction: {direction}")

    # Final output after machine halts (accept state reached or no valid transition)
    print("Final tape:", tape)
    print("Final state:", current_state)
