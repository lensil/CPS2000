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

    def __init__(self, symbol_type, line, type=None, value=None, params=None):
        self.symbol_type = symbol_type # The type of the sumbol (variable or function)
        self.value = value # The value of the symbol (if the symbol is a variable)
        self.params = params # The parameters of the function (if the symbol is a function)
        self.line = line # The line number of the symbol
        self.type = type # The type of the variable/return type of the function
        self.frame_index = None  # Keeps track of the index of the variable in the frame
        self.frame_level = None  # Keeps track of the level of the frame

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

    def lookup(self, name, scope_type):

        """

            Looks up a symbol in the symbol table.

            Parameters:
                name: The name of the symbol to look up.

            Returns:
                The symbol if it exists, None otherwise.

        """

        # If the scope type is function, only look in the current scope
        if scope_type == ScopeType.FUNCTION:
            if name in self.scopes[-2] and self.scopes[-2][name].symbol_type == SymbolType.FUNCTION:
                return self.scopes[-2][name]
            else: 
                return None
        
        # If the scope type is block, look in the current scope and all the scopes above it
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def is_declared(self, name, scope_type=ScopeType.BLOCK):

        """

            Checks if a symbol is already declared in the symbol table or not.

            Parameters:
                name: The name of the symbol to check.

            Returns:
                True if the symbol is declared, False otherwise.

        """

        return self.lookup(name, scope_type) is not None
    
    def is_function_scope(self):
            
        """
    
            Checks if the current scope is a function scope or not.
    
            Returns:
                True if the current scope is a function scope, False otherwise.
    
        """

        return self.scope_types[-1] == ScopeType.FUNCTION
    
    def is_global_scope(self):
        
        """
    
            Checks if the current scope is a global scope or not.
    
            Returns:
                True if the current scope is a global scope, False otherwise.
    
        """

        return self.scope_types[-1] == ScopeType.GLOBAL
    
    def get_type(self, name, scope_type=ScopeType.BLOCK):
            
        """
    
            Returns the type of a symbol.

            Parameters:
                name: The name of the symbol.

            Returns:
                The type of the symbol if it exists, None otherwise.
    
        """
    
        symbol = self.lookup(name, self.get_current_scope_type)
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
    
    def get_params(self, name):
            
            """
        
                Returns the parameters of a function.
    
                Parameters:
                    name: The name of the function.
    
                Returns:
                    The parameters of the function if it exists, None otherwise.
        
            """
        
            symbol = self.lookup(name, ScopeType.FUNCTION)
            if symbol is not None:
                return symbol.params
            return None

    def get_current_scope_type(self):
        
        """
    
            Returns the type of the current scope.
    
            Returns:
                The type of the current scope.
    
        """

        return self.scope_types[-1]
    
    def get_current_frame_level(self):

        """
    
            Returns the level of the current frame.
    
            Returns:
                The level of the current frame.
    
        """

        return len(self.scopes) - 1
    
    def get_curent_frame_index(self):

        """
    
            Returns the index of the current frame.
    
            Returns:
                The index of the current frame.
    
        """

        return len(self.scopes[-1])
    
    def set_location(self, name, frame_index, frame_level):
        
        """
    
            Sets the location of a variable in the frame.
    
            Parameters:
                name: The name of the variable.
                frame_index: The index of the variable in the frame.
                frame_level: The level of the frame.
    
        """

        symbol = self.lookup(name)
        symbol.frame_index = frame_index
        symbol.frame_level = frame_level

    def get_location(self, name):

        """
    
            Gets the location of a variable in the frame.
    
            Parameters:
                name: The name of the variable.
    
            Returns:
                The index of the variable in the frame.
    
        """

        symbol = self.lookup(name)
        return symbol.frame_index, symbol.frame_level