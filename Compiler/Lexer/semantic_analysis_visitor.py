# This file contains the SemanticAnalysisVisitor class which is used to perform semantic analysis on the AST.
# To do: parameters in functions?
# To do: fix write_box methods
# to do: fix function related stuff
from visitor import ASTVisitor
from symbol_table import SymbolTable, ScopeType, Symbol, SymbolType
from parser_testing import *
from astnodes import *

class SemanticAnalysisVisitor(ASTVisitor):

    """
    
        Visitor which traverses the AST and performs type checking for semantic analysis.
        
    """

    def __init__(self):
        self.symbol_table = SymbolTable() # Symbol table used for type checking

        self.current_function_name = None # Name of the current function being visited
        
        self.returns = False # Flag to check if a return statement is present in the function

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

            self.symbol_table.push_scope(ScopeType.BLOCK) 
    
            # Visit each statement in the block
            for statement in node.statements:
                statement.accept(self)

            if not self.symbol_table.is_function_scope():
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
        elif node_type == TokenType.WIDTH:
            return "int"
        elif node_type == TokenType.HEIGHT:
            return "int"
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
                if left_type != "int" and left_type != "float" and left_type != "color" and left_type != "width" and left_type != "height":
                    raise Exception("Invalid type for arithmetic operation on line ", line, ". Expected int or float, got ", left_type)
                type = left_type
            
            if operator in ['<', '>', '<=', '>=']:
                if left_type != "int" and left_type != "float" and left_type != "color" and left_type != "width" and left_type != "height":
                    raise Exception("Invalid type for comparison operation on line ", line, ". Expected int or float, got ", left_type)
                type = "bool"
            
            if operator in ['==', '!=']:
                type = "bool"
            
            if operator in ['and', 'or']:
                if left_type != "bool":
                    raise Exception("Invalid type for logical operation on line ", line, ". Expected bool, got ", left_type)
                type = "bool"
            
            if not node.cast_expr is None:
                type = node.cast_expr
    
            return type
    
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
        expr_type = node.expression.accept(self)

        if node.operand == "not":
            if expr_type != "bool":
                raise Exception("Invalid type for unary operation on line ", line)

        elif node.operand == "-":
            if expr_type != "float" and expr_type != "int":
                raise Exception("Invalid type for unary operation on line ", line)
            if not isinstance(node.expression, ASTLiteralNode):
                raise Exception("Expected literal on line ", line)
        
        return expr_type
    
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

        if self.current_function_name is not None:
            parameters = self.symbol_table.get_params(self.current_function_name)
            for param in parameters:
                if param["name"] == node.var_name:
                    type = param["type"]
                elif self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type()) is None:
                    raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)
            symbol = self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type())
            if symbol is None:
                raise Exception("Undeclared variable ", node.var_name, " on line ",  node.line_number)
            type = self.symbol_table.get_type(node.var_name)
            return type

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

        if self.current_function_name is not None:
            parameters = self.symbol_table.get_params(self.current_function_name)
            for param in parameters:
                if param["name"] == name:
                    raise Exception("Variable name clashes with parameter name on line ", line, ": ", name)
            symbol = self.symbol_table.lookup(name, self.symbol_table.get_current_scope_type())
            if self.symbol_table.lookup(name, self.symbol_table.get_current_scope_type()) is None:
                symbol = Symbol(SymbolType.VARIABLE, line, type, name, self.symbol_table.current_frame_index, self.symbol_table.current_frame_level)
                self.symbol_table.add_symbol(name, symbol)
                return type
            else:
                raise Exception("Identifier already declared on line ", line, ": ", name)
            
        if self.symbol_table.is_declared(name):
            raise Exception("Identifier already declared on line ", line, ": ", name)
        
        if type != expr_type:
            raise Exception("Type mismatch in declaration on line ", line, ". Expected ", type, ", got ", expr_type)
        symbol = Symbol(SymbolType.VARIABLE, line, type, name)
        self.symbol_table.add_symbol(name, symbol)

        return type

    def visit_array_dec_node(self, node):

        name = node.var_name.var_name 
        line = node.line

        if self.symbol_table.is_declared(name):
            raise Exception("Identifier already declared on line ", line, ": ", name)
        
        if self.current_function_name is not None:
            parameters = self.symbol_table.get_params(self.current_function_name)
            for param in parameters:
                if param["name"] == name:
                    raise Exception("Variable name clashes with parameter name on line ", line, ": ", name)
        
        
        if node.size is not None and len(node.array) != int(node.size):
            print("Expected array length", node.size, "but got", len(node.array))
            raise Exception("Array length does not match the number of elements on line ", node.line)
        type = node.var_type.value

        for element in node.array:
            element_type = element.accept(self)
            if type != element_type:
                raise Exception("Type mismatch in declaration on line ", line, ". Expected ", type, ", got ", element_type)

        symbol = Symbol(SymbolType.VARIABLE, line, type, name)
        self.symbol_table.add_symbol(name, symbol)

        return type
            
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
            raise Exception("Invalid type for delay operation on line ", line, ". Expected int or float, got ", expr_type)
        
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
        expr5_type = node.expression_5.accept(self)

        if expr1_type != "int":
            raise Exception("Expected int for first argument of write_box on line ", line, ", got ", expr1_type)
        
        if expr2_type != "int":
            raise Exception("Expected int for second argument of write_box on line ", line, ", got ", expr2_type)
        
        if expr3_type != "int":
            raise Exception("Expected int for third argument of write_box on line ", line, ", got ", expr3_type)
        
        if expr4_type != "int":
            raise Exception("Expected int for fourth argument of write_box on line ", line, ", got ", expr4_type)
        
        if expr5_type != "color":
            raise Exception("Expected color for fifth argument of write_box on line ", line, ", got ", expr5_type)
        
    def visit_read_node(self, node):
        
        """
        
            Visit a read node.
            
            Parameters:
                node (ASTReadNode): The read node to visit.
                
        """

        # Visit the child
        line = node.line_number
        expr_type_left = node.left_expression.accept(self)
        expr_type_right = node.right_expression.accept(self)
        
        if expr_type_left != "int":
            raise Exception("Expected int for left argument of read on line ", line, ", got ", expr_type_left)
        
        if expr_type_right != "int":
            raise Exception("Expected int for right argument of read on line ", line, ", got ", expr_type_right)
        
        return expr_type_left
    
    def visit_function_call_node(self, node):
        
        """
        
            Visit a function call node.
            
            Parameters:
                node (ASTFunctionCallNode): The function call node to visit.
                
        """

        function_name = node.function_name 
        line = node.line_number
        parameters = node.parameters

        # Check if the function is defined
        if not self.symbol_table.is_declared(function_name):
            raise Exception("Function not declared on line ", line, ": ", function_name)
        
        # Get the function definition from the symbol table
        function_symbol = self.symbol_table.lookup(function_name, self.symbol_table.get_current_scope_type)

        # Check if the number of parameters match
        if len(parameters) != len(function_symbol.params):
            raise Exception("Number of parameters do not match in function call on line ", line, ". Expected ", len(function_symbol.params), ", got ", len(parameters))
        
        # Check if the types of the parameters match
        for i in range(len(parameters)):
            param_type = parameters[i].accept(self)
            if param_type != function_symbol.params[i]["type"]:
                raise Exception("Type mismatch in function call on line ", line, ". Expected ", function_symbol.params[i]["type"], ", got ", param_type)
            
        return function_symbol.type

    def visit_function_node(self, node):
        
        """
        
            Visit a function node.
            
            Parameters:
                node (ASTFunctionNode): The function node to visit.
                
        """

        name = node.func_name.value
        func_parameters = []
        
        for param in node.parameters:
            parameter = param.accept(self)
            if (parameter["name"], parameter["type"]) in func_parameters:
                raise Exception("Duplicate parameter in function declaration on line ", node.line_number, ": ", parameter["name"])
            func_parameters.append(parameter)

        return_type = node.return_type.value

        # Add the function to the symbol table
        if self.symbol_table.is_declared(name):
            raise Exception("Function already declared on line ", node.line_number, ": ", name)
        
        if self.symbol_table.is_function_scope():
            raise Exception("Function declaration inside a function on line ", node.line_number, ": ", name)
        
        symbol = Symbol(SymbolType.FUNCTION, node.line_number, return_type, name, func_parameters)

        self.symbol_table.add_symbol(name, symbol)

        # Visit the block
        self.symbol_table.push_scope(ScopeType.FUNCTION)
        self.current_function_name = name
        node.body.accept(self)
        
        if not self.returns:
            raise Exception("Function does not return a value on line ", node.line_number, ": ", name)
        
        self.current_function_name = None
        self.symbol_table.pop_scope()

    def visit_formal_parameter_node(self, node):
        
        """
        
            Visit a formal parameter node.
            
            Parameters:
                node (ASTFormalParameterNode): The formal parameter node to visit.

            Returns:
                A dictionary containing the name and type of the parameter.
                
        """

        name = node.var_name.value
        type = node.type.value
    
        # Return the name and type of the parameter
        return {"name": name, "type": type}

    def visit_print_node(self, node):

        """
        
            Visit a print node.
            
            Parameters:
                node (ASTPrintNode): The print node to visit.
                
        """

        # Visit the child
        line = node.line_number
        expr_type = node.expression.accept(self)
        
        # Check if the type is compatible
        if expr_type != "int" and expr_type != "float" and expr_type != "bool" and expr_type != "color":
            raise Exception("Invalid type for print operation on line ", line)
        
        return expr_type
    
    def visit_if_node(self, node):

        """
        
            Visit an if node.
            
            Parameters:
                node (ASTIfNode): The if node to visit.
                
        """

        if self.current_function_name is not None:
            self.returns = False

        # Visit the condition and block
        line = node.line_number
        condition_type = node.condition.accept(self)
    
        # Check if the type is compatible
        if condition_type != "bool":
            raise Exception("Invalid type for if condition on line ", line, ". Expected bool, got ", condition_type)
        
        node.true_block.accept(self)

        if self.current_function_name is not None and not self.returns: 
            raise Exception("Function does not return a value on line ", line, ": ", self.current_function_name)
        
        
        node.true_block.accept(self)

        if not node.false_block is None:
            if self.current_function_name is not None:
                self.returns = False
            node.false_block.accept(self)

        return condition_type

    def visit_while_node(self, node):

        """
        
            Visit a while node.
            
            Parameters:
                node (ASTWhileNode): The while node to visit.
                
        """

        # Visit the condition and block
        line = node.line_number
        condition_type = node.condition.accept(self)

        # Check if the type is compatible
        if condition_type != "bool":
            raise Exception("Invalid type for while condition on line ", line, ". Expected bool, got ", condition_type)
        
        node.block.accept(self)

    def visit_for_node(self, node):

        """
        
            Visit a for node.
            
            Parameters:
                node (ASTForNode): The for node to visit.
                
        """

        # Visit the start, end, and block
        line = node.line_number

        if (node.init is not None):
            start_type = node.init.accept(self)
        
            # Check if the types are compatible
            if start_type != "int":
                raise Exception("Invalid initialization type for for loop on line ", line, ". Expected int, got ", start_type)
            
        condition_type = node.condition.accept(self)

        # Check if the type is compatible
        if condition_type != "bool":
            raise Exception("Invalid condition type for for loop on line ", line, ". Expected bool, got ", condition_type)
        
        increment_type = node.increment.accept(self)

        # Check if the types are compatible
        if increment_type != "int":
            raise Exception("Invalid increment type for for loop on line ", line, ". Expected int, got ", increment_type)

        node.block.accept(self)

    def visit_return_node(self, node):
        
        """
        
            Visit a return node.
            
            Parameters:
                node (ASTReturnNode): The return node to visit.
                
        """

        # Visit the child
        line = node.line_number
        expr_type = node.expression.accept(self)
        
        # Check if the type is compatible
        if not self.symbol_table.is_function_scope():
            raise Exception("Return statement outside of function on line ", line)
        
        func_name = self.current_function_name

        self.returns = True

        if self.symbol_table.get_type(func_name) != expr_type:
            raise Exception("Type mismatch in return statement on line ", line, ". Expected ", self.symbol_table.get_type(func_name), ", got ", expr_type)
        
        return expr_type
       
# Testing the semantic analysis visitor
# Test the parser
src_program = "let x:int[] = [1, 2, 3];"

parser = Parser(src_program)
parser.Parse()
parser.ASTroot.accept(SemanticAnalysisVisitor())
print("Semantic analysis passed successfully!")