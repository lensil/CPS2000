# Parser implementation
from Lexer import lexer

# Parser class
class Parser:
    def __init__(self):
        self.lexer = lexer.Lexer() # Create a lexer object
        self.index = -1 # Start at -1 so that the first token is at index 0
        self.tokens = self.lexer.generate_tokens() # Generate tokens from the lexer
        # Fix token type add void type???
        self.current_token = lexer.Token("", lexer.TokenType.WHITESPACE) # Current token
        self.next_token = lexer.Token("", lexer.TokenType.WHITESPACE) # Next token
        # Need to add AST program node
        self.ast_root = None # AST root node

    # Get the next token and skip whitespace
    def next_token_skip_whitespace(self):
        self.index += 1 # Grab the next token
        if (self.index < len(self.tokens)): # Check if we have iterated through all tokens
            # If not, set the current token to the next token
            self.current_token = self.tokens[self.index] # Get the token at the current index
        else: # Otherwise
            self.current_token = lexer.Token(lexer.TokenType.EOF, "END") # Set the current token to the end token

    # Get the next token
    def next_token(self):
        self.next_token_skip_whitespace() # Get the next token and skip whitespace
        while (self.current_token.type == lexer.TokenType.WHITESPACE): # Check if the current token is whitespace
            self.next_token_skip_whitespace() # Get the next token and skip whitespace