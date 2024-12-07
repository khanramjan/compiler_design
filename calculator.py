class Lexer:
    def __init__(self, input):
        self.input = input
        self.index = 0
        self.tokens = []

    def tokenize(self):
        operators = ['+', '-', '*', '/', '(', ')']
        while self.index < len(self.input):
            char = self.input[self.index]

            if char.isspace():
                self.index += 1
                continue

            if char.isdigit():
                number = ''
                while self.index < len(self.input) and self.input[self.index].isdigit():
                    number += self.input[self.index]
                    self.index += 1
                self.tokens.append({'type': 'NUMBER', 'value': int(number)})
                continue

            if char in operators:
                self.tokens.append({'type': 'OPERATOR', 'value': char})
                self.index += 1
                continue

            if char == ';':
                self.tokens.append({'type': 'END', 'value': ';'})
                self.index += 1
                continue

            print(f"Invalid token: '{char}' at position {self.index}")
            self.index += 1  

        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse_expression(self):
        left = self.parse_term()
        while self.match('OPERATOR') and self.tokens[self.index]['value'] in ('+', '-'):
            operator = self.consume()['value']
            right = self.parse_term()
            left = {'type': 'BinaryExpression', 'operator': operator, 'left': left, 'right': right}
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.match('OPERATOR') and self.tokens[self.index]['value'] in ('*', '/'):
            operator = self.consume()['value']
            right = self.parse_factor()
            left = {'type': 'BinaryExpression', 'operator': operator, 'left': left, 'right': right}
        return left

    def parse_factor(self):
        if self.match('NUMBER'):
            return {'type': 'Literal', 'value': self.consume()['value']}
        if self.match('OPERATOR') and self.tokens[self.index]['value'] == '(':
            self.consume()  
            expr = self.parse_expression()
            if not self.match('OPERATOR') or self.tokens[self.index]['value'] != ')':
                print(f"Expected ')' at position {self.index}")
            else:
                self.consume() 
            return expr
        print(f"Unexpected token at position {self.index}, skipping...")
        self.synchronize()
        return None

    def match(self, type):
        return self.index < len(self.tokens) and self.tokens[self.index]['type'] == type

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def synchronize(self):
        while self.index < len(self.tokens) and self.tokens[self.index]['type'] != 'END':
            self.index += 1
        if self.match('END'):
            self.consume() 


class Evaluator:
    def evaluate(self, node):
        if not node:
            return 0

        if node['type'] == 'Literal':
            return node['value']

        if node['type'] == 'BinaryExpression':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])

            if node['operator'] == '+':
                return left + right
            if node['operator'] == '-':
                return left - right
            if node['operator'] == '*':
                return left * right
            if node['operator'] == '/':
                if right == 0:
                    print('Division by zero error')
                    return 0
                return left / right
        return 0



def calculate(input):
    lexer = Lexer(input)
    tokens = lexer.tokenize()
    print('Tokens:', tokens)

    parser = Parser(tokens)
    ast = parser.parse_expression()
    print('AST:', ast)

    evaluator = Evaluator()
    result = evaluator.evaluate(ast)
    print('Result:', result)


# Sample input
calculate('5 + 3 * 2 - 1;')  
calculate('5 + * 3;')        
