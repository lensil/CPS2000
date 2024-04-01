"""
This file contains functionality related to tokens that the lexer will use to tokenize the input.

"""

from enum import Enum

class TokenType(Enum):

    """
    This class is an enumeration of all the token types that the lexer will use to tokenize the input.
    
    """

    # Punctuation tokens
    # These tokens are used to represent the punctuation characters of the language
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_SQ_BRACK = 5
    RIGHT_SQ_BRACK = 6
    COMMA = 7
    SEMICOLON = 8

    # Special functions tokens
    # These tokens are used to represent the special functions of the language
    
    RANDOM_INT = 9
    PRINT = 10
    DELAY = 11
    WRITE_BOX = 12
    WRITE = 13

    # Keywords
    # These tokens are used to represent the keywords of the language
    AS = 14
    LET = 15
    RETURN = 16
    IF = 17
    ELSE = 18
    FOR = 19
    WHILE = 20
    FUN = 21

    # Identifiers
    # This token is used to represent the identifiers of the language
    IDENTIFIER = 22

    # Literals
    # These tokens are used to represent the literals of the language
    INT_LITERAL = 23
    FLOAT_LITERAL = 24
    BOOL_LITERAL = 25
    COLOR_LITERAL = 26
    WIDTH = 27
    HEIGHT = 28
    READ = 29


    # Skip tokens
    # This token is used to represent the tokens that the lexer will skip 
    SKIP = 30

    # Operators
    # These tokens are used to represent the operators of the language
    ADDITIVE_OP = 31
    MULTIPLICATIVE_OP = 32
    ASSIGNMENT_OP = 33
    EQUAL_OP = 34
    NOT_EQUAL_OP = 35
    GREATER_OP = 36
    LESS_OP = 37
    GREATER_EQUAL_OP = 38
    LESS_EQUAL_OP = 39
    FUNC_ASSIGNMENT_OP = 40

    # End of file token
    # This token is used to represent the end of the file
    EOF = 41

    # Error token
    # This token is used to represent an error in the input
    ERROR = 42