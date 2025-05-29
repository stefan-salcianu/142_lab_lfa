import room_gameDFA as current_autom
import random_input as ri

print(f"Random case? 1-yes, 0-no")
random_case=bool(int(input()))
if not random_case:
    DFA = current_autom.validate_input('room_autom.txt','room_input.txt')
    # autom.emulate(numbers,q0rules,q1rules,start,accept)
    current_autom.emulate(DFA)
else:
    DFA = current_autom.validate_input('room_autom.txt','')
    ri.generate(DFA)
    

