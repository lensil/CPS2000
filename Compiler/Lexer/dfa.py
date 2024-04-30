"""

This file contains functionality related to the DFA that the lexer will use to tokenize the input.

"""

from enum import Enum

DFAStates = Enum('DFAStates', {f'S_{i}': i for i in range(28)})

def input_categories(character):
    
        """
        
        This function defines the categories of input that the DFA will accept.

        Parameters:
            character (str): The character to categorize.
        
        """

        match character:
            case char if char.isdigit():
                return 'digit'
            case 'a' | 'A' | 'b' | 'B' | 'c' | 'C' | 'd' | 'D' | 'e' | 'E' | 'f' | 'F':
                return 'hex'
            case char if char.isalpha():
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

class DFA:
    """
    This class defines the DFA that the lexer will use to tokenize the input.
    """

    def __init__(self):
        self.states = DFAStates
        self.start_state = self.states.S_0
        self.final_states = [self.states.S_1, self.states.S_2, self.states.S_3, self.states.S_4, self.states.S_5, self.states.S_6, self.states.S_9, self.states.S_10, self.states.S_12, self.states.S_10, self.states.S_11, self.states.S_12,
                                 self.states.S_13, self.states.S_16, self.states.S_17, self.states.S_18, self.states.S_20, self.states.S_27]
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
            (self.states.S_5, 'newline'): self.states.S_6,
            (self.states.S_4, 'star'): self.states.S_7,
            (self.states.S_7, 'star'): self.states.S_8,
            (self.states.S_8, 'star'): self.states.S_8,
            (self.states.S_8, 'slash'): self.states.S_6,
        }
        
        for char in ['digit', 'hex', 'letter', 'plus', 'minus', 'star', 'slash', 'punctuation', 'whitespace', 'equals', 'less', 'greater', 'exclamation', 'hash', 'dot', 'underscore', 'other']:
            self.transitions.update({(self.states.S_5, char): self.states.S_5})
            
        for char in ['digit', 'hex', 'letter', 'plus', 'minus', 'slash', 'punctuation', 'whitespace', 'newline', 'equals', 'less', 'greater', 'exclamation', 'hash', 'dot', 'underscore', 'other']:
            self.transitions.update({(self.states.S_7, char): self.states.S_7})

        for char in ['digit', 'hex', 'letter', 'plus', 'minus', 'punctuation', 'whitespace', 'newline', 'equals', 'less', 'greater', 'exclamation', 'hash', 'dot', 'underscore', 'other']:
            self.transitions.update({(self.states.S_8, char): self.states.S_7})

        self.transitions.update({

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
            (self.states.S_15, 'hex'): self.states.S_16,
            (self.states.S_16, 'letter'): self.states.S_16,
            (self.states.S_16, 'hex'): self.states.S_16,
            (self.states.S_16, 'underscore'): self.states.S_16,
            
            # Tokenizing identifiers
            (self.states.S_0, 'letter'): self.states.S_17,
            (self.states.S_0, 'hex'): self.states.S_17,
            (self.states.S_17, 'letter'): self.states.S_17,
            (self.states.S_17, 'hex'): self.states.S_17,
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
            (self.states.S_21, 'digit'): self.states.S_22,
            (self.states.S_22, 'hex'): self.states.S_23,
            (self.states.S_22, 'digit'): self.states.S_23,
            (self.states.S_23, 'hex'): self.states.S_24,
            (self.states.S_23, 'digit'): self.states.S_24,
            (self.states.S_24, 'hex'): self.states.S_25,
            (self.states.S_24, 'digit'): self.states.S_25,
            (self.states.S_25, 'hex'): self.states.S_26,
            (self.states.S_25, 'digit'): self.states.S_26,
            (self.states.S_26, 'hex'): self.states.S_27,
            (self.states.S_26, 'digit'): self.states.S_27
        })

    def accepting_states(self, state):
        
        """
            
            This function checks if the given state is an accepting state.
    
            Parameters:
                state (DFAStates): The state to check.
            
            """
    
        return state in self.final_states

