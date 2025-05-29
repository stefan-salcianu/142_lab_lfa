LbForm&Autom — Automata Simulators in Python

This repository is a modular and interactive toolkit for simulating:

- **DFA (Deterministic Finite Automata)**
- **NFA (Nondeterministic Finite Automata with ε-transitions)**
- **Turing Machines**

It supports both predefined inputs and randomized tests. Perfect for exploring formal languages, automata theory, and computational models.

---
### Concepts Covered
-DFA transition tables and deterministic state progression

-NFA state branching and ε-closure logic

-Turing machine simulation with tape expansion

-File-based input/output interaction

-Randomized test case generation

## 📁 Project Structure
LbForm&Autom/
│
├── DFA_room/ # DFA simulation in a room-based game context
│ ├── emulator.py # Entry point: user chooses manual/random execution
│ ├── map.txt # Output log for DFA results
│ ├── random_input.py # Random input generator for DFA game
│ ├── room_autom.txt # Configuration file (states, transitions, etc.)
│ ├── room_gameDFA.py # Main DFA logic with input validation & simulation
│ └── room_input.txt # Manual input for testing DFA
│
├── DFA_simple/ # Minimal DFA setup
│ ├── autom.py # Basic DFA simulator with hardcoded logic
│ ├── autom.txt # DFA configuration
│ └── input.txt # DFA input
│
├── Graph/ # (Optional/Unlinked) 
│ ├── graph.in # Input file (usage unclear)
│ ├── graph.out # Output file
│ └── graph.py # Graph-related processing 
│
├── NFA/ # Nondeterministic Finite Automaton with ε-transitions
│ ├── automNFA.py # Parser and emulator for NFA
│ ├── automNFA.txt # NFA configuration
│ ├── emulator_NFA.py # Entry point for running the NFA
│ ├── inputNFA.txt # Input string for NFA
│ └── NFA_rez.txt # NFA simulation results
│
├── Turing/ # Turing Machine simulator
│ ├── autom_turing.py # Turing machine parser & emulator
│ ├── emulator_turing.py# Entry point for running the Turing Machine
│ └── turing_rules.txt # Turing machine rules, states, transitions
│
└── .idea/, pycache/ # IDE and build artifacts (can be ignored)

---

##How to Run

### 1. DFA Room Game

bash
cd DFA_room
python emulator.py

Choose:

1 = Random test run

0 = Manual input from room_input.txt

Results are saved in map.txt.

### 2.NFA 
bash
cd NFA
python emulator_NFA.py

### 3.Turing Machine
bash
cd Turing
python emulator_turing.py

### 4.Simple DFA

bash
cd DFA_simple
python autom.py

# Requirements
Python 3.7 or newer

No external libraries needed

# Author
Ștefan-Alexandru Sălcianu
Student @ University of Bucharest
