"""

    General visitor class for the compiler

"""

class ASTVisitor:

    def visit_program_node(self, node):
        raise NotImplementedError()
    
    def visit_expression_node(self, node):  
        raise NotImplementedError()

    def visit_literal_node(self, node):
        raise NotImplementedError()
    
    def visit_variable_node(self, node):
        raise NotImplementedError()
    
    def visit_unary_op_node(self, node):
        raise NotImplementedError()
    
    def visit_range_node(self, node):
        raise NotImplementedError()

    def visit_read_node(self, node):
        raise NotImplementedError()
    
    def visit_function_call_node(self, node):
        raise NotImplementedError()
    
    def visit_binary_op_node(self, node):
        raise NotImplementedError()
    
    def visit_var_dec_node(self, node):
        raise NotImplementedError()
    
    def visit_return_node(self, node):
        raise NotImplementedError()
    
    def visit_delay_node(self, node):
        raise NotImplementedError()
    
    def visit_write_node(self, node):
        raise NotImplementedError()
    
    def visit_write_box_node(self, node):
        raise NotImplementedError()
    
    def visit_print_node(self, node):
        raise NotImplementedError()
    
    def visit_formal_parameter_node(self, node):
        raise NotImplementedError()
    
    def visit_function_node(self, node):
        raise NotImplementedError()
    
    def visit_block_node(self, node):
        raise NotImplementedError()
    
    def visit_assignment_node(self, node):
        raise NotImplementedError()
    
    def visit_if_node(self, node):
        raise NotImplementedError()
    
    def visit_while_node(self, node):
        raise NotImplementedError()
    
    def visit_for_node(self, node):
        raise NotImplementedError()
    
    def reset(self):
        raise NotImplementedError()
    
    def inc_tab_count(self):
        raise NotImplementedError()
    
    def dec_tab_count(self):
        raise NotImplementedError()