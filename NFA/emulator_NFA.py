import automNFA as current_NFA



NFA = current_NFA.validate_input('automNFA.txt','inputNFA.txt')
current_NFA.emulate(NFA)