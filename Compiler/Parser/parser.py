# Now we need the parser (using tokens produced by the Lexer) to build the AST - this code snipper is able to build ASTAssignmentNode trees. LHS can only be an integer here ....
# A small predictive recursive descent parser
import astnodes as ast
import lexer as lex

class Parser:
    def __init__(self, src_program_str):
        self.name = "PARSEAR"
        self.lexer = lex.Lexer()
        self.index = -1  #start at -1 so that the first token is at index 0
        self.src_program = src_program_str
        self.tokens = self.lexer.generate_tokens(self.src_program)
        #print("[Parser] Lexer generated token list ::")
        #for t in self.tokens:
        #    print(t.type, t.lexeme)
        self.crtToken = lex.Token("", lex.TokenType.ERROR)
        self.nextToken = lex.Token("", lex.TokenType.ERROR)
        self.ASTroot = ast.ASTAssignmentNode     #this will need to change once you introduce the AST program node .... that should become the new root node    

    def NextTokenSkipWS(self):
        self.index += 1   #Grab the next token
        if (self.index < len(self.tokens)):
            self.crtToken = self.tokens[self.index]
        else:
            self.crtToken = lex.Token(lex.TokenType.EOF, "END")

    def NextToken(self):
        self.NextTokenSkipWS()
        while (self.crtToken.TokenType == lex.TokenType.WHITESPACE):
            #print("--> Skipping WS")
            self.NextTokenSkipWS()

        #print("Next Token Set to ::: ", self.crtToken.type, self.crtToken.lexeme)                 

    def ParseExpression(self):
        left = None
        # First, check if the expression starts with an identifier (variable name)
        if self.crtToken.TokenType == lex.TokenType.IDENTIFIER:
            left = ast.ASTVariableNode(self.crtToken.value)
            self.NextToken()  # Move past the identifier
        elif self.crtToken.TokenType == lex.TokenType.INT_LITERAL:
            left = ast.ASTIntegerNode(self.crtToken.value)
            self.NextToken()
            return left

        # Then, check for a relational operator
        if self.crtToken.TokenType == lex.TokenType.REL_OP:
            op = self.crtToken.value
            self.NextToken()  # Move past the relational operator

            # After the relational operator, expect an integer literal
            if self.crtToken.TokenType == lex.TokenType.INT_LITERAL:
                right = ast.ASTIntegerNode(self.crtToken.value)
                self.NextToken()  # Move past the integer literal

            # Return a binary operation node representing the entire expression
                return ast.ASTBinaryOpNode(left, right, op)
            else:
                raise Exception("Expected an integer literal after relational operator")
        else:
        # If there's no relational operator, the expression might just be an identifier or integer
            return left  # Or you could directly return an integer node if that's the case

    def ParseAssignment(self):
        #Assignment is made up of two main parts; the LHS (the variable) and RHS (the expression)
        if (self.crtToken.TokenType == lex.TokenType.IDENTIFIER):
            #create AST node to store the identifier            
            assignment_lhs = ast.ASTVariableNode(self.crtToken.value)
            self.NextToken()
            #print("Variable Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        if (self.crtToken.TokenType == lex.TokenType.ASSIGNMENT_OP):
            #no need to do anything ... token can be discarded
            self.NextToken()
            #print("EQ Token Matched ::: Nxt Token is ", self.crtToken.type, self.crtToken.lexeme)

        #Next sequence of tokens should make up an expression ... therefor call ParseExpression that will return the subtree representing that expression
        assignment_rhs = self.ParseExpression()
                
        return ast.ASTAssignmentNode(assignment_lhs, assignment_rhs)
    
    def ParseIfStatement(self):
        self.NextToken()  # Consumes the 'if'
        # Check if the next token is a '('
        if self.crtToken.TokenType != lex.TokenType.PUNCTUATION or self.crtToken.value != '(':
            raise Exception("Expected '(' after 'if'")
        self.NextToken()  # Consumes the '('

        condition = self.ParseExpression()  # Parses <Expr>

        # Check if the next token is a ')'
        if self.crtToken.TokenType != lex.TokenType.PUNCTUATION or self.crtToken.value != ')':
            print("Current token:", self.crtToken.TokenType, self.crtToken.value)  # Debug print
            raise Exception("Expected ')' after condition")
        self.NextToken()  # Consumes the ')'

        true_block = self.ParseBlock()  # Parses <Block>

        false_block = None # Optional <Block>

        # Check if the next token is an 'else'
        if self.crtToken.TokenType == lex.TokenType.KEYWORD and self.crtToken.value == 'else':
            self.NextToken()  # Consumes the 'else'
            false_block = self.ParseBlock()  # Parses the optional <Block>

        # Return the ASTIfNode
        return ast.ASTIfNode(condition, true_block, false_block)
    
    def ParseWhileStatement(self):
        self.NextToken() # Consumes the 'while'
        # Check if the next token is a '('
        if self.crtToken.TokenType != lex.TokenType.PUNCTUATION or self.crtToken.value != '(':
            raise Exception("Expected '(' after 'while'")
        self.NextToken()
        condition = self.ParseExpression()

        # Check if the next token is a ')'
        if self.crtToken.TokenType != lex.TokenType.PUNCTUATION or self.crtToken.value != ')':
            raise Exception("Expected ')' after condition")
        
        self.NextToken() # Consumes the ')'
        block = self.ParseBlock() # Parses <Block>
        return ast.ASTWhileNode(condition, block) # Return the ASTWhileNode
    
    def ParseStatement(self):
        if self.crtToken.TokenType == lex.TokenType.IDENTIFIER:
        # Lookahead to see what the next significant token is.
            lookaheadToken = self.PeekNextToken()
        
            # If the next token is an assignment operator, parse an assignment.
            if lookaheadToken.TokenType == lex.TokenType.ASSIGNMENT_OP:
                return self.ParseAssignment()
            else:
                return self.ParseExpression()
        elif self.crtToken.TokenType == lex.TokenType.KEYWORD and self.crtToken.value == 'if':
            return self.ParseIfStatement()
        elif self.crtToken.TokenType == lex.TokenType.KEYWORD and self.crtToken.value == 'while':
            return self.ParseWhileStatement()
        else:
            raise Exception("Invalid statement")
    
    def PeekNextToken(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]
        else:
            return lex.Token("", lex.TokenType.EOF)  # Return an EOF token if there are no more tokens.
    
    def ParseBlock(self):
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type

        block = ast.ASTBlockNode()

        while (self.crtToken.TokenType != lex.TokenType.EOF):
            #print("New Statement - Processing Initial Token:: ", self.crtToken.type, self.crtToken.lexeme)
            s = self.ParseStatement()
            block.add_statement(s)
            if (self.crtToken.TokenType == lex.TokenType.PUNCTUATION):
                self.NextToken()
            else:
                print("Syntax Error - No Semicolon separating statements in block")
                break
        
        return block

    def ParseProgram(self):                        
        self.NextToken()  #set crtToken to the first token (skip all WS)
        b = self.ParseBlock()        
        return b        

    def Parse(self):        
        self.ASTroot = self.ParseProgram()


#parser = Parser("x=23;")
parser = Parser("     x=   23; y =6;")
parser.Parse()

print_visitor = ast.PrintNodesVisitor()
parser.ASTroot.accept(print_visitor)