import lexer
import astnodes as ast
from tokens import TokenType

# To do: check if the line number is correct for all nodes
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
            case TokenType.IDENTIFIER if self.nextToken.TokenType == TokenType.EQUALS:
                return self.parse_assignment()
            case TokenType.PRINT:
                return self.parse_print_statement()
            case TokenType.DELAY:
                return self.parse_delay_statement()
            case TokenType.WRITE, TokenType.WRITE_BOX:
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

        var_name = self.crtToken # get the current token - should be an identifier
        if var_name.TokenType != TokenType.IDENTIFIER:
            raise Exception("Expected identifier after let on line ", var_name.line)
    
        self.advance() # increment the current token to the next token

        next_token = self.crtToken # get the current token - should be :
        if next_token.TokenType != TokenType.COLON:
            raise Exception("Expected ':' after the variable name on line ", next_token.line)
    
        self.advance() # increment the current token to the next token, colon is skipped 

        var_type = self.crtToken  # get the current token - should be the type of the variable
        if var_type.TokenType != TokenType.TYPE:
            raise Exception("Expected variable type after : on line ", var_type.line)
    
        self.advance() # increment the current token to the next token
    
        next_token = self.crtToken  # get the current token - should be =
        if next_token.TokenType != TokenType.ASSIGNMENT_OP:
            raise Exception("Expected '=' after variable type on line ", next_token.line)
        
        self.advance() # increment the current token to the next token - = is skipped
    
        var_expression = self.parse_expression() # get an expression node

        self.advance() # increment the current token to the next token

        next_token = self.crtToken # get the current token - should be ;
        if next_token.TokenType != TokenType.SEMICOLON:
            raise Exception("Expected ';' after variable expression on line ", next_token.line)
    
        return ast.ASTVarDecNode(var_name, var_type, var_expression, line) # return the variable declaration node

    def parse_expression(self):

        """
        
        Parse a simple expression

        Returns:
            ASTNode: A simple expression node
        
        """

        line = self.crtToken.line

        expression = self.parse_simple_expression()

        if(self.crtToken.TokenType == TokenType.RELATIONAL_OP): # Check if the next token is a relational operator
            operator = self.crtToken.value # Get the operator
            self.advance() # Set the operator as the current token
            expression = ast.ASTBinaryOpNode(expression, self.parse_simple_expression(), operator, line) # Return the binary operation node
        
        if(self.nextToken.TokenType == TokenType.AS): # Check if the expression is typcasted
            self.advance() # Set the as as the current token
            if (self.nextToken.TokenType == TokenType.TYPE): # Check if the next token is a type
                self.advance() # Set the type as the current token
                expression.add_type(self.crtToken.value) # Add the type to the simple expression
            else:
                raise Exception("Expected type after as on line ", self.crtToken.line)

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
                line = self.crtToken.line
                self.advance() # Advance to the next token
                return ast.ASTVariableNode(identifier, line)
            case TokenType.NOT_OP :# TokenType.ADDITIVE_OP if self.crtToken.value == "-":
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

        function_name = self.crtToken
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
        pass

    def parse_print_statement(self):
        pass

    def parse_delay_statement(self):
        pass

    def parse_write_statement(self):
        pass

    def parse_if_statement(self):
        pass

    def parse_for_statement(self):
        pass

    def parse_while_statement(self):
        pass


    def parse_return_statement(self):
        pass

    def parse_function_declaration(self):
        pass

    def parse_block(self):
        pass

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

    def Parse(self):        
        self.advance()
        self.ASTroot = self.parse_statement()