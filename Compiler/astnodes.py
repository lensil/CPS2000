# To do: should i have different nodes for each literal type???
# to do: add statement node and pass it accordingly
class ASTNode: 

    """

    Represents a generic AST node. All other AST nodes inherit from this class.
    
    """

    def __init__(self):
        self.name = "ASTNode"    

class ASTProgramNode(ASTNode): 
    
    """

    Represents a program node. It contains all the statements in the program and
    is the root of the AST generated for the program.
    
    """

    def __init__(self):
        self.name = "ASTProgramNode"
        self.statements = [] # Array of program statements

    def add_statement(self, statement):
        
        """
        
        Adds a statement to the array of statements in the program node.

        Parameters:
            statement (ASTNode): The statement to add to the program node.
        
        """
        self.statements.append(statement)

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_program_node method on the visitor.

        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        return visitor.visit_program_node(self)

class ASTExpressionNode(ASTNode):

    """
    
    Represents an expression node in the AST. It is the base class for all expression nodes.

    Parameters:
        type (str): The type of the expression node.
        line_number (int): The line number in the source code where the expression node is located.

    """

    def __init__(self, line_number):
        self.name = "ASTExpressionNode" 
        self.cast_expr = None
        self.line_number = line_number
 
    def add_type(self, type):

        """
        
        Adds a type for type casting to the expression node.

        Parameters:
            type (str): The type to add to the expression node.
        
        """
        
        self.cast_expr = type

class ASTLiteralNode(ASTExpressionNode):

    """
    
    Represents a literal node in the AST. It contains the type and value of the literal.

    Parameters:
        type (str): The type of the literal.
        val (str): The value of the literal.
        line_number (int): The line number in the source code where the literal node is located.
    
    """

    def __init__(self, type, val, line_number):
        self.name = "ASTLiteralNode"
        self.type = type
        self.val = val
        self.line_number = line_number   

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_literal_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """

        return visitor.visit_literal_node(self)

class ASTArrayDecNode(ASTExpressionNode):
    
    """
    
    Represents an array declaration node in the AST. It contains the type, name and size of the array.
    
    Parameters:
        size (int): The size of the array.
        array (list): The elements of the array.
        line_number (int): The line number in the source code where the array declaration node is located.
        name (str): The name of the array.
        type (str): The type of the array.

    """

    def __init__(self, size, array, line_number, name, type):
        self.name = "ASTArrayDecNode"
        self.size = size
        self.array = array
        self.line = line_number
        self.var_name = name
        self.var_type = type

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_array_dec_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_array_dec_node(self)

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_array_dec_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_array_dec_node(self)

class ASTVariableNode(ASTExpressionNode):
    
    """
        
    Represents a variable node in the AST. It contains the name of the variable.

    Parameters:
        name (str): The name of the variable.
        length (int): The length of the variable if it is an array.
        line_number (int): The line number in the source code where the variable node is located.
        
    """

    def __init__(self, name, length, line_number):
        self.name = "ASTVariableNode"
        self.var_name = name
        self.length = length
        self.line_number = line_number

    def accept (self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_variable_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        return visitor.visit_variable_node(self)

class ASTUnaryNode(ASTExpressionNode):
        
    """
        
    Represents a unary operation node in the AST. It contains the operand and the operator.

    Parameters: 
        operand: The operand of the unary operation.
        expression (ASTExpressionNode): The expression to apply the unary operation to.
        line_number (int): The line number in the source code where the unary node is located.
        
    """

    def __init__(self, operand, expression, line_number):
        self.name = "ASTUnaryNode"
        self.operand = operand
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_unary_node method on the visitor.
        
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """
            
        return visitor.visit_unary_op_node(self)

class ASTRandomNode(ASTExpressionNode):
        
    """
        
    Represents a random node in the AST. It contains the range of the random number.

    Parameters:
        expression (ASTExpressionNode): The expression containing the range of the random number.
        line_number (int): The line number in the source code where the random node is located.
        
    """

    def __init__(self, expression, line_number):
        self.name = "ASTRandomNode"
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_random_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
    
        """
    
        return visitor.visit_random_node(self)

class ASTReadNode(ASTExpressionNode):
            
    """
            
    Represents a read node in the AST. It contains the variable to read into.

    Parameters:
        left_expression (ASTExpressionNode): The expression containing the variable to read into.
        right_expression (ASTExpressionNode): The expression containing the prompt for the read statement.
        line_number (int): The line number in the source code where the read node is located.
            
    """
    
    def __init__(self, left_expression, right_expression, line_number):
        self.name = "ASTReadNode"
        self.left_expression = left_expression
        self.right_expression = right_expression
        self.line_number = line_number

    def accept(self, visitor):
                
        """
                
        Accepts a visitor and calls the visit_read_node method on the visitor.
        
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_read_node(self)

class ASTFunctionCallNode(ASTExpressionNode):

    """
    
    Represents a function call node in the AST. It contains the name of the function and its arguments.

    Parameters:
        function_name (str): The name of the function.
        parameters (list): The arguments of the function.
        line_number (int): The line number in the source code where the function call node is located.
    
    """
    
    def __init__(self, function_name, parameters, line_number):
        self.name = "ASTFunctionCallNode"
        self.function_name = function_name
        self.parameters = parameters
        self.line_number = line_number

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_function_call_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_function_call_node(self)

class ASTBinaryOpNode(ASTExpressionNode):

    """
    
    Represents a binary operation node in the AST. It contains the left and right operands

    Parameters:
        left (ASTExpressionNode): The left operand of the binary operation.
        right (ASTExpressionNode): The right operand of the binary operation.
        op (str): The operator of the binary operation.
        line_number (int): The line number in the source code where the binary operation node is located.
    
    """
    def __init__(self, left, right, op, line_number):
        self.name = "ASTBinaryOpNode"
        self.left = left
        self.right = right
        self.op = op
        self.line_number = line_number

    def accept(self, visitor):
            
        """
    
        Accepts a visitor and calls the visit_binary_op_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
    
        """
    
        return visitor.visit_binary_op_node(self)

class ASTVarDecNode(ASTNode):

    """

    Represents a variable declaration node in the AST. It contains the name, type and value of the variable.

    Parameters:
        var_name (str): The name of the variable.
        var_type (str): The type of the variable.
        var_expression (ASTExpressionNode): The value of the variable.
        line_number (int): The line number in the source code where the variable declaration node is located.
    
    """

    def __init__(self, var_name, var_type, var_expression, line_number):
        self.name = "ASTVarDecNode"
        self.var_name = var_name
        self.var_type = var_type
        self.var_expression = var_expression
        self.line_number = line_number

    def accept(self, visitor):

        """

        Accepts a visitor and calls the visit_var_dec_node method on the visitor.

        Parameters:
            visitor (ASTVisitor): The visitor to accept.

        """

        return visitor.visit_var_dec_node(self)

class ASTReturnNode(ASTNode):

    """
    
    Represents a return statement node in the AST. It contains the expression to return.

    Parameters:
        expression (ASTExpressionNode): The expression to return.
        line_number (int): The line number in the source code where the return node is located.
    
    """

    def __init__(self, expression, line_number):
        self.name = "ASTReturnNode"
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):
        
        """
    
        Accepts a visitor and calls the visit_return_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
    
        """
    
        return visitor.visit_return_node(self)

class ASTDelayNode(ASTNode):

    """
    
    Represents a delay statement node in the AST. It contains the expression representing the delay time.

    Parameters:
        expression (ASTExpressionNode): The expression representing the delay time.
        line_number (int): The line number in the source code where the delay node is located.
    
    """

    def __init__(self, expression, line_number):
        self.name = "ASTDelayNode"
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_delay_node method on the visitor.
        
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """
            
        return visitor.visit_delay_node(self)

class ASTWriteNode(ASTNode):

    """
    
    Represents a write statement node in the AST. It contains the expression to write.

    Parameters:
        expression_1 (ASTExpressionNode): The first expression to write.
        expression_2 (ASTExpressionNode): The second expression to write.
        expression_3 (ASTExpressionNode): The third expression to write.
        line_number (int): The line number in the source code where the write node is located.
    
    """

    def __init__(self, expression_1, expression_2, expression_3, line_number):
        self.name = "ASTWriteNode"
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        self.expression_3 = expression_3
        self.line_number = line_number


    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_write_node method on the visitor.
        
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """
            
        return visitor.visit_write_node(self)

class ASTWriteBoxNode(ASTNode):

    """
    
    Represents a write box statement node in the AST. It contains the expression to write.

    Parameters:
        expression_1 (ASTExpressionNode): The first expression to write.
        expression_2 (ASTExpressionNode): The second expression to write.
        expression_3 (ASTExpressionNode): The third expression to write.
        expression_4 (ASTExpressionNode): The fourth expression to write.
        expression_5 (ASTExpressionNode): The fifth expression to write.
        line_number (int): The line number in the source code where the write box node is located.
    
    """

    def __init__(self, expression_1, expression_2, expression_3, expression_4, expression_5, line_number):
        self.name = "ASTWriteBoxNode"
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        self.expression_3 = expression_3
        self.expression_4 = expression_4
        self.expression_5 = expression_5
        self.line_number = line_number

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_write_box_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_write_box_node(self)

class ASTPrintNode(ASTNode):

    """
    
    Represents a print statement node in the AST. It contains the expression to print.

    Parameters:
        expression (ASTExpressionNode): The expression to print.
        line_number (int): The line number in the source code where the print node is located.
    
    """

    def __init__(self, expression, line_number):
        self.name = "ASTPrintNode"
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_print_node method on the visitor.
        
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """
            
        return visitor.visit_print_node(self)

class ASTFormalParameterNode(ASTNode):

    """
    
    Represents a formal parameter node in the AST. It contains the name and type of the parameter.

    Parameters:
        name (str): The name of the parameter.
        type (str): The type of the parameter.
        line_number (int): The line number in the source code where the formal parameter node is located.
    
    """

    def __init__(self, name, type, line_number):
        self.name = "ASTFormalParameterNode"
        self.var_name = name
        self.type = type
        self.line_number = line_number

    def accept(self, visitor):
        
        """
        
        Accepts a visitor and calls the visit_formal_parameter_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_formal_parameter_node(self)

class ASTFunctionNode(ASTNode):

    """
    
    Represents a function node in the AST. It contains the name, return type, parameters and body of the function.

    Parameters:
        name (str): The name of the function.
        parameters (list): The parameters of the function.
        return_type (str): The return type of the function.
        body (ASTNode): The body of the function.
        line_number (int): The line number in the source code where the function node is located.
    
    """

    def __init__(self, name, parameters, return_type, body, line_number):
        self.name = "ASTFunctionNode"
        self.func_name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.line_number = line_number

    def accept(self, visitor):

        """
        
        Accepts a visitor and calls the visit_function_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_function_node(self)

class ASTBlockNode(ASTNode):
    
    """
        
    Represents a block node in the AST. It contains a list of statements.
    
    Parameters:
        statements (list): The statements in the block.
        line_number (int): The line number in the source code where the block node is located.
        
    """
    
    def __init__(self, statements, line_number):
        self.name = "ASTBlockNode"
        self.statements = statements
        self.line_number = line_number

    def add_statement(self, statement):
            
        """
            
        Adds a statement to the list of statements in the block node.
    
        Parameters:
            statement (ASTNode): The statement to add to the block node.
            
        """
        
        self.statements.append(statement)

    def accept(self, visitor):
            
        """
            
        Accepts a visitor and calls the visit_block_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
            
        """

        return visitor.visit_block_node(self)

class ASTAssignmentNode(ASTNode):

    """
    Represents an assignment node in the AST. It contains the identifier and the expression to assign to it.

    Parameters:
        identifier (str): The identifier to assign to.
        expression (ASTExpressionNode): The expression to assign to the identifier.
        line_number (int): The line number in the source code where the assignment node is located.

    """

    def __init__(self, identifier, expression, line_number):
        self.name = "ASTAssignmentNode"
        self.identifier = identifier
        self.expression = expression
        self.line_number = line_number

    def accept(self, visitor):

        """

        Accepts a visitor and calls the visit_assignment_node method on the visitor.

        Parameters:
            visitor (ASTVisitor): The visitor to accept.

        """

        return visitor.visit_assignment_node(self)

class ASTIfNode(ASTNode):

    """
    
    Represents an if statement node in the AST. It contains the condition, true block and optional false block.

    Parameters:
        condition (ASTExpressionNode): The condition of the if statement.
        true_block (ASTBlockNode): The block to execute if the condition is true.
        false_block (ASTBlockNode): The block to execute if the condition is false.
        line_number (int): The line number in the source code where the if node is located.
    
    """

    def __init__(self, condition, true_block, false_block, line_number):
        self.name = "ASTIfNode"
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
        self.line_number = line_number

    def accept(self, visitor):

        """
        
        Accepts a visitor and calls the visit_if_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_if_node(self)

class ASTWhileNode(ASTNode):
    
    """

    Represents a while statement node in the AST. It contains the condition and the block to execute.

    Parameters:
        condition (ASTExpressionNode): The condition of the while statement.
        block (ASTBlockNode): The block to execute while the condition is true.
        line_number (int): The line number in the source code where the while node is located.
    
    """

    def __init__(self, condition, block, line_number):
        self.name = "ASTWhileNode"
        self.condition = condition
        self.block = block
        self.line_number = line_number

    def accept(self, visitor):

        """
        
        Accepts a visitor and calls the visit_while_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_while_node(self)

class ASTForNode(ASTNode):

    """
    
    Represents a for statement node in the AST. It contains the initial value, condition, increment and block to execute.
    
    Parameters:
        init (ASTNode): The initial value of the for loop.
        condition (ASTExpressionNode): The condition of the for loop.
        increment (ASTNode): The increment of the for loop.
        block (ASTBlockNode): The block to execute in the for loop.
        line_number (int): The line number in the source code where the for node is located.
    
    """

    def __init__(self, init, condition, increment, block, line_number):
        self.name = "ASTForNode"
        self.init = init
        self.condition = condition
        self.increment = increment
        self.block = block
        self.line_number = line_number

    def accept(self, visitor):

        """
        
        Accepts a visitor and calls the visit_for_node method on the visitor.
    
        Parameters:
            visitor (ASTVisitor): The visitor to accept.
        
        """
        
        return visitor.visit_for_node(self)