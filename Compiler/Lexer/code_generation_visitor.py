from visitor import ASTVisitor
from symbol_table import SymbolTable, ScopeType, Symbol, SymbolType
from parser_testing import *
from astnodes import *
# To do: increase size of frame if needed

class CodeGenerationVisitor(ASTVisitor):

    def __init__(self, output_file):
        self.symbol_table = SymbolTable() # Symbol table
        self.current_function_name = None # Current function name being visited
        self.returns = False # Flag to check if function returns a value
        self.output_file = open(output_file, "w") # Output file of where the generated code will be written
        self.output = [] # List of strings to be written to the output file
        self.current_block_length = 0 # Length of the current block
    
    # Done
    def visit_program_node(self, node):
        self.output.append(".main\n") 
        self.output.append("push 4\n")
        self.output.append("jmp\n")
        self.output.append("halt\n")
        self.output.append("push " + str(len(node.statements)) + "\n")
        self.output.append("oframe\n")
        for statement in node.statements:
            statement.accept(self)

        for line in self.output:
            self.output_file.write(line)

        self.output_file.close() # Close the output file
    
    # Done
    def visit_block_node(self, node):
 
        self.output.append("push " + str(len(node.statements)) + "\n") # Push the number of statements onto the stack
        self.output.append("oframe\n") # Open the frame

        self.current_block_length += 2
    
        self.symbol_table.push_scope(ScopeType.BLOCK) 


        for statement in node.statements:
            statement.accept(self)          

        if not self.symbol_table.is_function_scope():
            self.symbol_table.pop_scope()
        else:
            self.symbol_table.current_frame_level -= 1

        self.output.append("cframe\n") # Close the frame
        self.current_block_length += 1

    # Done
    def visit_literal_node(self, node):

        self.current_block_length += 1

        if node.type == TokenType.INT_LITERAL or node.type == TokenType.FLOAT_LITERAL or node.type == TokenType.COLOR_LITERAL:
            self.output.append("push " + str(node.val) + "\n") # Push the literal value onto the stack
        elif node.type == TokenType.BOOL_LITERAL:
            if node.val == "true":
                self.output.append("push 1\n")
            else:
                self.output.append("push 0\n")

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

        self.current_block_length += 1

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
                self.output.append("add\n")
            elif operator == '-':
                self.output.append("sub\n")
            elif operator == '*':
                self.output.append("mul\n")
            elif operator == '/':
                self.output.append("div\n")
            return left_type
    
        

        if not node.cast_expr is None:
            return node.cast_expr

        # Comparison operations
        if operator in ['<', '>', '<=', '>=']:
            if left_type != "int" and left_type != "float":
                raise Exception("Invalid type for comparison operation on line ", line, ". Expected int or float, got ", left_type)
            if operator == '<':
                self.output.append("lt\n")
            elif operator == '>':
                self.output.append("gt\n")
            elif operator == '<=':
                self.output.append("le\n")
            elif operator == '>=':
                self.output.append("ge\n")
            return "bool"
        

        if operator in ['==', '!=']:
            if operator == '==':
                self.output.append("eq\n")
            elif operator == '!=':
                self.output.append("eq\n")
                self.output.append("not\n")
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

        self.output.append("not\n")

        if expr_type != "bool":
            raise Exception("Invalid type for unary operation on line ", line)
        
        self.current_block_length += 1

        return expr_type

    # Done
    def visit_assignment_node(self, node):

        identifier_type = self.visit_variable_node(node.identifier)

        expression_type = node.expression.accept(self)

        symbol = self.symbol_table.lookup(node.identifier.var_name, self.symbol_table.get_current_scope_type)

        self.output.append("push "+ str(symbol.frame_index) + "\n")
        self.output.append("push "+ str(self.symbol_table.current_frame_level - symbol.frame_level) + "\n")
        self.output.append("st\n")

        self.current_block_length += 3

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
            if self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type()) is None:
                raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)
            symbol = self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type())
            self.output.append("push [" + str(symbol.frame_index) + ":" + str(self.symbol_table.current_frame_level - symbol.frame_level) + "]\n")
            self.current_block_length += 1
            return self.symbol_table.get_type(node.var_name)

        var_type = self.symbol_table.get_type(node.var_name)

        self.current_block_length += 1

        if var_type is None:
            raise Exception("Undeclared identifier on line ", node.line_number, ": ", node.var_name)
        symbol = self.symbol_table.lookup(node.var_name, self.symbol_table.get_current_scope_type())
        self.output.append("push [" + str(symbol.frame_index) + ":" + str(self.symbol_table.current_frame_level - symbol.frame_level) + "]\n")
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
            symbol = self.symbol_table.lookup(name, self.symbol_table.get_current_scope_type())
            if self.symbol_table.lookup(name, self.symbol_table.get_current_scope_type()) is None:
                self.output.append("push " + str(self.symbol_table.current_frame_index) + "\n")
                self.output.append("push " + str(0)  + "\n")
                self.output.append("st\n")
                symbol = Symbol(SymbolType.VARIABLE, line, type, name, self.symbol_table.current_frame_index, self.symbol_table.current_frame_level)
                self.symbol_table.add_symbol(name, symbol)
                self.current_block_length += 3
                return type
            else:
                raise Exception("Identifier already declared on line ", line, ": ", name)

        self.output.append("push " + str(self.symbol_table.current_frame_index ) + "\n")
        self.output.append("push " + str(0) + "\n")
        self.output.append("st\n")
        if self.symbol_table.is_declared(name):
            raise Exception("Identifier already declared on line ", line, ": ", name)
        

        if type != expr_type:
            raise Exception("Type mismatch in declaration on line ", line, ". Expected ", type, ", got ", expr_type)
        symbol = Symbol(SymbolType.VARIABLE, line, type, name)
        self.symbol_table.add_symbol(name, symbol)

        self.current_block_length += 3

        return type

    # Done
    def visit_random_node(self, node):

        self.current_block_length += 1

        line = node.line_number
        expr_type = node.expression.accept(self)

        if expr_type != "int":
            raise Exception("Invalid type for random operation on line ", line)
        
        self.output.append("irnd\n")

        return expr_type

    # Done
    def visit_delay_node(self, node):

        self.current_block_length += 1

        line = node.line_number
        expr_type = node.expression.accept(self)

        if expr_type != "int" and expr_type != "float":
            raise Exception("Invalid type for delay operation on line ", line, ". Expected int or float, got ", expr_type)
        
        self.output.append("delay\n")

        return expr_type

    # Done
    def visit_write_node(self, node):

        self.current_block_length += 1

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
        
        self.output.append("write\n")

        return expr1_type

    # Done
    def visit_write_box_node(self, node):

        self.current_block_length += 1

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
        
        self.output.append("write_box\n")
        
        return expr1_type

    # Done
    def visit_read_node(self, node):

        line = node.line_number
        expr_type_right = node.right_expression.accept(self)
        expr_type_left = node.left_expression.accept(self)

        if expr_type_left != "int":
            raise Exception("Expected int for left argument of read on line ", line, ", got ", expr_type_left)

        if expr_type_right != "int":
            raise Exception("Expected int for right argument of read on line ", line, ", got ", expr_type_right)
        
        self.output.append("read\n")

        return expr_type_left

    # Done
    def visit_function_call_node(self, node):

        function_name = node.function_name 
        line = node.line_number
        parameters = node.parameters

        self.current_block_length += 3

        #self.output.append("push " + (str(len(node.parameters)))+ "\n") 
        self.output.append("push ." + function_name + "\n")
        self.output.append("call\n")

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

    # Done
    def visit_function_node(self, node):

        self.current_block_length = 0

        self.output.append("push #PC+00000000000000000\n") # Placeholder
        index = len(self.output) - 1
        self.output.append("jmp\n")

        name = node.func_name.value
        func_parameters = []

        for param in node.parameters:
            parameter = param.accept(self)
            if (parameter["name"], parameter["type"]) in func_parameters:
                raise Exception("Duplicate parameter in function declaration on line ", node.line_number, ": ", parameter["name"])
            func_parameters.append(parameter)

        self.output.append("." + name + "\n") # Function name

        self.current_block_length += 3
        function_index = len(self.output) - 1 # Index/line of the function in the output list

        return_type = node.return_type.value

        if self.symbol_table.is_declared(name):
            raise Exception("Function already declared on line ", node.line_number, ": ", name)

        if self.symbol_table.is_function_scope():
            raise Exception("Function declaration inside a function on line ", node.line_number, ": ", name)

        symbol = Symbol(SymbolType.FUNCTION, node.line_number, return_type, name, func_parameters)

        symbol.add_function_line(function_index) # Add the line where the function is declared

        self.symbol_table.add_symbol(name, symbol)

        self.symbol_table.push_scope(ScopeType.FUNCTION)
        self.current_function_name = name
        node.body.accept(self)

        if not self.returns:
            raise Exception("Function does not return a value on line ", node.line_number, ": ", name)
        
        if isinstance(node.body.statements[-1], ASTIfNode):
                if not isinstance(node.body.statements[-1].true_block.statements[-1], ASTReturnNode):
                    raise Exception("Function does not end with a return a value on line ", node.line_number, ": ", self.current_function_name)
                if not node.body.statements[-1].false_block is None:
                    if not isinstance(node.body.statements[-1].false_block.statements[-1], ASTReturnNode):
                        raise Exception("Function does not end with a return a value on line ", node.line_number, ": ", self.current_function_name)
                    self.output.append("ret\n") # Add return statement to the end of the function
                    self.current_block_length += 5
                else:
                    raise Exception("Function does not end with a return a value on line ", node.line_number, ": ", self.current_function_name)
        elif not isinstance(node.body.statements[-1], ASTReturnNode):
                raise Exception("Function does not end with a return a value on line ", node.line_number, ": ", self.current_function_name)
        elif isinstance(node.body.statements[-1], ASTReturnNode) and len(node.body.statements) > 1:
                if isinstance(node.body.statements[-2], ASTIfNode):
                    self.current_block_length += 0
        
        self.returns = False # Reset the returns flag

        self.output[index] = "push #PC+" + str(self.current_block_length) + "\n"

        # Swap return statement and cframe
        return_statement = self.output[len(self.output) - 1]
        cframe = self.output[len(self.output) - 2]
        self.output[len(self.output) - 1] = cframe
        self.output[len(self.output) - 2] = return_statement



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
        
        self.output.append("print\n")

        self.current_block_length += 1

        return expr_type

    # Done
    def visit_if_node(self, node):

        block_length_before = self.current_block_length

        self.current_block_length = 0

        if self.current_function_name is not None:
            self.returns = False

        # Visit the condition and block
        line = node.line_number
        condition_type = node.condition.accept(self)

        self.output.append("push #PC+4\n")  
        self.output.append("cjmp\n") # Enter the if block
        self.output.append("push #PC+00000000000000000\n") # Placeholder
        index = len(self.output) - 1
        self.output.append("jmp\n")  # Exit the if block

        self.current_block_length += 4
    
        # Check if the type is compatible
        if condition_type != "bool":
            raise Exception("Invalid type for if condition on line ", line, ". Expected bool, got ", condition_type)
        
        node.true_block.accept(self)

        self.output[index] = "push #PC+" + str(self.current_block_length-3) + "\n" # Jump to the end of the if block

        if not node.false_block is None:
            block_length = self.current_block_length
            self.output[index] = "push #PC+" + str(self.current_block_length) + "\n" # Jump to the end of the if block
            self.output.append("push #PC+00000000000000000\n") # Placeholder
            index = len(self.output) - 1
            self.output.append("jmp\n")  # Exit the if block
            self.current_block_length += 2
            if self.current_function_name is not None:
                self.returns = False
            node.false_block.accept(self)
            self.output[index] = "push #PC+" + str(self.current_block_length-block_length) + "\n" # Jump to the end of the else block

        if self.current_function_name is not None:
            self.current_block_length += block_length_before

        return condition_type

    # Done
    def visit_while_node(self, node):

        self.current_block_length = 0

        line = node.line_number

        condition_type = node.condition.accept(self)

        self.output.append("push #PC+4\n")  
        self.output.append("cjmp\n") # Enter the loop
        self.output.append("push #PC+00000000000000000\n") # Placeholder
        index = len(self.output) - 1
        self.output.append("jmp\n")  # Exit the loop

        self.current_block_length += 4

        if condition_type != "bool":
            raise Exception("Invalid type for while condition on line ", line, ". Expected bool, got ", condition_type)

        node.block.accept(self)

        self.output[index] = "push #PC+" + str(self.current_block_length) + "\n" # Jump to the condition

        self.output.append("push #PC-" + str(self.current_block_length) + "\n") # Jump to the condition
        self.output.append("jmp\n") # Jump to the condition

        self.current_block_length = 0

    # Done
    def visit_for_node(self, node):

        self.current_block_length = 0

        line = node.line_number

        if (node.init is not None):
            start_type = node.init.accept(self)

            if start_type != "int":
                raise Exception("Invalid initialization type for for loop on line ", line, ". Expected int, got ", start_type)
        
        self.current_block_length = 0

        condition_type = node.condition.accept(self)

        self.output.append("push #PC+4\n")  
        self.output.append("cjmp\n") # Enter the loop
        self.output.append("push #PC+00000000000000000\n") # Placeholder
        index = len(self.output) - 1
        self.output.append("jmp\n")  # Exit the loop

        self.current_block_length += 4

        if condition_type != "bool":
            raise Exception("Invalid condition type for for loop on line ", line, ". Expected bool, got ", condition_type)

        node.block.accept(self) # Execute the for loop block

        self.output[index] = "push #PC+" + str(self.current_block_length) + "\n" # Jump to the condition

        increment_type = node.increment.accept(self)

        self.output.append("push #PC-" + str(self.current_block_length) + "\n") # Jump to the condition
        self.output.append("jmp\n") # Jump to the condition

        if increment_type != "int": # Evaluate the expression
            raise Exception("Invalid increment type for for loop on line ", line, ". Expected int, got ", increment_type)
        
        self.current_block_length = 0

    # Done
    def visit_return_node(self, node):

        self.current_block_length += 1

        line = node.line_number
        expr_type = node.expression.accept(self)
        self.output.append("ret\n")

        if not self.symbol_table.is_function_scope():
            raise Exception("Return statement outside of function on line ", line)

        func_name = self.current_function_name

        self.returns = True

        if self.symbol_table.get_type(func_name) != expr_type:
            raise Exception("Type mismatch in return statement on line ", line, ". Expected ", self.symbol_table.get_type(func_name), ", got ", expr_type)

        return expr_type

src_program = "let x:int = 0; fun test(x: int) -> int { __print x; return x+2; } __print x; x = test(5); __print x;"
parser = Parser(src_program)
parser.Parse()
parser.ASTroot.accept(CodeGenerationVisitor(output_file="output.txt"))