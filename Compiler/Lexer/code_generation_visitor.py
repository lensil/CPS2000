from visitor import ASTVisitor
from symbol_table import SymbolTable, ScopeType, Symbol, SymbolType
from parser_testing import *

class CodeGenerationVisitor(ASTVisitor):

    def __init__(self, output_file):
        self.symbol_table = SymbolTable() # Symbol table
        self.current_function_name = None # Current function name being visited
        self.returns = False # Flag to check if function returns a value
        self.output_file = open(output_file, "w") # Output file of where the generated code will be written
        self.output_string = "" # Output string where the generated code will be written
        self.current_block_length = 0 # Length of the current block
    # Done
    def visit_program_node(self, node):
        self.output_file.write(".main\n") # Write the main function header
        self.output_file.write("push 4\n") # Call the main function
        self.output_file.write("jmp\n") 
        self.output_file.write("halt\n") 
        self.output_file.write("push " + str(len(node.statements)) + "\n") # Push the number of statements onto the stack
        self.output_file.write("oframe\n") # Open the frame
        for statement in node.statements:
            statement.accept(self)

        self.output_file.close() # Close the output file
    
    # Done
    def visit_block_node(self, node):
        self.output_file.write("push " + str(len(node.statements)) + "\n") # Push the number of statements onto the stack
        self.output_file.write("oframe\n") # Open the frame
        
        if not self.symbol_table.is_function_scope():
            self.symbol_table.push_scope(ScopeType.BLOCK) 

        for statement in node.statements:
            statement.accept(self)

        if not self.symbol_table.is_function_scope():
            self.symbol_table.pop_scope()

        self.output_file.write("cframe\n") # Close the frame
        self.current_block_length += 3

    # Done
    def visit_literal_node(self, node):

        self.current_block_length += 1

        if node.type == TokenType.INT_LITERAL or node.type == TokenType.FLOAT_LITERAL or node.type == TokenType.COLOR_LITERAL:
            self.output_file.write("push " + str(node.val) + "\n") # Push the literal value onto the stack
        elif node.type == TokenType.BOOL_LITERAL:
            if node.val == "true":
                self.output_file.write("push 1\n")
            else:
                self.output_file.write("push 0\n")

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

    # Done
    def visit_binary_op_node(self, node):

        operator = node.op
        line = node.line_number
        right_type = node.right.accept(self)
        left_type = node.left.accept(self)

        if left_type != right_type:
            raise Exception("Type mismatch in binary operation on line ", line, ". Expected ", left_type, ", got ", right_type)

        # Mathematical operations
        if operator in ['+', '-', '*', '/']:
            if left_type != "int" and left_type != "float":
                raise Exception("Invalid type for arithmetic operation on line ", line, ". Expected int or float, got ", left_type)
            if operator == '+':
                self.output_file.write("add\n")
            elif operator == '-':
                self.output_file.write("sub\n")
            elif operator == '*':
                self.output_file.write("mul\n")
            elif operator == '/':
                self.output_file.write("div\n")
            return left_type
    
        

        if not node.cast_expr is None:
            return node.cast_expr

        # Comparison operations
        if operator in ['<', '>', '<=', '>=']:
            if left_type != "int" and left_type != "float":
                raise Exception("Invalid type for comparison operation on line ", line, ". Expected int or float, got ", left_type)
            if operator == '<':
                self.output_file.write("lt\n")
            elif operator == '>':
                self.output_file.write("gt\n")
            elif operator == '<=':
                self.output_file.write("le\n")
            elif operator == '>=':
                self.output_file.write("ge\n")
            return "bool"
        

        if operator in ['==', '!=']:
            if operator == '==':
                self.output_file.write("eq\n")
            elif operator == '!=':
                self.output_file.write("eq\n")
                self.output_file.write("not\n")
            return "bool"
        

        if operator in ['and', 'or']:
            if left_type != "bool":
                raise Exception("Invalid type for logical operation on line ", line, ". Expected bool, got ", left_type)
            if operator == 'and':
                self.output_file.write("and\n")
            elif operator == 'or':
                self.output_file.write("or\n")
            return "bool"

        return left_type

    # Done
    def visit_unary_op_node(self, node):

        line = node.line_number
        expr_type = node.expression.accept(self)

        self.output_file.write("not\n")

        if expr_type != "bool":
            raise Exception("Invalid type for unary operation on line ", line)

        return expr_type

    def visit_assignment_node(self, node):

        identifier_type = self.visit_variable_node(node.identifier)

        expression_type = node.expression.accept(self)

        if identifier_type != expression_type:
            raise Exception("Type mismatch in assignment on line ", node.line_number, ". Expected ", identifier_type, ", got ", expression_type)

        return identifier_type

    # Done
    def visit_variable_node(self, node):

        if self.current_function_name is not None:
            parameters = self.symbol_table.get_params(self.current_function_name)
            for param in parameters:
                if param["name"] == node.var_name:
                    return param["type"]
                else:
                    raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)

        var_type = self.symbol_table.get_type(node.var_name)

        if var_type is None:
            raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)
        symbol = self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type)
        self.output_file.write("push [" + str(symbol.frame_index) + ":" + str(self.symbol_table.current_frame_level - symbol.frame_level) + "]\n")
        return var_type

    # Done
    def visit_var_dec_node(self, node):

        name = node.var_name.var_name 
        line = node.line_number
        type = node.var_type.value
        expr_type = node.var_expression.accept(self)

        if self.current_function_name is not None:
            parameters = self.symbol_table.get_params(self.current_function_name)
            for param in parameters:
                if param["name"] == name:
                    raise Exception("Variable name clashes with parameter name on line ", line, ": ", name)

        self.output_file.write("push " + str(self.symbol_table.current_frame_index ) + "\n")
        self.output_file.write("push " + str(0) + "\n")
        self.output_file.write("st\n")
        if self.symbol_table.is_declared(name):
            raise Exception("Identifier already declared on line ", line, ": ", name)
        

        if type != expr_type:
            raise Exception("Type mismatch in declaration on line ", line, ". Expected ", type, ", got ", expr_type)
        symbol = Symbol(SymbolType.VARIABLE, line, type, name)
        self.symbol_table.add_symbol(name, symbol)

        return type

    # Done
    def visit_random_node(self, node):

        line = node.line_number
        expr_type = node.expression.accept(self)

        if expr_type != "int":
            raise Exception("Invalid type for random operation on line ", line)
        
        self.output_file.write("irnd\n")

        return expr_type

    # Done
    def visit_delay_node(self, node):

        line = node.line_number
        expr_type = node.expression.accept(self)

        if expr_type != "int" and expr_type != "float":
            raise Exception("Invalid type for delay operation on line ", line, ". Expected int or float, got ", expr_type)
        
        self.output_file.write("delay\n")

        return expr_type

    # Done
    def visit_write_node(self, node):

        line = node.line_number
        expr3_type = node.expression_3.accept(self)
        expr2_type = node.expression_2.accept(self)
        expr1_type = node.expression_1.accept(self)
        

        if expr1_type != "int":
            raise Exception("Expected int for first argument of write on line ", line, ", got ", expr1_type)

        if expr2_type != "int":
            raise Exception("Expected int for second argument of write on line ", line, ", got ", expr2_type)

        if expr3_type != "color":
            raise Exception("Expected color for third argument of write on line ", line, ", got ", expr3_type)
        
        self.output_file.write("write\n")

        return expr1_type

    # Done
    def visit_write_box_node(self, node):

        line = node.line_number
        expr5_type = node.expression_5.accept(self)
        expr4_type = node.expression_4.accept(self)
        expr3_type = node.expression_3.accept(self)
        expr2_type = node.expression_2.accept(self)
        expr1_type = node.expression_1.accept(self)

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
        
        self.output_file.write("writebox\n")
        
        return expr1_type

    def visit_read_node(self, node):

        line = node.line_number
        expr_type_left = node.left_expression.accept(self)
        expr_type_right = node.right_expression.accept(self)

        if expr_type_left != "int":
            raise Exception("Expected int for left argument of read on line ", line, ", got ", expr_type_left)

        if expr_type_right != "int":
            raise Exception("Expected int for right argument of read on line ", line, ", got ", expr_type_right)

        return expr_type_left

    def visit_function_call_node(self, node):

        function_name = node.function_name 
        line = node.line_number
        parameters = node.parameters

        if not self.symbol_table.is_declared(function_name):
            raise Exception("Function not declared on line ", line, ": ", function_name)

        function_symbol = self.symbol_table.lookup(function_name, self.symbol_table.get_current_scope_type)

        if len(parameters) != len(function_symbol.params):
            raise Exception("Number of parameters do not match in function call on line ", line, ". Expected ", len(function_symbol.params), ", got ", len(parameters))

        for i in range(len(parameters)):
            param_type = parameters[i].accept(self)
            if param_type != function_symbol.params[i]["type"]:
                raise Exception("Type mismatch in function call on line ", line, ". Expected ", function_symbol.params[i]["type"], ", got ", param_type)

        return function_symbol.type

    def visit_function_node(self, node):

        name = node.func_name.value
        func_parameters = []

        for param in node.parameters:
            parameter = param.accept(self)
            if (parameter["name"], parameter["type"]) in func_parameters:
                raise Exception("Duplicate parameter in function declaration on line ", node.line_number, ": ", parameter["name"])
            func_parameters.append(parameter)

        return_type = node.return_type.value

        if self.symbol_table.is_declared(name):
            raise Exception("Function already declared on line ", node.line_number, ": ", name)

        if self.symbol_table.is_function_scope():
            raise Exception("Function declaration inside a function on line ", node.line_number, ": ", name)

        symbol = Symbol(SymbolType.FUNCTION, node.line_number, return_type, name, func_parameters)

        self.symbol_table.add_symbol(name, symbol)

        self.symbol_table.push_scope(ScopeType.FUNCTION)
        self.current_function_name = name
        node.body.accept(self)

        if not self.returns:
            raise Exception("Function does not return a value on line ", node.line_number, ": ", name)

        self.current_function_name = None
        self.symbol_table.pop_scope()

    def visit_formal_parameter_node(self, node):

        name = node.var_name.value
        type = node.type.value

        return {"name": name, "type": type}

    # Done
    def visit_print_node(self, node):

        line = node.line_number
        expr_type = node.expression.accept(self)

        if expr_type != "int" and expr_type != "float" and expr_type != "bool" and expr_type != "color":
            raise Exception("Invalid type for print operation on line ", line)
        
        self.output_file.write("print\n")

        self.current_block_length += 1

        return expr_type

    def visit_if_node(self, node):
        if self.current_function_name is not None:
            self.returns = False

        line = node.line_number
        condition_type = node.condition.accept(self)

        if condition_type != "bool":
            raise Exception("Invalid type for if condition on line ", line, ". Expected bool, got ", condition_type)

        
        # First pass: Write the lines that you can, leaving placeholders for the others
        current_position = self.output_file.tell()
        self.output_file.write("push #PC+00000000000000000\n")  # Placeholder
        self.output_file.write("cjmp \n")
        node.true_block.accept(self)

# Calculate self.current_block_length here

# Second pass: Replace the placeholder with the actual line
        self.output_file.seek(current_position)
        self.output_file.write("push #PC+" + str(self.current_block_length).zfill(17) + "\n")  # Make sure the length of the string is 17

# Move the file pointer to the end
        self.output_file.seek(0, 2)


        if self.current_function_name is not None and not self.returns:
            raise Exception("Function does not return a value on line ", line, ": ", self.current_function_name)

        if not node.false_block is None:
            if self.current_function_name is not None:
                self.returns = False
            self.output_file.write("push #PC+" + str(len(node.false_block.statements) + 1) + "\n")
            self.output_file.write("jmp\n")
            node.false_block.accept(self)

        return condition_type

    def visit_while_node(self, node):

        line = node.line_number
        condition_type = node.condition.accept(self)

        if condition_type != "bool":
            raise Exception("Invalid type for while condition on line ", line, ". Expected bool, got ", condition_type)

        node.block.accept(self)

    def visit_for_node(self, node):

        line = node.line_number

        if (node.init is not None):
            start_type = node.init.accept(self)

            if start_type != "int":
                raise Exception("Invalid initialization type for for loop on line ", line, ". Expected int, got ", start_type)

        condition_type = node.condition.accept(self)

        if condition_type != "bool":
            raise Exception("Invalid condition type for for loop on line ", line, ". Expected bool, got ", condition_type)

        increment_type = node.increment.accept(self)

        if increment_type != "int":
            raise Exception("Invalid increment type for for loop on line ", line, ". Expected int, got ", increment_type)

        node.block.accept(self)

    def visit_return_node(self, node):

        line = node.line_number
        expr_type = node.expression.accept(self)

        if not self.symbol_table.is_function_scope():
            raise Exception("Return statement outside of function on line ", line)

        func_name = self.current_function_name

        self.returns = True

        if self.symbol_table.get_type(func_name) != expr_type:
            raise Exception("Type mismatch in return statement on line ", line, ". Expected ", self.symbol_table.get_type(func_name), ", got ", expr_type)

        return expr_type

src_program = "if (1 > 5) { __print 9; __print 9; __print 9;}"

parser = Parser(src_program)
parser.Parse()
parser.ASTroot.accept(CodeGenerationVisitor(output_file="output.txt"))
print("Semantic analysis passed successfully!")