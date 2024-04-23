# Lexer Implementation
from dfa import DFA, input_categories
from tokens import Token, token_type_by_final_state, TokenType

# Lexer Class
class Lexer:
    def __init__(self):
        self.dfa = DFA()
        self.line_number = 1
            
    def end_of_input(self, src_program_str, src_program_idx):

        """

        Check if the end of the input has been reached

        Parameters:
            src_program_str (str): The source program string
            src_program_idx (int): The index of the current character in the source program string

        Returns:
            bool: True if the end of the input has been reached, False otherwise
        
        """
        if (src_program_idx > len(src_program_str)-1): # Check if the index is greater than the length of the input
            return True  # Return True if the end of the input has been reached
        else:
            return False # Return False if the end of the input has not been reached

    def next_char(self, src_program_str, src_program_idx):

        """

        Get the next character in the input

        Parameters:
            src_program_str (str): The source program string
            src_program_idx (int): The index of the current character in the source program string

        Returns:
            bool: True if the next character exists, False otherwise
            str: The next character in the input

        """

        if (not self.end_of_input(src_program_str, src_program_idx)): # Check that the end of the input has not been reached
            if src_program_str[src_program_idx] == '\n': # Check if the current character is a newline character
                self.line_number += 1 # Increment the line number
            return True, src_program_str[src_program_idx] # Return True and the current character
        else: # If the end of the input has been reached
            return False, "." # Return False 
        
    def next_token(self, src_program_str, src_program_idx):

        """
        
        Get the next token in the input
        
        Parameters:
            src_program_str (str): The source program string
            src_program_idx (int): The index of the current character in the source program string
            
        Returns:
            Token: The next token in the input
        
        """

        lexeme = "" # Initialize the lexeme to an empty string
        state = self.dfa.start_state # Set the state to the start state of the DFA
        stack = [] # Initialize an empty stack
        stack.append(-2) # Push -2 onto the stack

        while (state != None): # Loop while the state is not None i.e. while an invalid state has not been reached
            if self.dfa.accepting_states(state):  # Check if the current state is an accepting state
                stack.clear() # Clear the stack
            stack.append(state) # Push the current state onto the stack

            exists, character = self.next_char(src_program_str, src_program_idx) # Get the next character in the input
            lexeme += character # Append the character to the lexeme
            if (not exists):  # Check if the character exists
                break # Break out of the loop
            src_program_idx = src_program_idx + 1 # Increment the index

            cat = input_categories(character) # Get the category of the character
            state = self.dfa.transitions.get((state, cat), None) # Get the next state based on the current state and category
            if (state == None): # Check if the state is None
                if character == "\n": # Check if the character is a newline character
                    self.line_number -= 1 # Decrement the line number

        lexeme = lexeme[:-1] # Remove the last character from the lexeme

        syntax_error = False # Initialize the syntax error flag to False

        while (len(stack) > 0): # Loop while the stack is not empty
            if (stack[-1] == -2): # Check if the top of the stack is -2
                syntax_error = True # Set the syntax error flag to True
                break # Break out of the loop

            if (not self.dfa.accepting_states(stack[-1])): # Check if the top of the stack is not an accepting state
                stack.pop() # Pop the top of the stack
                lexeme = lexeme[:-1] # Remove the last character from the lexeme
            else: # If the top of the stack is an accepting state
                state = stack.pop() # Pop the top of the stack
                break # Break out of the loop

        if syntax_error: # Check if there is a syntax error
            raise Exception("Invalid lexeme: " + lexeme + " at line " + str(self.line_number)) # Raise an exception
        if self.dfa.accepting_states(state): # Check if the state is an accepting state
            return token_type_by_final_state(state.value, lexeme, self.line_number)  # Return the token type based on the final state
        else: # If the state is not an accepting state
            raise Exception("Invalid lexeme: " + lexeme + " at line " + str(self.line_number)) # Raise an exception
        
    def generate_tokens(self, src_program_str):
        
        """

        Generate tokens from the source program string

        Parameters:
            src_program_str (str): The source program string

        Returns:
            list: A list of tokens generated from the source program string
        
        """

        tokens_list = [] # Initialize an empty list to store the tokens
        src_program_idx = 0 # Initialize the index to 0
        token = self.next_token(src_program_str, src_program_idx) # Get the next token

        while (token.TokenType != TokenType.EOF): # Loop while the token type is not EOF
            if token.TokenType != TokenType.SKIP: # Check if the token type is not SKIP
                tokens_list.append(token) # Append the token to the list if the token type is not SKIP
            src_program_idx = src_program_idx + len(token.value) # Increment the index by the length of the token value
            if (not self.end_of_input(src_program_str, src_program_idx)): # Check if the end of the input has not been reached
                token = self.next_token(src_program_str, src_program_idx) # Get the next token if the end of the input has not been reached
            else: # If the end of the input has been reached
                token = Token(TokenType.EOF, "EOF", self.line_number) # Set the token type to EOF

        tokens_list.append(token)   
        return tokens_list # Return the list of tokens