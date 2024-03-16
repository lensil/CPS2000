# Lexer Implementation

import enum

# Keywords
keywords = {"if", "else"}

# Operators
# Relation Operators
relational_ops = {"<", ">", "<=", ">=", "==", "!="}

# Multiplicative Operators
multiplicative_ops = {"*", "/", "and"}

# Additive Operators
additive_ops = {"+", "-", "or"}

# Punctuation
punctuation = {";", "(", ")", "{", "}"}

# Boolean Literals
bool_literals = {"true", "false"}

# Token Types
class Token_Type(enum.Enum):
    IDENTIFIER = 1
    KEYWORD = 2
    REL_OP = 3
    MULT_OP = 4
    ADD_OP = 5
    ASSIGNMENT_OP = 6
    PUNCTUATION = 7
    INT_LITERAL = 8
    FLOAT_LITERAL = 9
    BOOL_LITERAL = 10
    WHITESPACE = 11
    EOF = 12

# Token Class
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value
    
# Lexer Class
class Lexer:
    def __init__(self):
        self.lexeme_list = ["_", "letter", "digit", "ws", "<", ">", "!", ".", "punctuation", "rel_op", "*", "/", "+", "-", "other", "eq"]
        self.states_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.states_accp = [1, 2, 3, 4, 5, 7, 8, 9, 10]

        self.rows = len(self.states_list)
        self.cols = len(self.lexeme_list)

        self.Tx = [[-1 for j in range(self.cols)] for i in range(self.rows)]
        self.transition_table(); 
    
    def transition_table(self):
        # Integer Literals
        self.Tx[0][self.lexeme_list.index("digit")] = 1
        self.Tx[1][self.lexeme_list.index("digit")] = 1

        # Float Literals
        self.Tx[1][self.lexeme_list.index('.')] = 2
        self.Tx[2][self.lexeme_list.index("digit")] = 2

        # Identifiers
        self.Tx[0][self.lexeme_list.index("letter")] = 3
        self.Tx[3][self.lexeme_list.index("letter")] = 3
        self.Tx[3][self.lexeme_list.index("digit")] = 3
        self.Tx[3][self.lexeme_list.index("_")] = 3

        # Assignment Operator
        self.Tx[0][self.lexeme_list.index("eq")] = 4

        # Relation Operators
        self.Tx[0][self.lexeme_list.index(">")] = 5
        self.Tx[0][self.lexeme_list.index("<")] = 5
        self.Tx[0][self.lexeme_list.index("!")] = 6
        self.Tx[4][self.lexeme_list.index("eq")] = 7
        self.Tx[5][self.lexeme_list.index("eq")] = 7
        self.Tx[6][self.lexeme_list.index("eq")] = 7

        # Punctuation
        self.Tx[0][self.lexeme_list.index("punctuation")] = 8

        # Multiplicative Operators
        self.Tx[0][self.lexeme_list.index("*")] = 9
        self.Tx[0][self.lexeme_list.index("/")] = 9

        # Additive Operators
        self.Tx[0][self.lexeme_list.index("+")] = 10
        self.Tx[0][self.lexeme_list.index("-")] = 10
    
    def accepting_states(self, state):
        try:
            self.states_accp.index(state)
            return True
        except ValueError:
            return False

    def get_token_type_by_final_state(self, state, lexeme):
        match state:
            case 1:
                return Token(Token_Type.INT_LITERAL, lexeme)
            case 2:
                return Token(Token_Type.FLOAT_LITERAL, lexeme)
            case 3:
                if lexeme in keywords:
                    return Token(Token_Type.KEYWORD, lexeme)
                elif lexeme in bool_literals:
                    return Token(Token_Type.BOOL_LITERAL, lexeme)
                elif lexeme in relational_ops:
                    return Token(Token_Type.REL_OP, lexeme)
                elif lexeme in multiplicative_ops:
                    return Token(Token_Type.MULT_OP, lexeme)
                else:
                    return Token(Token_Type.IDENTIFIER, lexeme)
            case 4:
                return Token(Token_Type.ASSIGNMENT_OP, lexeme)
            case 5:
                return Token(Token_Type.REL_OP, lexeme)
            case 7:
                return Token(Token_Type.REL_OP, lexeme)
            case 8:
                return Token(Token_Type.PUNCTUATION, lexeme)
            case 9:
                return Token(Token_Type.MULT_OP, lexeme)
            case 10:
                return Token(Token_Type.ADD_OP, lexeme)
            case _:
                return None
            
    def categorize_character(self, character):
        match character:
            case char if char.isalpha():
                return "letter"
            case char if char.isdigit():
                return "digit"
            case "_":
                return "_"
            case " ":
                return "ws"
            case ";" | "(" | ")" | "{" | "}":
                return "punctuation"
            case "=":
                return "eq"
            case "<":
                return "<"
            case ">":
                return ">"
            case "!":
                return "!"
            case ".":
                return "."
            case "*":
                return "*"
            case "/":
                return "/"
            case "+":
                return "+"
            case "-":
                return "-"
            case _:
                return "other"
            
    def end_of_input(self, src_program_str, src_program_idx):
        if (src_program_idx > len(src_program_str)-1):
            return True
        else:
            return False

    def next_char(self, src_program_str, src_program_idx):
        if (not self.end_of_input(src_program_str, src_program_idx)):
            return True, src_program_str[src_program_idx]
        else: 
            return False, "."
        
    def next_token(self, src_program_str, src_program_idx):
        lexeme = ""
        state = 0
        stack = []
        stack.append(-2)

        while (state != -1):
            if self.accepting_states(state): 
                stack.clear()
            stack.append(state)

            exists, character = self.next_char(src_program_str, src_program_idx)
            lexeme += character
            if (not exists): 
                break
            src_program_idx = src_program_idx + 1

            cat = self.categorize_character(character)
            state = self.Tx[state][self.lexeme_list.index(cat)]

        lexeme = lexeme[:-1]

        syntax_error = False

        while (len(stack) > 0):
            if (stack[-1] == -2):
                syntax_error = True
                break

            if (not self.accepting_states(stack[-1])):
                stack.pop()
                lexeme = lexeme[:-1]
            else:
                state = stack.pop()
                break

        if syntax_error:
            return None
        
        if self.accepting_states(state):
            return self.get_token_type_by_final_state(state, lexeme), lexeme
        else:
            return None
        
    def generate_tokens(self, src_program_str):
        tokens_list = []
        src_program_idx = 0
        token, lexeme = self.next_token(src_program_str, src_program_idx)
        tokens_list.append(token)

        while (token != -1):
            src_program_idx = src_program_idx + len(lexeme)
            if (not self.end_of_input(src_program_str, src_program_idx)):
                token, lexeme = self.next_token(src_program_str, src_program_idx)
                tokens_list.append(token)
            else:
                break

        return tokens_list

# Test
lexer = Lexer()
tokens = lexer.generate_tokens("if(x>=y){23.678}")
for token in tokens:
    print(token.token_type, token.value)