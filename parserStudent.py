import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0

        self.token_types = {
            'VARIABLE': r'[a-zA-Z_]\w*',
            'INTEGER': r'\d+',
            'OPERATOR': r'[-+*/]',
            'ASSIGN': r'=',
            'SEMICOLON': r';',
            'PARENTHESIS': r'[()]'
        }

    def parse_token(self, token):
        for type, pattern in self.token_types.items():
            if re.fullmatch(pattern, token):
                if type == 'INTEGER':
                    return type, int(token)
                return type, token

        raise ValueError(f'Invalid character: {token}')

    def tokenize(self):
        lines = self.input.split('\n')
        tokens = []

        for line in lines:
            raw_tokens = re.split('(\W)', line)
            line_tokens = [Token(*self.parse_token(token)) for token in raw_tokens if token.strip() != '']

            tokens += line_tokens
        return tokens

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def consume(self, expected_type=None):
        # Consume the current token and move to the next token.
        if expected_type and self.tokens[self.position].type != expected_type:
            raise SyntaxError(f"Syntax error: Expected {expected_type} but found {self.tokens[self.position].type}")
        self.position += 1

    def peek(self):
        # Get the current token without moving to the next one.
        if self.position >= len(self.tokens):
            raise SyntaxError("Syntax error: unexpected end of input")
        return self.tokens[self.position]

    def parse(self):
        # Start parsing with StatementList
        root = self.parse_statement_list()
        return root

    def parse_statement_list(self):
        # StatementList -> Statement StatementList | Statement
        statement_count = self.tokens.count(Token('SEMICOLON', ';'))
        if statement_count == 0:
            raise SyntaxError("Syntax error: unexpected end of input")

        statements = []
        for _ in range(statement_count):
            statements.append(self.parse_statement())
            self.consume('SEMICOLON')

        # statements = [self.parse_statement()]
        # if self.position >= len(self.tokens):
        #     return Node('StatementList', children=statements)

        # while self.peek().type == 'SEMICOLON':
        #     self.consume('SEMICOLON')  # Consume the semicolon
        #     statements.append(self.parse_statement())
        return Node('StatementList', children=statements)

    def parse_statement(self):
        # Statement -> AssignmentStatement
        return self.parse_assignment_statement()

    def parse_assignment_statement(self):
        # AssignmentStatement -> VARIABLE ASSIGN Expression SEMICOLON
        variable = self.peek().value  # The left-hand side variable
        self.consume('VARIABLE')
        self.consume('ASSIGN')  # Consume the assignment operator
        expression = self.parse_expression()
        return Node('AssignmentStatement', value=variable, children=[expression])

    def parse_expression(self):
        # Expression -> (Expression) | Expression OPERATOR Term | Term
        if self.peek().type == 'PARENTHESIS' and self.peek().value == '(':
            self.consume('PARENTHESIS')
            expression = self.parse_expression()

            if self.peek().type == 'OPERATOR':
                operator = self.peek().value
                self.consume('OPERATOR')
                right_term = self.parse_term()
                self.consume('PARENTHESIS')  # Consume the closing parenthesis
                if self.peek().type == 'OPERATOR':
                    right_term = Node('Expression', value=operator, children=[right_term, self.parse_expression()])
                return Node('Expression', value=operator, children=[expression, right_term])
            else:
                self.consume('PARENTHESIS')  # Consume the closing parenthesis

                if self.peek().type == 'OPERATOR':
                    operator = self.peek().value
                    self.consume('OPERATOR')
                    right_term = self.parse_term()
                    if self.peek().type == 'OPERATOR':
                        right_term = Node('Expression', value=operator, children=[right_term, self.parse_expression()])
                    return Node('Expression', value=operator, children=[expression, right_term])
                return expression

        else:
            left_term = self.parse_term()
            
            if self.peek().type == 'SEMICOLON':
                return left_term

            while self.peek().type == 'OPERATOR':
                operator = self.peek().value
                self.consume('OPERATOR')
                # right_term = self.parse_term()
                right_term = self.parse_expression()
                left_term = Node('Expression', value=operator, children=[left_term, right_term])
            return left_term

    def parse_term(self):
        # Term -> INTEGER | VARIABLE
        if self.peek().type == 'INTEGER':
            value = int(self.peek().value)
            self.consume('INTEGER')
            return Node('Term', value=value)
        elif self.peek().type == 'VARIABLE':
            variable = self.peek().value
            self.consume('VARIABLE')
            return Node('Term', value=variable)
        else:
            raise SyntaxError(f"Syntax error: Expected INTEGER or VARIABLE, but found {self.peek().type}")