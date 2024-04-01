"""

This file contains functionality related to the DFA that the lexer will use to tokenize the input.

"""

from enum import Enum

class DFAStates(Enum):

    """
    
    This class is an enumeration of all the states that the DFA can be in.
    
    """

    S_0 = 0 # Start state
    S_1 = 1
    S_2 = 2
    S_3 = 3
    S_4 = 4
    S_5 = 5
    S_6 = 6
    S_7 = 7
    S_8 = 8
    S_9 = 9
    S_10 = 10
    S_11 = 11
    S_12 = 12
    S_13 = 13
    S_14 = 14
    S_15 = 15
    S_16 = 16
    S_17 = 17
    S_18 = 18
    S_19 = 19
    S_20 = 20
    S_21 = 21
    S_22 = 22
    S_23 = 23
    S_24 = 24
    S_25 = 25
    S_26 = 26

def input_categories(character):
    
        """
        
        This function defines the categories of input that the DFA will accept.

        Parameters:
            character (str): The character to categorize.
        
        """

        match character:
            case character.isdigit():
                return 'digit'
            case 'a' | 'A' | 'b' | 'B' | 'c' | 'C' | 'd' | 'D' | 'e' | 'E' | 'f' | 'F':
                return 'hex'
            case character.isalpha():
                return 'letter'
            case '+':
                return 'plus'
            case '-':
                return 'minus'
            case '*':
                return 'star'
            case '/':
                return 'slash'
            case '(' | ')' | '{' | '}' | '[' | ']' | ',' | ':' | ';':
                return 'punctuation'
            case ' ' | '\t':
                return 'whitespace'
            case '\n':
                return 'newline'
            case '=':
                return 'equals'
            case '<' :
                return 'less'
            case '>':
                return 'greater'
            case '!':
                return 'exclamation'
            case '#':
                return 'hash'
            case '.':
                return 'dot'
            case '_':
                return 'underscore'
            case __:
                return 'other'
        
print(input_categories('8')) # Should print 'digit'


class DFA:

    """
        
        This class defines the DFA that the lexer will use to tokenize the input.
        
    """

    def __init__(self):
        self.states = DFAStates
        self.final_states = [self.states.S_1, self.states.S_2, self.states.S_3, self.states.S_4, self.states.S_5, self.states.S_6, self.states.S_9, self.states.S_10, self.states.S_12, self.states.S_10, self.states.S_11, self.states.S_12,
                                 self.states.S_13, self.states.S_16, self.states.S_17, self.states.S_18, self.states.S_20, self.states.S_26]
        self.current_state = self.states.S_0
        
        # Define the transitions for the DFA as a dictionary
        self.transitions = {

            # Tokenizing operators
            (self.states.S_0, 'minus'): self.states.S_1,
            (self.states.S_1, 'greater'): self.states.S_2,
            (self.states.S_0, 'plus'): self.states.S_3,
            (self.states.S_0, 'star'): self.states.S_3,
            (self.states.S_0, 'slash'): self.states.S_4,

            # Tokenizing whitespace 
            (self.states.S_0, 'whitespace'): self.states.S_6,
            (self.states.S_0, 'newline'): self.states.S_6,
            (self.states.S_6, 'whitespace'): self.states.S_6,
            (self.states.S_6, 'newline'): self.states.S_6,

            # Tokenizing comments
            (self.states.S_4, 'slash'): self.states.S_5,
            (self.states.S_5, 'digit'): self.states.S_5,
            (self.states.S_5, 'hex'): self.states.S_5,
            (self.states.S_5, 'letter'): self.states.S_5,
            (self.states.S_5, 'plus'): self.states.S_5,
            (self.states.S_5, 'minus'): self.states.S_5,
            (self.states.S_5, 'star'): self.states.S_5,
            (self.states.S_5, 'slash'): self.states.S_5,
            (self.states.S_5, 'punctuation'): self.states.S_5,
            (self.states.S_5, 'whitespace'): self.states.S_5,
            (self.states.S_5, 'newline'): self.states.S_6,
            (self.states.S_5, 'equals'): self.states.S_5,
            (self.states.S_5, 'less'): self.states.S_5,
            (self.states.S_5, 'greater'): self.states.S_5,
            (self.states.S_5, 'exclamation'): self.states.S_5,
            (self.states.S_5, 'hash'): self.states.S_5,
            (self.states.S_5, 'dot'): self.states.S_5,
            (self.states.S_5, 'underscore'): self.states.S_5,
            (self.states.S_5, 'other'): self.states.S_5,
            (self.states.S_4, 'star'): self.states.S_7,
            (self.states.S_7, 'digit'): self.states.S_7,
            (self.states.S_7, 'hex'): self.states.S_7,
            (self.states.S_7, 'letter'): self.states.S_7,
            (self.states.S_7, 'plus'): self.states.S_7,
            (self.states.S_7, 'minus'): self.states.S_7,
            (self.states.S_7, 'star'): self.states.S_8,
            (self.states.S_7, 'slash'): self.states.S_7,
            (self.states.S_7, 'punctuation'): self.states.S_7,
            (self.states.S_7, 'whitespace'): self.states.S_7,
            (self.states.S_7, 'newline'): self.states.S_7,
            (self.states.S_7, 'equals'): self.states.S_7,
            (self.states.S_7, 'less'): self.states.S_7,
            (self.states.S_7, 'greater'): self.states.S_7,
            (self.states.S_7, 'exclamation'): self.states.S_7,
            (self.states.S_7, 'hash'): self.states.S_7,
            (self.states.S_7, 'dot'): self.states.S_7,
            (self.states.S_7, 'underscore'): self.states.S_7,
            (self.states.S_7, 'other'): self.states.S_7,
            (self.states.S_8, 'digit'): self.states.S_7,
            (self.states.S_8, 'hex'): self.states.S_7,
            (self.states.S_8, 'letter'): self.states.S_7,
            (self.states.S_8, 'plus'): self.states.S_7,
            (self.states.S_8, 'minus'): self.states.S_7,
            (self.states.S_8, 'star'): self.states.S_8,
            (self.states.S_8, 'slash'): self.states.S_6,
            (self.states.S_8, 'punctuation'): self.states.S_7,
            (self.states.S_8, 'whitespace'): self.states.S_7,
            (self.states.S_8, 'newline'): self.states.S_7,
            (self.states.S_8, 'equals'): self.states.S_7,
            (self.states.S_8, 'less'): self.states.S_7,
            (self.states.S_8, 'greater'): self.states.S_7,
            (self.states.S_8, 'exclamation'): self.states.S_7,
            (self.states.S_8, 'hash'): self.states.S_7,
            (self.states.S_8, 'dot'): self.states.S_7,
            (self.states.S_8, 'underscore'): self.states.S_7,
            (self.states.S_8, 'other'): self.states.S_7,

            # Tokenizing the assignment operator
            (self.states.S_0, 'equals'): self.states.S_9,

            # Tokenizing relational operators
            (self.states.S_0, 'greater'): self.states.S_10,
            (self.states.S_0, 'less'): self.states.S_10,
            (self.states.S_0, 'exclamation'): self.states.S_11,
            (self.states.S_9, 'equals'): self.states.S_12,
            (self.states.S_10, 'equals'): self.states.S_12,
            (self.states.S_11, 'equals'): self.states.S_12,

            # Tokenizing punctuation
            (self.states.S_0, 'punctuation'): self.states.S_13,

            # Tokenizing special language functions/literals
            (self.states.S_0, 'underscore'): self.states.S_14,
            (self.states.S_14, 'underscore'): self.states.S_15,
            (self.states.S_15, 'letter'): self.states.S_16,
            (self.states.S_16, 'letter'): self.states.S_16,
            (self.states.S_16, 'underscore'): self.states.S_16,
            
            # Tokenizing identifiers
            (self.states.S_0, 'letter'): self.states.S_17,
            (self.states.S_0, 'hex'): self.states.S_17,
            (self.states.S_17, 'letter'): self.states.S_17,
            (self.states.S_17, 'digit'): self.states.S_17,
            (self.states.S_17, 'underscore'): self.states.S_17,

            # Tokenizing integer literals
            (self.states.S_0, 'digit'): self.states.S_18,
            (self.states.S_18, 'digit'): self.states.S_18,

            # Tokenizing floating point literals
            (self.states.S_18, 'dot'): self.states.S_19,
            (self.states.S_19, 'digit'): self.states.S_20,
            (self.states.S_20, 'digit'): self.states.S_20,

            # Tokenizing color literals
            (self.states.S_0, 'hash'): self.states.S_21,
            (self.states.S_21, 'hex'): self.states.S_22,
            (self.states.S_22, 'hex'): self.states.S_23,
            (self.states.S_23, 'hex'): self.states.S_24,
            (self.states.S_24, 'hex'): self.states.S_25,
            (self.states.S_25, 'hex'): self.states.S_26

        }