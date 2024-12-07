import keyword
import re

def find_invalid_identifiers(file_path):
    with open(file_path, 'r') as file:
        input_string = file.read()
        
  
    input_string = re.sub(r"#include<.*?>|using namespace std;|void main\(\)|\bint\b|\bfloat\b|[{};=+*,.]", "", input_string)
    
    
   
    potential_identifiers = input_string.split()
    
    
    valid_identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]{0,9}$')
    
    
    reserved_words = set(keyword.kwlist + ['int', 'float', 'double', 'char', 'void', 'return', 'namespace', 'std', 'main'])
    
    
    invalid_identifiers = []
    
    for identifier in potential_identifiers:
        
        if identifier in reserved_words:
            invalid_identifiers.append(identifier)
        elif not valid_identifier_pattern.match(identifier):
            invalid_identifiers.append(identifier)
    
    return invalid_identifiers


file_path = 'input.txt'
invalid_identifiers = find_invalid_identifiers(file_path)
print("Invalid Identifiers:", invalid_identifiers)
