#Class to wrap the different tokens we'll be using
from enum import Enum

class TokenType(Enum):
    rel_op = 1
    identifier = 2
    equals = 3
    punctuation = 4


class Token:
    def __init__(self, t, l):
        self.type = t
        self.lexeme = l        

#Lexer class wrapper for code above
class Lexer:
    def __init__(self):
        self.lexeme_list = ["<", "=", "!", ">", "_", "letter", "digit", ":", ";", ",", "(", ")", "{", "}",
                            "[", "]"]
        self.states_list = [0, 1, 2, 3, 4, 5, 6]
        self.states_accp = [1, 3, 4, 5, 6]

        self.rows = len(self.states_list)
        self.cols = len(self.lexeme_list)

        # Let's take integer -1 to represent the error state for this DFA
        self.Tx = [[-1 for j in range(self.cols)] for i in range(self.rows)]
        self.InitialiseTxTable();     

    def InitialiseTxTable(self):
        # Update Tx to represent the state transition function of the DFA
        
        # Greater than/less than 
        self.Tx[0][self.lexeme_list.index(">")] = 1
        self.Tx[0][self.lexeme_list.index("<")] = 1

        # Less than/greater than or equal to
        self.Tx[1][self.lexeme_list.index("=")] = 3
        
        # Not equal to/equal to
        self.Tx[0][self.lexeme_list.index("!")] = 2
        self.Tx[2][self.lexeme_list.index("=")] = 3
        self.Tx[4][self.lexeme_list.index("=")] = 3

        # Equals 
        self.Tx[0][self.lexeme_list.index("=")] = 4

        # Variable names
        self.Tx[0][self.lexeme_list.index("letter")] = 5
        self.Tx[5][self.lexeme_list.index("letter")] = 5
        self.Tx[5][self.lexeme_list.index("digit")] = 5
        self.Tx[5][self.lexeme_list.index("_")] = 5


        # Punctuation
        self.Tx[0][self.lexeme_list.index(":")] = 6
        self.Tx[0][self.lexeme_list.index(";")] = 6
        self.Tx[0][self.lexeme_list.index(",")] = 6
        self.Tx[0][self.lexeme_list.index("(")] = 6
        self.Tx[0][self.lexeme_list.index(")")] = 6
        self.Tx[0][self.lexeme_list.index("{")] = 6
        self.Tx[0][self.lexeme_list.index("}")] = 6
        self.Tx[0][self.lexeme_list.index("[")] = 6
        self.Tx[0][self.lexeme_list.index("]")] = 6
        

        for row in self.Tx:
            print(row)

    def AcceptingStates(self, state):
        try:
            self.states_accp.index(state)
            return True;
        except ValueError:
            return False;
