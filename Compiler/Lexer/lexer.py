# Lexer Implementation

import enum
from dfa import DFA, input_categories
from tokens import Token, token_type_by_final_state, TokenType

# Lexer Class
class Lexer:
    def __init__(self):
        self.dfa = DFA()
        self.line_number = 1
            
    def end_of_input(self, src_program_str, src_program_idx):
        if (src_program_idx > len(src_program_str)-1):
            return True
        else:
            return False

    def next_char(self, src_program_str, src_program_idx):
        if (not self.end_of_input(src_program_str, src_program_idx)):
            if src_program_str[src_program_idx] == '\n':
                self.line_number += 1
            return True, src_program_str[src_program_idx]
        else: 
            return False, "."
        
    def next_token(self, src_program_str, src_program_idx):
        lexeme = ""
        state = self.dfa.start_state
        stack = []
        stack.append(-2)

        while (state != None):
            if self.dfa.accepting_states(state): 
                stack.clear()
            stack.append(state)

            exists, character = self.next_char(src_program_str, src_program_idx)
            lexeme += character
            if (not exists): 
                break
            src_program_idx = src_program_idx + 1

            cat = input_categories(character)
            state = self.dfa.transitions.get((state, cat), None)
            if (state == None):
                if character == "\n":
                    self.line_number -= 1

        lexeme = lexeme[:-1]

        syntax_error = False

        while (len(stack) > 0):
            if (stack[-1] == -2):
                syntax_error = True
                break

            if (not self.dfa.accepting_states(stack[-1])):
                stack.pop()
                lexeme = lexeme[:-1]
            else:
                state = stack.pop()
                break

        if syntax_error:
            raise Exception("Invalid lexeme: " + lexeme + " at line " + str(self.line_number))
        if self.dfa.accepting_states(state):
            return token_type_by_final_state(state.value, lexeme, self.line_number) # To do: Update lexer to keep track of line and column numbers
        else:
            raise Exception("Invalid lexeme: " + lexeme + " at line " + str(self.line_number))
        
    def generate_tokens(self, src_program_str):
        tokens_list = []
        src_program_idx = 0
        token = self.next_token(src_program_str, src_program_idx)

        while (token.TokenType != TokenType.EOF):
            if token.TokenType != TokenType.SKIP:
                tokens_list.append(token)
            src_program_idx = src_program_idx + len(token.value)
            if (not self.end_of_input(src_program_str, src_program_idx)):
                token = self.next_token(src_program_str, src_program_idx)
            else:
                token = Token(TokenType.EOF, "EOF", self.line_number)

        return tokens_list
    
    
# Test the lexer
lexer = Lexer()
src_program_str = "\\"
#src_program_str = "x = 10 + 20 \n "
tokens = lexer.generate_tokens(src_program_str)
for token in tokens:
    print(token.value, token.TokenType, token.line)