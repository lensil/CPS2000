import lexer
import astnodes as ast
from tokens import TokenType

# To do:  lexer check for EOF taken and make work with empty string
class Parser:
    def __init__(self, src_program_str):
        self.lexer = lexer.Lexer()
        self.index = -1  
        self.src_program = src_program_str
        self.tokens = self.lexer.generate_tokens(self.src_program)
        self.crtToken = lexer.Token("", lexer.TokenType.ERROR, -1)
        self.nextToken = lexer.Token("", lexer.TokenType.ERROR, -1)
        self.ASTroot = ast.ASTProgramNode() 

    def parse_statement(self):

        """
    
        Parse a statement
    
        Returns:
            ASTNode: A statement node
        
        """

        match self.crtToken.TokenType:
            case TokenType.LET:
                return self.parse_variable_declartion()
            case TokenType.IDENTIFIER if self.nextToken.TokenType == TokenType.ASSIGNMENT_OP or self.nextToken.TokenType == TokenType.LEFT_SQ_BRACK:
                return self.parse_assignment_statement()
            case TokenType.PRINT:
                return self.parse_print_statement()
            case TokenType.DELAY:
                return self.parse_delay_statement()
            case TokenType.WRITE | TokenType.WRITE_BOX:
                return self.parse_write_statement()
            case TokenType.IF:
                return self.parse_if_statement()
            case TokenType.FOR:
                return self.parse_for_statement()
            case TokenType.WHILE:
                return self.parse_while_statement()
            case TokenType.RETURN:
                return self.parse_return_statement()
            case TokenType.FUN:
                return self.parse_function_declaration()
            case TokenType.LEFT_BRACE:
                return self.parse_block()
            case _:
                raise Exception("Invalid statement on line ", self.crtToken.line)
    
    def parse_variable_declartion(self):

        """
    
        Parse a variable declaration

        Returns:
            ASTVarDecNode: A variable declaration node

        """

        line = self.crtToken.line
        self.advance() # skip the let token

        if self.crtToken.TokenType != TokenType.IDENTIFIER:
            raise Exception("Expected identifier after let on line ", var_name.line)
        var_name = ast.ASTVariableNode(self.crtToken.value, None, line) # get the current token - should be the variable name
        self.advance() # increment the current token to the next token

        next_token = self.crtToken # get the current token - should be :
        if next_token.TokenType != TokenType.COLON:
            raise Exception("Expected ':' after the variable name on line ", next_token.line)
    
        self.advance() # increment the current token to the next token, colon is skipped 

        var_type = self.crtToken  # get the current token - should be the type of the variable
        if var_type.TokenType != TokenType.TYPE:
            raise Exception("Expected variable type after : on line ", var_type.line)
    
        self.advance() # increment the current token to the next token
    
        next_token = self.crtToken  # get the current token 
        if next_token.TokenType == TokenType.LEFT_SQ_BRACK:
            self.advance()
            return self.parse_array_declaration(line, var_name, var_type)
        if next_token.TokenType != TokenType.ASSIGNMENT_OP:
            raise Exception("Expected '=' after variable type on line ", next_token.line)
        
        self.advance() # increment the current token to the next token - = is skipped
    
        var_expression = self.parse_expression() # get an expression node

        next_token = self.crtToken # get the current token - should be ;
        if next_token.TokenType != TokenType.SEMICOLON:
            raise Exception("Expected ';' after variable expression on line ", next_token.line)

        self.advance() # increment the current token to the next token - ; is skipped

        return ast.ASTVarDecNode(var_name, var_type, var_expression, line) # return the variable declaration node
    
    def parse_array_declaration(self, line, name, type):

        """
    
        Parse an array declaration

        Parameters:
            line (int): The line number
            name (str): The name of the array
            type (TokenType): The type of the array

        Returns:
            ASTArrayDecNode: An array declaration node

        """

        array_length = None

        if self.crtToken.TokenType == TokenType.INT_LITERAL:
            array_length = self.crtToken.value
            self.advance()

        if self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK: 
            raise Exception("Expected ']' after '[' on line ", self.crtToken.line)
        
        self.advance()
        
        if self.crtToken.TokenType != TokenType.ASSIGNMENT_OP:
            raise Exception("Expected '=' after ']' on line ", self.crtToken.line)
        
        self.advance() # increment the current token to the next token - = is skipped

        arary_elements = []

        if self.crtToken.TokenType != TokenType.LEFT_SQ_BRACK:
            raise Exception("Expected '[' after '=' on line ", self.crtToken.line)

        while self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK:
            self.advance()
            arary_elements.append(ast.ASTLiteralNode(self.crtToken.TokenType, self.crtToken.value, self.crtToken.line))
            self.advance()
            if self.crtToken.TokenType != TokenType.COMMA and self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK:
                raise Exception("Expected ',' or ']' on line ", self.crtToken.line)
        
        if self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK:
            raise Exception("Expected ']' on line ", self.crtToken.line)

        self.advance()

        if self.crtToken.TokenType != TokenType.SEMICOLON:
            raise Exception("Expected ';' on line ", self.crtToken.line)
        
        self.advance()

        return ast.ASTArrayDecNode(array_length, arary_elements, line, name, type)

    def parse_expression(self):

        """
        
        Parses an expression

        Returns:
            ASTNode: An expression node
        
        """

        line = self.crtToken.line

        expression = self.parse_simple_expression()

        if(self.crtToken.TokenType == TokenType.RELATIONAL_OP): # Check if the next token is a relational operator
            operator = self.crtToken.value # Get the operator
            self.advance() # Set the operator as the current token
            expression = ast.ASTBinaryOpNode(expression, self.parse_simple_expression(), operator, line) # Return the binary operation node
        
        if(self.crtToken.TokenType == TokenType.AS): # Check if the expression is typcasted
            if (self.nextToken.TokenType == TokenType.TYPE): # Check if the next token is a type
                self.advance() # Set the type as the current token
                expression.add_type(self.crtToken.value) # Add the type to the simple expression
                self.advance() # Advance to the next token
            else:
                raise Exception("Expected type after as on line ", self.crtToken.line)
        else:
            expression.add_type(None)

        return expression # Return the simple expression node

    def parse_simple_expression(self):

        """
        
        Parse a simple expression

        Returns:
            ASTNode: A simple expression node
        
        """

        line = self.crtToken.line

        term = self.parse_term() # Parse the term

        if self.crtToken.TokenType == TokenType.ADDITIVE_OP: # Check if the next token is an addition operator
            operator = self.crtToken.value # Get the operator
            self.advance() # Set the operator as the current token
            return ast.ASTBinaryOpNode(term, self.parse_term(), operator, line) # Return the binary operation node

        return term # Return the term node

    def parse_term(self):

        """
        
        Parse a term

        Returns:
            ASTNode: A term node
        
        """

        line = self.crtToken.line

        factor = self.parse_factor() # Parse the factor

        if self.crtToken.TokenType == TokenType.MULTIPLICATIVE_OP: # Check if the next token is a multiplication operator
            operator = self.crtToken.value # Get the operator
            self.advance() # Set the operator as the current token
            return ast.ASTBinaryOpNode(factor, self.parse_factor(), operator, line) # Return the binary operation node
        
        return factor # Return the factor node

    def parse_factor(self):

        """
        
        Parse a factor
        
        Returns:
            ASTNode: A factor node
            
        """
        
        match self.crtToken.TokenType:
            case TokenType.BOOL_LITERAL | TokenType.INT_LITERAL | TokenType.FLOAT_LITERAL | TokenType.COLOR_LITERAL | TokenType.WIDTH | TokenType.HEIGHT:
                type = self.crtToken.TokenType
                value = self.crtToken.value
                line = self.crtToken.line
                self.advance() # Advance to the next token
                return ast.ASTLiteralNode(type, value, line)
            case TokenType.IDENTIFIER if self.nextToken.TokenType == TokenType.LEFT_PAREN:
                return self.parse_function_call()
            case TokenType.IDENTIFIER if self.nextToken.TokenType != TokenType.LEFT_PAREN:
                identifier = self.crtToken.value
                length = None
                line = self.crtToken.line
                self.advance() # Advance to the next token
                if self.crtToken.TokenType == TokenType.LEFT_SQ_BRACK:
                    self.advance()
                    length = self.parse_expression()
                    if self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK:
                        raise Exception("Expected ']' after array index on line ", self.crtToken.line)
                    self.advance()  
                return ast.ASTVariableNode(identifier, length, line)
            case TokenType.NOT_OP :# TokenType.ADDITIVE_OP if self.crtToken.value == "-":
                operator = self.crtToken.value
                line = self.crtToken.line
                self.advance()
                return ast.ASTUnaryNode(operator, self.parse_expression(), line)
            case TokenType.ADDITIVE_OP:
                if self.crtToken.value == "-":
                    operator = self.crtToken.value
                    line = self.crtToken.line
                    self.advance()
                    return ast.ASTUnaryNode(operator, self.parse_expression(), line)
            case TokenType.RANDOM_INT:
                line = self.crtToken.line
                self.advance() # Advance to the next token - random int is skipped
                return ast.ASTRandomNode(self.parse_expression(), line)
            case TokenType.LEFT_PAREN:
                self.advance() # Advance to the next token - left parenthesis is skipped
                sub_expression = self.parse_expression()
                if self.crtToken.TokenType != TokenType.RIGHT_PAREN: # Check if the next token is a right parenthesis
                    raise Exception("Expected ')' on line ", self.crtToken.line) # Raise an exception if the next token is not a right parenthesis
                self.advance() # Advance to the next token - right parenthesis is skipped
                return sub_expression
            case TokenType.READ:
                line = self.crtToken.line
                self.advance() # Advance to the next token - read is skipped
                expression_1 = self.parse_expression()
                if self.crtToken.TokenType != TokenType.COMMA:
                    raise Exception("Expected ',' on line ", self.crtToken.line)
                self.advance() # Advance to the next token - comma is skipped
                expression_2 = self.parse_expression()
                return ast.ASTReadNode(expression_1, expression_2, line)
            case _:
                raise Exception("Invalid factor on line ", self.crtToken.line)

    def parse_function_call(self):

        """

        Parse a function call

        Returns:
            ASTNode: A function call node
        
        """

        function_name = self.crtToken.value
        line = self.crtToken.line
        self.advance() # Advance to the next token

        if self.crtToken.TokenType != TokenType.LEFT_PAREN: # Check if the next token is a left parenthesis
            raise Exception("Expected '(' after function name on line ", self.crtToken.line) # Raise an exception if the next token is not a left parenthesis
        
        self.advance() # Advance to the next token as the left parenthesis is skipped

        # Check for a closing parenthesis to see if there are any parameters
        if self.crtToken.TokenType == TokenType.RIGHT_PAREN: # Check if the next token is a right parenthesis
            self.advance() # Advance to the next token as the right parenthesis is skipped
            return ast.ASTFunctionCallNode(function_name, [], line) # Return the function call node with no parameters

        parameters = self.parse_actual_parameters() # Get the parameters

        if self.crtToken.TokenType != TokenType.RIGHT_PAREN: # Check if the next token is a right parenthesis
            raise Exception("Expected ')' after function parameters on line ", self.crtToken.line) # Raise an exception if the next token is not a right parenthesis  

        self.advance() # Advance to the next token as the right parenthesis is skipped  
        
        return ast.ASTFunctionCallNode(function_name, parameters, line) # Return the function call node

    def parse_actual_parameters(self):

        """

        Parse the parameters of a function call

        Returns:
            list: A list of expression nodes
        
        """

        parameters = [] # Create an empty list to store the parameters as a list of expression nodes
        expression = self.parse_expression() # Parse the expression
        parameters.append(expression)

        # Check if there are more than one parameter
        while self.crtToken.TokenType == TokenType.COMMA: # Check if the next token is a comma
            self.advance() # Advance to the next token as the comma is skipped
            expression = self.parse_expression() # Parse the expression
            parameters.append(expression) # Append the expression to the list of parameters
        
        return parameters # Return the list of parameters

    def parse_assignment(self):
        
        """

        Parse an assignment statement

        Returns:
            ASTNode: An assignment statement node

        """

        line = self.crtToken.line

        identifier = self.crtToken.value 

        length = None

        self.advance() # Advance to the next token

        if self.crtToken.TokenType == TokenType.LEFT_SQ_BRACK: # Check if variable is an array
            self.advance() # Advance to the next token - left square bracket is skipped
            length = self.parse_expression() # Parse the expression
            if self.crtToken.TokenType != TokenType.RIGHT_SQ_BRACK: # Check if the next token is a right square bracket
                raise Exception("Expected ']' after array index on line ", self.crtToken.line) # Raise an exception if the next token is not a right square bracket
            self.advance() # Advance to the next token - right square bracket is skipped
        
        identifier_node = ast.ASTVariableNode(identifier, length, line) # Create an identifier node

        #self.advance() # Advance to the next token

        if self.crtToken.TokenType != TokenType.ASSIGNMENT_OP: # Check if the next token is an assignment operator
            raise Exception("Expected '=' after variable name on line ", self.crtToken.line) # Raise an exception if the next token is not an assignment operator
        
        self.advance() # Advance to the next token - assignment operator is skipped

        expression = self.parse_expression() # Parse the expression

        return ast.ASTAssignmentNode(identifier_node, expression, line) # Return the assignment statement node
    
    def parse_assignment_statement(self):
            
        """
    
        Parse an assignment statement
    
        Returns:
            ASTNode: An assignment statement node
    
        """
    
        assignment = self.parse_assignment()

        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after assignment on line ", self.crtToken.line) # Raise an exception if the next token is not a semicolon
            
        self.advance() # Advance to the next token - semicolon is skipped

        return assignment # Return the assignment statement node

    def parse_print_statement(self):

        """

        Parse a print statement

        Returns:
            ASTNode: A print statement node

        """

        line = self.crtToken.line
        self.advance() # Advance to the next token - print is skipped

        expression = self.parse_expression() # Parse the expression

        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after print expression on line ", self.crtToken.line) # Raise an exception if the next token is not a semicolon
        
        self.advance() # Advance to the next token - semicolon is skipped

        return ast.ASTPrintNode(expression, line) # Return the print statement node

    def parse_delay_statement(self):

        """

        Parse a delay statement

        Returns:
            ASTNode: A delay statement node

        """
        
        line = self.crtToken.line
        self.advance() # Advance to the next token - delay keywork is skipped

        expression = self.parse_expression() # Parse the expression

        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after delay expression on line ", self.crtToken.line) # Raise an exception if the next token is not a semicolon
        
        self.advance() # Advance to the next token - semicolon is skipped

        return ast.ASTDelayNode(expression, line) # Return the delay statement node

    def parse_write_statement(self):

        """

        Parse a write statement

        Returns:
            ASTNode: A write statement node

        """

        line = self.crtToken.line

        write_node = None # Stores the write node
        
        if self.crtToken.value == "__write":
            self.advance() # Advance to the next token - write keywork is skipped

            expression_1 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a comma
            
            self.advance() # Advance to the next token - comma is skipped

            expression_2 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a comma
            
            self.advance() # Advance to the next token - comma is skipped

            expression_3 = self.parse_expression() # Parse the expression

            write_node = ast.ASTWriteNode(expression_1, expression_2, expression_3, line) # Create a write node

        elif self.crtToken.value == "__write_box":
            self.advance() # Advance to the next token - write box keywork is skipped

            expression_1 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a comma
            
            self.advance() # Advance to the next token - comma is skipped
            
            expression_2 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a comma
            
            self.advance() # Advance to the next token - comma is skipped

            expression_3 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a comma
            
            self.advance() # Advance to the next token - comma is skipped

            expression_4 = self.parse_expression() # Parse the expression

            if self.crtToken.TokenType != TokenType.COMMA: # Check if the next token is a comma 
                raise Exception("Expected ',' after write expression on line ", self.crtToken.line)

            self.advance() # Advance to the next token

            expression_5 = self.parse_expression() # Parse the expression

            write_node = ast.ASTWriteBoxNode(expression_1, expression_2, expression_3, expression_4, expression_5, line) # Create a write box node

        else :
            raise Exception("Invalid write statement on line ", self.crtToken.line)
        
        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after write expression on line ", self.crtToken.line) # Raise an exception if the next token is not a semicolon
        
        self.advance() # Advance to the next token - semicolon is skipped

        return write_node

    def parse_if_statement(self):
        
        line = self.crtToken.line
        self.advance() # Advance to the next token - if is skipped

        if self.crtToken.TokenType != TokenType.LEFT_PAREN: # Check if the next token is a left parenthesis
            raise Exception("Expected '(' after if on line ", self.crtToken.line) # Raise an exception if the next token is not a left parenthesis
        
        self.advance() # Advance to the next token

        condition = self.parse_expression() # Parse the expression

        if self.crtToken.TokenType != TokenType.RIGHT_PAREN: # Check if the next token is a right parenthesis
            raise Exception("Expected ')' after condition on line ", self.crtToken.line) # Raise an exception if the next token is not a right parenthesis
        
        self.advance() # Advance to the next token - right parenthesis is skipped

        true_block = self.parse_block() # Parse the block

        false_block = None # Optional block

        if self.crtToken.TokenType == TokenType.ELSE: # Check if the next token is an else
            self.advance() # Advance to the next token - else is skipped
            false_block = self.parse_block() # Parse the optional block

        return ast.ASTIfNode(condition, true_block, false_block, line) # Return the if statement node

    def parse_for_statement(self):
        
        line = self.crtToken.line
        self.advance() # Advance to the next token - for is skipped

        if self.crtToken.TokenType != TokenType.LEFT_PAREN: # Check if the next token is a left parenthesis
            raise Exception("Expected '(' after for on line ", self.crtToken.line) # Raise an exception if the next token is not a left parenthesis
        
        self.advance() # Advance to the next token - left parenthesis is skipped

        variable = None

        if self.crtToken.TokenType == TokenType.LET: # Check if the next token is a let
            variable = self.parse_variable_declartion() # Parse the variable declaration
        
        condition = self.parse_expression() # Parse the expression

        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after condition on line ", self.crtToken.line) # Raise an exception if the next token is not a semicolon
        
        self.advance() # Advance to the next token - semicolon is skipped

        increment = None
        if (self.crtToken.TokenType == TokenType.IDENTIFIER):
            increment = self.parse_assignment()

        if self.crtToken.TokenType != TokenType.RIGHT_PAREN: # Check if the next token is a right parenthesis
            raise Exception("Expected ')' after increment on line ", self.crtToken.line) # Raise an exception if the next token is not a right parenthesis
        
        self.advance() # Advance to the next token - right parenthesis is skipped

        block = self.parse_block() # Parse the block

        return ast.ASTForNode(variable, condition, increment, block, line) # Return the for statement node

    def parse_while_statement(self):

        """
        
        Parse a while statement
        
        Returns:
            ASTNode: A while statement node
            
        """
        
        line = self.crtToken.line
        self.advance()

        if self.crtToken.TokenType != TokenType.LEFT_PAREN:
            raise Exception("Expected '(' after while on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token - left parenthesis is skipped

        condition = self.parse_expression()

        if self.crtToken.TokenType != TokenType.RIGHT_PAREN:
            raise Exception("Expected ')' after condition on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token - right parenthesis is skipped

        block = self.parse_block()

        return ast.ASTWhileNode(condition, block, line)

    def parse_return_statement(self):

        """

        Parse a return statement

        Returns:
            ASTNode: A return statement node
        
        """

        line = self.crtToken.line
        self.advance() # Advance to the next token - return is skipped

        expression = self.parse_expression() # Parse the expression

        if self.crtToken.TokenType != TokenType.SEMICOLON: # Check if the next token is a semicolon
            raise Exception("Expected ';' after return expression on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token - semicolon is skipped

        return ast.ASTReturnNode(expression, line) # Return the return statement node

    def parse_function_declaration(self):

        """

        Parse a function declaration

        Returns:
            ASTNode: A function declaration node

        """
        
        line = self.crtToken.line
        self.advance() # Advance to the next token - fun is skipped

        function_name = self.crtToken # Get the current token - should be an identifier
        if function_name.TokenType != TokenType.IDENTIFIER: # Check if the current token is an identifier
            raise Exception("Expected identifier after fun on line ", function_name.line)
        
        self.advance() # Advance to the next token

        if self.crtToken.TokenType != TokenType.LEFT_PAREN: # Check if the current token is a left parenthesis
            raise Exception("Expected '(' after function name on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token

        parameters = self.parse_formal_parameters() # Parse the parameters

        if self.crtToken.TokenType != TokenType.RIGHT_PAREN: # Check if the current token is a right parenthesis
            raise Exception("Expected ')' after function parameters on line ", self.crtToken.line)

        self.advance() # Advance to the next token

        if self.crtToken.TokenType != TokenType.FUNC_ASSIGNMENT_OP: # Check if the current token is a colon
            raise Exception("Expected '->' after function parameters on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token

        return_type = self.crtToken # Get the current token - should be a type

        if return_type.TokenType != TokenType.TYPE: # Check if the current token is a type
            raise Exception("Expected type after '->' on line ", return_type.line)
        
        self.advance() # Advance to the next token

        func_block = self.parse_block() # Parse the block

        return ast.ASTFunctionNode(function_name, parameters, return_type, func_block, line) # Return the function declaration node
    
    def parse_formal_parameter(self):

        """

        Parse a formal parameter

        Returns:
            ASTNode: A formal parameter node

        """
        
        line = self.crtToken.line
        identifier = self.crtToken

        if identifier.TokenType != TokenType.IDENTIFIER: # Check if the current token is an identifier
            raise Exception("Expected identifier after '(' on line ", identifier.line) # Raise an exception if the current token is not an identifier
        
        self.advance() # Advance to the next token

        if self.crtToken.TokenType != TokenType.COLON: # Check if the current token is a colon
            raise Exception("Expected ':' after parameter name on line ", self.crtToken.line)
        
        self.advance() # Advance to the next token

        type = self.crtToken

        if type.TokenType != TokenType.TYPE: # Check if the current token is a type
            raise Exception("Expected type after ':' on line ", self.crtToken.line) # Raise an exception if the current token is not a type
        
        self.advance() # Advance to the next token

        return ast.ASTFormalParameterNode(identifier, type, line)
    
    def parse_formal_parameters(self):

        """

        Parse the parameters of a function declaration

        Returns:
            list: A list of formal parameter nodes

        """

        parameters = []

        if self.crtToken.TokenType == TokenType.RIGHT_PAREN: # Check if the current token is a right parenthesis
            return parameters # Return since there are no parameters

        parameter = self.parse_formal_parameter()

        parameters.append(parameter)

        while self.crtToken.TokenType == TokenType.COMMA:
            self.advance()
            parameter = self.parse_formal_parameter()
            parameters.append(parameter)

        return parameters

    def parse_block(self):

        """

        Parse a block

        Returns:
            ASTNode: A block node

        """
        
        line = self.crtToken.line # Get the line number
        self.advance() # Advance to the next token - left brace is skipped

        statements = [] # Create an empty list to store the statements

        while self.crtToken.TokenType != TokenType.RIGHT_BRACE and self.crtToken.TokenType != TokenType.EOF: # Check if the current token is a right brace or EOF
            statement = self.parse_statement() # Parse the statement
            statements.append(statement) # Append the statement to the list of statements

        if self.crtToken.TokenType != TokenType.RIGHT_BRACE: # Check if the current token is a right brace
            raise Exception("Expected '}' on line ", self.crtToken.line) # Raise an exception if the current token is not a right brace
        
        self.advance() # Advance to the next token

        return ast.ASTBlockNode(statements, line)

    def advance(self):

        """

        Advance the current and next token

        """

        self.index += 1
        if self.index < len(self.tokens):
            self.crtToken = self.tokens[self.index]
        if self.index + 1 < len(self.tokens):
            self.nextToken = self.tokens[self.index + 1]
        else:
            self.nextToken = lexer.Token("", lexer.TokenType.EOF, -1)   

    def parse_program(self):

        """

        Parses the program

        Returns:
            ASTNode: A program node

        """
    
        self.advance()
        while self.crtToken.TokenType != lexer.TokenType.EOF:
            statement = self.parse_statement()
            self.ASTroot.add_statement(statement)
        return self.ASTroot
    
    def Parse(self):        
        self.ASTroot = self.parse_program()

# Test the parser
src_program = "let x:float[] = [1, 2, 3];"
parser = Parser(src_program)
parser.Parse()