# To do: should i have different nodes for each literal type???
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

class ASTExpressionNode(ASTNode):

    """
    
    Represents an expression node in the AST. It is the base class for all expression nodes.

    Parameters:
        type (str): The type of the expression node.
        line_number (int): The line number in the source code where the expression node is located.

    """

    def __init__(self, line_number):
        self.name = "ASTExpressionNode" 
        self.type = None
        self.line_number = line_number

    def add_type(self, type):

        """
        
        Adds a type for type casting to the expression node.

        Parameters:
            type (str): The type to add to the expression node.
        
        """
        self.type = type


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

class ASTVariableNode(ASTExpressionNode):
    
    """
        
    Represents a variable node in the AST. It contains the name of the variable.

    Parameters:
        name (str): The name of the variable.
        line_number (int): The line number in the source code where the variable node is located.
        
    """

    def __init__(self, name, line_number):
        self.name = "ASTVariableNode"
        self.var_name = name
        self.line_number = line_number

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


class ASTBinaryOpNode(ASTNode):

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
        self.val_expression = var_expression
        self.line_number = line_number

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
        self.expression_1 = expression_1,
        self.expression_2 = expression_2
        self.expression_3 = expression_3
        self.line_number = line_number

class ASTWriteBoxNode(ASTNode):

    """
    
    Represents a write box statement node in the AST. It contains the expression to write.

    Parameters:
        expression_1 (ASTExpressionNode): The first expression to write.
        expression_2 (ASTExpressionNode): The second expression to write.
        expression_3 (ASTExpressionNode): The third expression to write.
        expression_4 (ASTExpressionNode): The fourth expression to write.
        line_number (int): The line number in the source code where the write box node is located.
    
    """

    def __init__(self, expression_1, expression_2, expression_3, expression_4, line_number):
        self.name = "ASTWriteBoxNode"
        self.expression_1 = expression_1
        self.expression_2 = expression_2
        self.expression_3 = expression_3
        self.expression_4 = expression_4
        self.line_number = line_number

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
        self.name = name
        self.type = type
        self.line_number = line_number

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
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.line_number = line_number