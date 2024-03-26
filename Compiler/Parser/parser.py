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
        #for now we'll assume an expression can only be an integer
        if (self.crtToken.TokenType == lex.TokenType.INT_LITERAL):
            value = self.crtToken.value
            self.NextToken()
            return ast.ASTIntegerNode(value)

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
        self.NextToken() # Consuming the IF token
        condition = self.ParseExpression() # Parsing the condition
        false_block = None
        if self.crtToken.TokenType == lex.TokenType.KEYWORD and self.crtToken.value == "else":
            self.NextToken()
            false_block = self.ParseBlock()
        return ASTIfNode(condition, true_block, false_block)
    
    def ParseStatement(self):
        #At the moment we only have assignment statements .... you'll need to add more for the assignment - branching depends on the token type
        return self.ParseAssignment()
    

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
parser = Parser("     x=   23 ; y=  100;  z = 23 ;")
parser.Parse()

print_visitor = ast.PrintNodesVisitor()
parser.ASTroot.accept(print_visitor)