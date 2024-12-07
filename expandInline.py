import re

def tokenize_cpp_code(code):
    return [t for t in re.findall(r'inline|[a-zA-Z_]\w*|\d+|[+\-*/=;{}(),]', code) if not t.isspace()]

def parse_inline_functions(tokens):
    inline_functions, i = {}, 0     #inline_functions["add"] = ([("int", "a"), ("int", "b")], ["return a + b;"])
    while i < len(tokens):
        if tokens[i] == 'inline':
            name = tokens[i + 2]
            params, i = [], i + 4
            while tokens[i] != ')':
                params.append((tokens[i], tokens[i + 1]))
                i += 3 if tokens[i + 2] == ',' else 2
            body_start, i = i + 2, i + 2
            while tokens[i] != '}':
                i += 1
            inline_functions[name] = (params, tokens[body_start:i])
        i += 1
    return inline_functions

def expand_inline_functions(code, inline_functions):
    tokens, i, result = tokenize_cpp_code(code), 0, []
    while i < len(tokens):
        if tokens[i] in inline_functions:
            params, body, args, i = *inline_functions[tokens[i]], [], i + 2
            while tokens[i] != ')':
                args.append(tokens[i])
                i += 2 if tokens[i + 1] == ',' else 1
            body_str = ' '.join([' '.join(body).replace(pname, arg) for (ptype, pname), arg in zip(params, args)])
            result.append(body_str)
            i += 1
        else:
            result.append(tokens[i])
        i += 1
    return ' '.join(result)

def main():
    with open('input.cpp') as f:
        code = f.read()
    inline_functions = parse_inline_functions(tokenize_cpp_code(code))
    expanded_code = expand_inline_functions(code, inline_functions)
    with open('output.cpp', 'w') as f:
        f.write(expanded_code)

if __name__ == '__main__':
    main()
