import re


class Token:
    def __init__(self, token_type, value, line_number):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number

    def __str__(self):
        return f"Token(Type: {self.token_type}, Value: '{self.value}', Line: {self.line_number})"


class Lexer:
    def __init__(self, code):
        self.code = code
        self.current_position = 0
        self.line_number = 1
        self.keywords = {"int", "float", "char", "if", "else", "while", "for", "return"}
        self.operators = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "!"}
        self.separators = {"(", ")", "{", "}", "[", "]", ",", ";"}

    def get_next_char(self):
        if self.current_position < len(self.code):
            return self.code[self.current_position]
        return None

    def advance(self):
        if self.get_next_char() == '\n':
            self.line_number += 1
        self.current_position += 1

    def match(self, expected_char):
        if self.get_next_char() == expected_char:
            self.advance()
            return True
        return False

    def skip_whitespace_and_comments(self):
        while self.get_next_char() and (self.get_next_char().isspace() or 
                                        self.code[self.current_position:self.current_position+2] in {"//", "/*"}):
            if self.code[self.current_position:self.current_position+2] == "//":
                self.advance()
                self.advance()
                while self.get_next_char() and self.get_next_char() != '\n':
                    self.advance()
            elif self.code[self.current_position:self.current_position+2] == "/*":
                self.advance()
                self.advance()
                while self.get_next_char() and self.code[self.current_position:self.current_position+2] != "*/":
                    if self.get_next_char() == '\n':
                        self.line_number += 1
                    self.advance()
                if self.get_next_char():
                    self.advance()
                    self.advance()
            else:
                self.advance()

    def get_identifier_or_keyword(self):
        start_pos = self.current_position
        while self.get_next_char() and (self.get_next_char().isalnum() or self.get_next_char() == '_'):
            self.advance()
        lexeme = self.code[start_pos:self.current_position]
        if lexeme in self.keywords:
            return Token("Keyword", lexeme, self.line_number)
        return Token("Identifier", lexeme, self.line_number)

    def get_number_literal(self):
        start_pos = self.current_position
        is_float = False
        while self.get_next_char() and (self.get_next_char().isdigit() or self.get_next_char() == '.'):
            if self.get_next_char() == '.':
                if is_float:
                    break
                is_float = True
            self.advance()
        lexeme = self.code[start_pos:self.current_position]
        if lexeme.count('.') > 1:  
            self.error(f"Malformed floating-point literal: {lexeme}")
            return None
        token_type = "FloatLiteral" if is_float else "IntegerLiteral"
        return Token(token_type, lexeme, self.line_number)

    def get_operator(self):
        start_pos = self.current_position
        lexeme = ""
        while self.get_next_char() and self.code[start_pos:self.current_position+1] in self.operators:
            lexeme += self.get_next_char()
            self.advance()
        if lexeme in self.operators:
            return Token("Operator", lexeme, self.line_number)
        else:
            self.error(f"Invalid operator: {lexeme}")
            return None

    def get_char_literal(self):
        if self.match("'"):
            char = self.get_next_char()
            if char == '\\': 
                self.advance()
                char += self.get_next_char()
            self.advance()
            if self.match("'"):
                return Token("CharLiteral", char, self.line_number)
            else:
                self.error("Unclosed character literal.")
                return None
        else:
            self.error("Invalid character literal.")
            self.advance()
            return None

    def get_separator(self):
        lexeme = self.get_next_char()
        self.advance()
        return Token("Separator", lexeme, self.line_number)

    def get_next_token(self):
        self.skip_whitespace_and_comments()
        current_char = self.get_next_char()
        
        if not current_char:
            return None
        elif current_char.isalpha() or current_char == '_':
            return self.get_identifier_or_keyword()
        elif current_char.isdigit():
            return self.get_number_literal()
        elif current_char == "'":
            return self.get_char_literal()
        elif current_char in self.operators:
            return self.get_operator()
        elif current_char in self.separators:
            return self.get_separator()
        else:
            self.error(f"Unrecognized character '{current_char}'")
            self.advance()

    def tokenize(self):
        tokens = []
        while self.current_position < len(self.code):
            token = self.get_next_token()
            if token:
                tokens.append(token)
        return tokens

    def error(self, message):
        print(f"Error on line {self.line_number}: {message}")

# Example usage
code = """
int main() {
    int a = 5;
    float b = 3.14;
    char c = 'x';
    if (a > 0) {
        // This is a comment
        a = a + b * 2;
    }
    /* Multi-line
       comment */
    return a;
}
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)