# CPS2000 Assignment

This project is a compiler for the PArL programming language, written in Python. It includes a lexer, parser, semantic analyzer, and code generator.

## Project Structure

- `Compiler/`: Contains the main components of the compiler.
  - `astnodes.py`: Defines the AST nodes used by the parser.
  - `code_generation_visitor.py`: Contains the `CodeGenerationVisitor` class for generating code.
  - `dfa.py`: Defines the DFA for the lexer.
  - `lexer.py`: Contains the `Lexer` class for lexical analysis.
  - `main.py`: The main entry point of the compiler.
  - `parser_.py`: Contains the `Parser` class for parsing.
  - `semantic_analysis_visitor.py`: Contains the `SemanticAnalysisVisitor` class for semantic analysis.
  - `symbol_table.py`: Defines the symbol table used by `SemanticAnalysisVisitor` and `CodeGenerationVisitor`.
  - `tokens.py`: Defines the tokens for the lexer.
  - `visitor.py`: Defines the `ASTVisitor` class for visiting AST nodes.
- `Examples/`: Contains example programs.
- `output.txt`: The output file of the code generator.
- `Documentation/`: Contains the documentation of the compiler.
   - `CPS2000_doc.pdf`: The report of the compiler. A link to the video presentation is included in the report.
   - `PlagiarismForm.pdf`: The plagiarism form.
## Requirments

- Python 3.10 or later

## Usage

To use the compiler, run the `main.py` file with a program in the `test.txt` file as input. The generated code will be written to `output.txt`.
