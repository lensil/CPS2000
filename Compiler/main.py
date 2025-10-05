from lexer import *
from parser_ import *
from semantic_analysis_visitor import * 
from code_generation_visitor import *

task_1_1_path = 'Examples/test.txt' 
with open(task_1_1_path, 'r') as file:
    src_program_str = file.read()

# Lexer 
lexer = Lexer()
tokens = lexer.generate_tokens(src_program_str)
for token in tokens:
    print(token.TokenType, token.value, token.line)

# Parser
parser = Parser(src_program_str)
program_ast = parser.parse_program()

# Semantic Analysis
program_ast.accept(SemanticAnalysisVisitor())

# Code Generation
program_ast.accept(CodeGenerationVisitor("output.txt"))