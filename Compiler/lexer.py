#Class to wrap the different tokens we'll be using
from enum import Enum

# Set of token types
class TokenType(Enum):
    rel_op = 1 
    identifier = 2
    equals = 3
    punctuation = 4

# Token class
# Represents a token with a type and a lexeme
class Token:
    def __init__(self, t, l):
        self.type = t
        self.lexeme = l        

#Lexer class wrapper for code above
class Lexer:
    def __init__(self):
        self.lexeme_list = ["<", "=", "!", ">", "_", "letter", "digit", "punctuation"]
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
        # > | <
        self.Tx[0][self.lexeme_list.index(">")] = 1
        self.Tx[0][self.lexeme_list.index("<")] = 1

        # Less than/greater than or equal to
        # >= | <=
        self.Tx[1][self.lexeme_list.index("=")] = 3
        
        # Not equal to/equal to
        # != | ==
        self.Tx[0][self.lexeme_list.index("!")] = 2
        self.Tx[2][self.lexeme_list.index("=")] = 3
        self.Tx[4][self.lexeme_list.index("=")] = 3

        # Equals 
        # =
        self.Tx[0][self.lexeme_list.index("=")] = 4

        # Variable names
        # _ | letter | digit
        self.Tx[0][self.lexeme_list.index("letter")] = 5
        self.Tx[5][self.lexeme_list.index("letter")] = 5
        self.Tx[5][self.lexeme_list.index("digit")] = 5
        self.Tx[5][self.lexeme_list.index("_")] = 5


        # Punctuation
        # : ; , ( ) { } [ ]
        self.Tx[0][self.lexeme_list.index("punctuation")] = 6

        for row in self.Tx:
            print(row)

    # Check if the state is an accepting state
    def AcceptingStates(self, state):
        try:
            self.states_accp.index(state)
            return True;
        except ValueError:
            return False;

    # Returns the token type depending on the final state
    def GetTokenTypeByFinalState(self, state, lexeme):
        if state == 1:
            return Token(TokenType.rel_op, lexeme)
        elif state == 3:
            return Token(TokenType.rel_op, lexeme)
        elif state == 4:
            return Token(TokenType.equals, lexeme)
        elif state == 5:
            return Token(TokenType.identifier, lexeme)
        elif state == 6:
            return Token(TokenType.punctuation, lexeme)
        else:
            return 'default result'

    # Returns the category of a character 
    def CatChar(self, character):
        if character.isalpha():
            return "letter"
        if character.isdigit():
            return "digit"
        if character == "_":
            return "_"
        if character in [":", ";", ",", "(", ")", "{", "}", "[", "]"]:
            return "punctuation"
        if character in ["<", ">", "=", "!"]:
            return character
        return "other"
    
    # Check if the input has ended
    def EndOfInput(self, src_program_str, src_program_idx):
        if (src_program_idx > len(src_program_str)-1):
            return True;
        else:
            return False;

    # Get the next character
    def NextChar(self, src_program_str, src_program_idx):
        if (not self.EndOfInput(src_program_str, src_program_idx)):
            return True, src_program_str[src_program_idx]
        else: 
            return False, "."
        
    # Main function to get the next token
    def GetNextToken(self, src_program_str, src_program_idx):
        state = 0
        stack = []
        lexeme = ""
        stack.append(-2)

        while (state != -1):
            if self.AcceptingStates(state): 
                stack.clear();
            stack.append(state);

            exists, character = self.NextChar(src_program_str, src_program_idx)
            lexeme += character
            if (not exists):
                break
            src_program_idx += 1

            cat = self.CatChar(character)
            state = self.Tx[state][self.lexeme_list.index(cat)]

        lexeme = lexeme[:-1]

        syntax_error = False
        while (len(stack) > 0):
            if (stack[-1] == -2):
                syntax_error = True
                break
        
            if(not self.AcceptingStates(stack[-1])):
                stack.pop()
                print("Popped")
                lexeme = lexeme[:-1]

            else:
                state = stack.pop()
                break

        if syntax_error:
            return 'Syntax error'
        
        if self.AcceptingStates(state):
            return self.GetTokenTypeByFinalState(state, lexeme), lexeme
        
        else:
            return 'Syntax error'
        
    def generate_token(self, src_program_str):
        print("INPUT:: " + src_program_str)
        tokens_list = []
        src_program_idx = 0
        token, lexeme = self.GetNextToken(src_program_str, src_program_idx)
        tokens_list.append(token)

        while (token != -1):
            src_program_idx = src_program_idx + len(lexeme)
            if (not self.EndOfInput(src_program_str, src_program_idx)):
                token, lexeme = self.GetNextToken(src_program_str, src_program_idx)
                tokens_list.append(token)
            else: 
                break
        return tokens_list
    
lex = Lexer()
toks = lex.generate_token("<=>=!=a_abc123:;")

for t in toks:
    print(t.lexeme, t.type)
