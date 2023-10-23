# A Compiler 👾

This project is a basic compiler for a simple programming language, implemented in Python. The compiler consists of three main components: a Lexer, a Parser, and a Node class for constructing an Abstract Syntax Tree (AST). The code implements concepts such as lexical analysis, syntax analysis, and AST construction, fundamental concepts in compiler construction and programming languages.

## Example
Code:
```plaintext
a = 5 + 3;
b = a * 2 - 1;
c = (a + b) * 2;
```

Abstract Syntax Tree:
```plaintext
AssignmentStatement: a
        Expression: +
                Term: 5
                Term: 3
AssignmentStatement: b
        Expression: *
                Term: a
                Expression: -
                        Term: 2
                        Term: 1
AssignmentStatement: c
        Expression: *
                Expression: +
                        Term: a
                        Term: b
                Term: 2
```

## Components

### 1. Lexer

- **Class**: `Lexer`
- **Purpose**: The lexer is responsible for converting the input string, which represents a sequence of characters, into a list of Token objects.
- **Attributes**:
  - `input`: The input string to be analyzed.
  - `position`: The current character position in the input string.
- **Methods**:
  - `parse_token(token)`: Recognizes the type of token and creates the corresponding Token object.
  - `tokenize()`: Tokenizes the input string and returns a list of Token objects.

### 2. Token

- **Class**: `Token`
- **Purpose**: Models individual tokens, representing the smallest units of meaning in the input.
- **Attributes**:
  - `type`: Denotes the type of token (e.g., INTEGER, OPERATOR, VARIABLE).
  - `value`: Holds the actual string value or content of the token.

### 3. Parser

- **Class**: `Parser`
- **Purpose**: Converts the sequence of tokens into an AST, revealing the hierarchical structure of the program.
- **Attributes**:
  - `tokens`: List of tokens to be parsed.
  - `position`: The current position in the list of tokens.
- **Methods**:
  - `consume(expected_type=None)`: Reads the current token and ensures it is of the expected type, moving the position to the next token.
  - `peek()`: Examines the type and value of the current token without moving to the next token.
  - `parse()`: Constructs the root of the Abstract Syntax Tree (AST) and iteratively parses each statement in the token list.
  - `parse_statement_list()`: Parses a list of statements.
  - `parse_statement()`: Parses a single statement.
  - `parse_assignment_statement()`: Parses an assignment statement.
  - `parse_expression()`: Parses expressions involving mathematical operations.
  - `parse_term()`: Parses individual terms in an expression (integers, variables, or nested expressions).

### 4. Node

- **Class**: `Node`
- **Purpose**: Models a node in the AST, holding the type, value, and children of each node in the tree.
- **Attributes**:
  - `type`: Represents the type of the node (e.g. ASSIGNMENT, EXPRESSION).
  - `value`: Contains the value or content of the node.
  - `children`: A list holding the child nodes of the current node.

## Streaming Input

One important feature of this compiler is its ability to stream input, allowing it to create ASTs for unlimited code. The Lexer and Parser are designed to process code as it is fed in, making it suitable for handling code of arbitrary length.
