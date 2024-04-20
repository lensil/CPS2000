# This file contains the SemanticAnalysisVisitor class which is used to perform semantic analysis on the AST.

from visitor import ASTVisitor
from symbol_table import SymbolTable

class SemanticAnalysisVisitor(ASTVisitor):

    """
    
        Visitor which traverses the AST and performs type checking for semantic analysis.
        
    """

    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_program_node(self, node):

        """
        
            Visit a program node.

            Parameters:
                node (ASTProgramNode): The program node to visit.
            
        """

        for statement in node.statements:
            statement.accept(self)

    def visit_block_node(self, node):
            
            """
            
                Visit a block node.
    
                Parameters:
                    node (ASTBlockNode): The block node to visit.
                
            """

            # Push a new scope onto the symbol table
            self.symbol_table.push_scope() 
    
            # Visit each statement in the block
            for statement in node.statements:
                statement.accept(self)

            # Pop the scope off the symbol table
            self.symbol_table.pop_scope()

    def visit_literal_node(self, node):
            
        """
            
            Visit a literal node.
    
            Parameters:
                node (ASTLiteralNode): The literal node to visit.
                
        """

        return node.type

    def visit_binary_op_node(self, node):
                
            """
                
                Visit a binary operation node.
        
                Parameters:
                    node (BinaryOpNode): The binary operation node to visit.

                Returns:
                    The type of the binary operation.
                    
            """
    
            # Visit the left and right children
            operator = node.operator
            line = node.line
            left_type = node.left.accept(self)
            right_type = node.right.accept(self)
    
            # Check if the types are compatible
            if left_type != right_type:
                raise Exception("Type mismatch in binary operation on line ", line, ". Expected ", left_type, ", got ", right_type)
            
            if operator in ['+', '-', '*', '/']:
                if left_type != "int" or left_type != "float":
                    raise Exception("Invalid type for arithmetic operation on line ", line, ". Expected int or float, got ", left_type)
                return left_type

            if operator in ['<', '>', '<=', '>=']:
                if left_type != "int" or left_type != "float":
                    raise Exception("Invalid type for comparison operation on line ", line, ". Expected int or float, got ", left_type)
                return "bool"
            
            if operator in ['==', '!=']:
                return "bool"
            
            if operator in ['and', 'or']:
                if left_type != "bool":
                    raise Exception("Invalid type for logical operation on line ", line, ". Expected bool, got ", left_type)
                return "bool"
    
            return left_type
    
    def visit_unary_op_node(self, node):
         
        """
            
            Visit a unary operation node.
    
            Parameters:
                node (UnaryOpNode): The unary operation node to visit.

            Returns:
                The type of the unary operation.
                
        """
        
        # Visit the child
        line = node.line
        child_type = node.child.accept(self)
        
        # Check if the type is compatible
        if child_type not in ["int", "float"]:
            raise Exception("Invalid type for unary operation on line ", line)
        
        return child_type
    
    def visit_identifier_node(self, node):

        """
        
            Visit an identifier node.

            Parameters:
                node (IdentifierNode): The identifier node to visit.
            
        """

        # Check if the identifier is declared
        name = node.name
        line = node.line
        if not self.symbol_table.is_declared(name):
            raise Exception("Undeclared identifier on line ", line, ": ", name)
        
        return self.symbol_table.get_type(name)