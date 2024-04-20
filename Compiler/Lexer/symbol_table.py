"""

    Represents the symbol table used during the semantic analysis phase of the compiler.

"""

from enum import Enum

class SymbolType(Enum):

    """
    
        The type of the symbol.
        
    """
    VARIABLE = 1
    FUNCTION = 2

class ScopeType(Enum):
    
        """
        
            The type of the scope.
            
        """
        GLOBAL = 1
        BLOCK = 2
        FUNCTION = 3

class Symbol:

    """

        Represents a symbol in the symbol table. A symbol has a type, value, and parameters.

    """

    def __init__(self, symbol_type,line, value=None, params=None):
        self.symbol_type = symbol_type # The type of the sumbol (variable or function)
        self.value = value # The value of the symbol (if the symbol is a variable)
        self.params = params # The parameters of the function (if the symbol is a function)
        self.line = line # The line number of the symbol
        self.type = None # The type of the variable/return type of the function


class SymbolTable:
    
    """

        A symbol table represnted as a stack of scopes. Each scope is a dictionary that maps variable names to their attributes.
    
    """
    def __init__(self):
        self.scopes = []
        self.scope_types = []
        self.push_scope(ScopeType.GLOBAL) # Push the global scope

    def push_scope(self, scope_type):

        """

            Pushes a new scope onto the stack.

            Parameters:
                scope_type: The type of the scope.

        """

        self.scopes.append({})
        self.scope_types.append(scope_type)

    def pop_scope(self):

        """

            Pops the top scope off the stack.

        """

        self.scopes.pop()
        self.scope_types.pop()

    def add_symbol(self, name, symbol):

        """

            Adds a symbol to the current scope.

        """

        self.scopes[-1][name] = symbol

    def lookup(self, name):

        """

            Looks up a symbol in the symbol table.

        """
        
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def is_declared(self, name):

        """

            Checks if a symbol is already declared in the symbol table or not.

            Parameters:
                name: The name of the symbol to check.

            Returns:
                True if the symbol is declared, False otherwise.

        """

        return self.lookup(name) is not None
    
    def is_function_scope(self):
            
        """
    
            Checks if the current scope is a function scope or not.
    
            Returns:
                True if the current scope is a function scope, False otherwise.
    
        """

        return self.scope_types[-1] == ScopeType.FUNCTION
    
    def get_type(self, name):
            
        """
    
            Returns the type of a symbol.

            Parameters:
                name: The name of the symbol.

            Returns:
                The type of the symbol if it exists, None otherwise.
    
        """
    
        symbol = self.lookup(name)
        if symbol is not None:
            return symbol.type
        return None
    
    def get_line(self, name):
        
        """
    
            Returns the line number of a symbol.

            Parameters:
                name: The name of the symbol.

            Returns:
                The line number of the symbol if it exists, None otherwise.
    
        """
    
        symbol = self.lookup(name)
        if symbol is not None:
            return symbol.line
        return None