#First some AST Node classes we'll use to build the AST with
# Best on what you're parsing you generate the appropriate AST nodes
class ASTNode: # Base class for all AST nodes
    def __init__(self):
        self.name = "ASTNode"    

# ASTNode for  more specific statements etc
class ASTStatementNode(ASTNode):
    def __init__(self):
        self.name = "ASTStatementNode"

class ASTExpressionNode(ASTNode):
    def __init__(self):
        self.name = "ASTExpressionNode"

# ASTNode for variable
# Stores what the variable is 
class ASTVariableNode(ASTExpressionNode):
    def __init__(self, lexeme): # Store lexeme 
        # e.g if variable x this would be the lexeme
        self.name = "ASTVariableNode"
        self.lexeme = lexeme

    def accept(self, visitor):
        visitor.visit_variable_node(self)

class ASTIntegerNode(ASTExpressionNode):
    def __init__(self, v):
        self.name = "ASTIntegerNode" # Name not needed
        self.value = v # Instead of lexeme but same concept

    def accept(self, visitor):
        visitor.visit_integer_node(self)        

class ASTAssignmentNode(ASTStatementNode):
    def __init__(self, ast_var_node, ast_expression_node):
        self.name = "ASTStatementNode"        
        self.id   = ast_var_node # Variable node
        self.expr = ast_expression_node # Expression node

    # Pass visitor pattern
    # Call accept 
    def accept(self, visitor):
        visitor.visit_assignment_node(self)
        visitor.inc_tab_count()
        self.id.accept(visitor)
        self.expr.accept(visitor)
        visitor.dec_tab_count()

# ASTNode for block of statements i.e. { ... }
class ASTBlockNode(ASTNode):
    def __init__(self):
        self.name = "ASTBlockNode"
        self.stmts = [] # Array of statements
        # Won't know beforehand how many statements in block -> i.e. node
        # Can do it differently 
        # Parse symbol table (visitor)

    def add_statement(self, node):
        self.stmts.append(node)

    def accept(self, visitor):
        visitor.visit_block_node(self)
        visitor.inc_tab_count()
        
        for st in self.stmts:
            st.accept(visitor)
        
        visitor.dec_tab_count()

# Visitor pattern
# Will not be implemented 
# Parent of all visiotrs
class ASTVisitor:

    # Need to implement these eventually??
    def visit_integer_node(self, node):
        raise NotImplementedError()

    def visit_assignment_node(self, node):
        raise NotImplementedError()
    
    def visit_variable_node(self, node):
        raise NotImplementedError()
    
    def visit_block_node(self, node):
        raise NotImplementedError()
    
    def reset(self):
        raise NotImplementedError()
    
    def inc_tab_count(self):
        raise NotImplementedError()
    
    def dec_tab_count(self):
        raise NotImplementedError()

# Concrete implementation 
# Visitor to print nodes
class PrintNodesVisitor(ASTVisitor):
    def __init__(self):
        self.name = "Print Tree Visitor"
        self.node_count = 0
        self.tab_count = 0

    # Implmentation of the functions
    def reset(self):
        self.node_count = 0
        self.tab_count = 0

    def inc_tab_count(self):
        self.tab_count += 1

    def dec_tab_count(self):
        self.tab_count -= 1
        
    # Leaf ??
    def visit_integer_node(self, int_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Integer value::", int_node.value)

    def visit_assignment_node(self, ass_node):
        self.node_count += 1        
        print('\t' * self.tab_count, "Assignment node => ")        

    def visit_variable_node(self, var_node):
        self.node_count += 1
        print('\t' * self.tab_count, "Variable => ", var_node.lexeme)

    def visit_block_node(self, block_node):
        self.node_count += 1
        print('\t' * self.tab_count, "New Block => ")        


#Create a print visitor instance
print_visitor = PrintNodesVisitor()

#assume root node the AST assignment node .... 
#x=23
# Should be done parser 
# This is for debugging
print("Building AST for assigment statement x=23;")
assignment_lhs = ASTVariableNode("x")
assignment_rhs = ASTIntegerNode(23)
root = ASTAssignmentNode(assignment_lhs, assignment_rhs)
root.accept(print_visitor)
print("Node Count => ", print_visitor.node_count)
print("----")


#assume root node the AST variable node .... 
#x123
print("Building AST for variable x123;")
root = ASTVariableNode("x123")
print_visitor.reset()    #reset visitor - in this case node and tab counts

root.accept(print_visitor)
print("Node Count => ", print_visitor.node_count)