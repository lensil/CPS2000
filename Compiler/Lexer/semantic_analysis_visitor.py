# This file contains the SemanticAnalysisVisitor class which is used to perform semantic analysis on the AST.

from visitor import ASTVisitor
from symbol_table import SymbolTable, ScopeType, Symbol, SymbolType
from parser_testing import *

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
            self.symbol_table.push_scope(ScopeType.BLOCK) 
    
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

        node_type = node.type
        if node_type == TokenType.INT_LITERAL:
            return "int"
        elif node_type == TokenType.FLOAT_LITERAL:
            return "float"
        elif node_type == TokenType.BOOL_LITERAL:
            return "bool"
        elif node_type == TokenType.COLOR_LITERAL:
            return "color"
        else:
            return None

    def visit_binary_op_node(self, node):
                
            """
                
                Visit a binary operation node.
        
                Parameters:
                    node (BinaryOpNode): The binary operation node to visit.

                Returns:
                    The type of the binary operation.
                    
            """
    
            # Visit the left and right children
            operator = node.op
            line = node.line_number
            left_type = node.left.accept(self)
            right_type = node.right.accept(self)
    
            # Check if the types are compatible
            if left_type != right_type:
                raise Exception("Type mismatch in binary operation on line ", line, ". Expected ", left_type, ", got ", right_type)
            
            if operator in ['+', '-', '*', '/']:
                if left_type != "int" and left_type != "float":
                    raise Exception("Invalid type for arithmetic operation on line ", line, ". Expected int or float, got ", left_type)
                return left_type
            
            if not node.cast_expr is None:
                return node.cast_expr

            if operator in ['<', '>', '<=', '>=']:
                if left_type != "int" and left_type != "float":
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
        line = node.line_number
        child_type = node.child.accept(self)
        
        # Check if the type is compatible
        if child_type not in ["int", "float"]:
            raise Exception("Invalid type for unary operation on line ", line)
        
        return child_type
    
    def visit_assignment_node(self, node):
            
        """
            
            Visit an assignment node.
    
            Parameters:
                node (ASTAssignmentNode): The assignment node to visit.

            Returns:
                The type of the assignment.
                
        """
    
        # Visit the identifier and expression
        identifier_type = self.visit_variable_node(node.identifier)
    
        expression_type = node.expression.accept(self)

        # Check if the types are compatible
        if identifier_type != expression_type:
            raise Exception("Type mismatch in assignment on line ", node.line_number, ". Expected ", identifier_type, ", got ", expression_type)
        
        return identifier_type
    
    def visit_variable_node(self, node):
        
        """
        
            Visit a variable node.

            Parameters:
                node (ASTVariableNode): The variable node to visit.

            Returns:
                The type of the variable.
            
        """

        var_type = self.symbol_table.get_type(node.var_name)

        if var_type is None:
            raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)
        
        return var_type
    
    def visit_var_dec_node(self, node):
            
        """
            
            Visit a declaration node.
    
            Parameters:
                node (ASTDeclarationNode): The declaration node to visit.
                
        """
    
        # Add the identifier to the symbol table
        name = node.var_name.var_name 
        line = node.line_number
        type = node.var_type.value
        expr_type = node.var_expression.accept(self)
        if self.symbol_table.is_declared(name):
            raise Exception("Identifier already declared on line ", line, ": ", name)
        if type != expr_type:
            raise Exception("Type mismatch in declaration on line ", line, ". Expected ", type, ", got ", expr_type)
        symbol = Symbol(SymbolType.VARIABLE, line, type, name)
        self.symbol_table.add_symbol(name, symbol)


    def visit_random_node(self, node):
        
        """
        
            Visit a random node.

            Parameters:
                node (ASTRandomNode): The random node to visit.

            Returns:
                The type of the random node.
            
        """

        # Visit the child
        line = node.line_number
        expr_type = node.expression.accept(self)
        
        # Check if the type is compatible
        if expr_type != "int":
            raise Exception("Invalid type for random operation on line ", line)
        
        return expr_type
    
    def visit_delay_node(self, node):
        
        """
        
            Visit a delay node.

            Parameters:
                node (ASTDelayNode): The delay node to visit.

            Returns:
                The type of the delay node.
            
        """

        # Visit the child
        line = node.line_number
        expr_type = node.expression.accept(self)
        
        # Check if the type is compatible
        if expr_type != "int" and expr_type != "float":
            raise Exception("Invalid type for delay operation on line ", line)
        
        return expr_type
    
    def visit_write_node(self, node):
        
        """
        
            Visit a write node.

            Parameters:
                node (ASTWriteNode): The write node to visit.

            Returns:
                The type of the write node.
            
        """

        # Visit the child
        line = node.line_number
        expr1_type = node.expression_1.accept(self)
        expr2_type = node.expression_2.accept(self)
        expr3_type = node.expression_3.accept(self)
        
        if expr1_type != "int":
            raise Exception("Expected int for first argument of write on line ", line, ", got ", expr1_type)
        
        if expr2_type != "int":
            raise Exception("Expected int for second argument of write on line ", line, ", got ", expr2_type)
        
        if expr3_type != "color":
            raise Exception("Expected color for third argument of write on line ", line, ", got ", expr3_type)
        
        return expr1_type
    
    def visit_write_box_node(self, node):
        
        """
        
            Visit a write box node.
            
            Parameters:
                node (ASTWriteBoxNode): The write box node to visit.
                
        """

        # Visit the children
        line = node.line_number
        expr1_type = node.expression_1.accept(self)
        expr2_type = node.expression_2.accept(self)
        expr3_type = node.expression_3.accept(self)
        expr4_type = node.expression_4.accept(self)

        if expr1_type != "int":
            raise Exception("Expected int for first argument of write_box on line ", line, ", got ", expr1_type)
        
        if expr2_type != "int":
            raise Exception("Expected int for second argument of write_box on line ", line, ", got ", expr2_type)
        
        if expr3_type != "int":
            raise Exception("Expected int for third argument of write_box on line ", line, ", got ", expr3_type)
        
        if expr4_type != "color":
            raise Exception("Expected color for fourth argument of write_box on line ", line, ", got ", expr4_type)
       
# Testing the semantic analysis visitor
# Test the parser
src_program = "let x: bool = true; x = 5 + 9;"
parser = Parser(src_program)
parser.Parse()
parser.ASTroot.accept(SemanticAnalysisVisitor())
print("Semantic analysis passed successfully!")