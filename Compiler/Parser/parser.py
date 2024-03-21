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
