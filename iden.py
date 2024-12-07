import keyword
import re

def find_invalid_identifiers(file_path):
    with open(file_path, 'r') as file:
        input_string = file.read()
        
    # Remove known C++ headers, keywords, and common operators that aren't identifiers
    input_string = re.sub(r"#include<.*?>|using namespace std;|int main\(\)|\bint\b|\bcout\b|\bend\b|[{};=+]", "", input_string)
    
    # Split remaining text by whitespace to get potential identifiers
    potential_identifiers = input_string.split()
    
    # Define a pattern for valid identifiers (following typical identifier naming conventions)
    valid_identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]{0,9}$')
    
    # Combine Python keywords and commonly used C++ keywords
    reserved_words = set(keyword.kwlist + ['int', 'float', 'str', 'bool', 'list', 'dict', 'set', 'tuple', 'cout', 'endl', 'namespace', 'std', 'main'])
    
    # List to store invalid identifiers
    invalid_identifiers = []
    
    for identifier in potential_identifiers:
        # Check if it's a reserved word or does not match valid identifier pattern
        if identifier in reserved_words:
            invalid_identifiers.append(identifier)
        elif not valid_identifier_pattern.match(identifier):
            invalid_identifiers.append(identifier)
    
    return invalid_identifiers

# Example usage
file_path = 'input.txt'
invalid_identifiers = find_invalid_identifiers(file_path)
print("Invalid Identifiers:", invalid_identifiers)
