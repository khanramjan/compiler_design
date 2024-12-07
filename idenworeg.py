KEYWORDS = {'int', 'float', 'if', 'else', 'while', 'return'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '&&', '||'}
SEPARATORS = {';', ',', '(', ')', '{', '}'}

def categorize_token(token):
    if token in KEYWORDS:
        return f"{token} (keyword)"
    elif token in OPERATORS:
        return f"{token} (operator)"
    elif token in SEPARATORS:
        return f"{token} (separator)"
    elif token.isidentifier() and not token.isdigit():
        return f"{token} (identifier)"
    elif token.isdigit():
        return f"{token} (integer literal)"
    elif '.' in token and all(part.isdigit() for part in token.split('.') if part):
        return f"{token} (floating-point literal)"
    elif token.startswith('"') and token.endswith('"'):
        return f"{token} (string literal)"
    return f"{token} (unknown)"

def tokenize_and_categorize(input_string):
    tokens, current_token = [], ""
    for char in input_string:
        if char.isspace():
            if current_token: tokens.append(current_token); current_token = ""
        elif char in OPERATORS | SEPARATORS:
            if current_token: tokens.append(current_token); current_token = ""
            tokens.append(char)
        else:
            current_token += char
    if current_token: tokens.append(current_token)
    return [categorize_token(token) for token in tokens]

def process_file(filename):
    with open(filename, 'r') as file:
        input_code = file.read()
    for token in tokenize_and_categorize(input_code):
        print(token)

process_file('idenfyToken.txt')
