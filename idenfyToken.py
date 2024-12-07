KEYWORDS = {'int', 'float', 'if', 'else', 'while', 'return'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '&&', '||'}
SEPARATORS = {';', ',', '(', ')', '{', '}'}

def is_identifier(token):
    
    if token and (token[0].isalpha() or token[0] == '_'):
        return all(char.isalnum() or char == '_' for char in token[1:])
    return False

def is_integer_literal(token):
 
    return token.isdigit()

def is_float_literal(token):
   
    if '.' in token:
        parts = token.split('.')
        return len(parts) == 2 and all(part.isdigit() for part in parts)
    return False

def is_string_literal(token):

    return token.startswith('"') and token.endswith('"')

def categorize_token(token):
    if token in KEYWORDS:
        return f"{token} (keyword)"
    elif token in OPERATORS:
        return f"{token} (operator)"
    elif token in SEPARATORS:
        return f"{token} (separator)"
    elif is_identifier(token):
        return f"{token} (identifier)"
    elif is_integer_literal(token):
        return f"{token} (integer literal)"
    elif is_float_literal(token):
        return f"{token} (floating-point literal)"
    elif is_string_literal(token):
        return f"{token} (string literal)"
    return f"{token} (unknown)"

def tokenize_and_categorize(input_string):

    tokens = []
    current_token = ""
    
    for char in input_string:
        if char.isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif char in OPERATORS or char in SEPARATORS:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        else:
            current_token += char
    
    if current_token:
        tokens.append(current_token)

    categorized_tokens = [categorize_token(token) for token in tokens]
    return categorized_tokens

def process_file(filename):
    with open(filename, 'r') as file:
        input_code = file.read()

    categorized_tokens = tokenize_and_categorize(input_code)
    for token in categorized_tokens:
        print(token)

filename = 'idenfyToken.txt'
process_file(filename)
