##############################################
#    Simple C source code obfuscator class   #
#                                            #
#        Defines the class and methods       #
#           of the Obfuscator class          #
#           Author: Filip Januska            #
##############################################
from random import shuffle, randint
from pycparser import c_ast


class Scrambler:
    def __init__(self):
        # Dictionary containing mappings of old names to new names
        # key: old name
        # value: new name
        self.id_table = {}
        self.identifiers = True
        self.strings = True
        self.integers = True
        self.whitespaces = True

    # Set the methods of obfuscation to be applied
    def set_options(self, identifiers, strings, integers, whitespaces):
        self.identifiers = identifiers
        self.strings = strings
        self.integers = integers
        self.whitespaces = whitespaces

    # Recursively apply obfuscation methods
    def obfuscate(self, node):
        if isinstance(node, (c_ast.Decl, c_ast.ID)) and self.identifiers:
            node.name = self.scramble_name(node.name, node.coord.column, node.coord.line)
        elif isinstance(node, c_ast.TypeDecl) and self.identifiers:
            node.declname = self.scramble_name(node.declname, node.coord.column, node.coord.line)

        elif isinstance(node, c_ast.Constant):
            if node.type == 'string' and self.strings:
                node.value = self.scramble_string(node.value)
            if node.type == 'int' and self.integers:
                node.value = self.scramble_int(node.value)

        for child in node:
            self.obfuscate(child)

    # Obfuscates identifiers
    def scramble_name(self, name, x, y):
        if name == 'main':
            return name
        if name in self.id_table:
            # Name has already been remapped, reuse it from the id_table
            return self.id_table[name]

        # Name hasn't been mapped yet, map it now
        new_name = list(f'{"O"*x}{"0"*y}')
        shuffle(new_name)
        new_name = 'O' + ''.join(new_name)
        self.id_table[name] = new_name
        return new_name

    # Obfuscates string literals
    def scramble_string(self, string):
        # Transforms the string to a sequence of escaped hex bytes
        res = ''
        for char in string:
            if char == '"':
                res += char
                continue
            res += r'\x' + f'{hex(ord(char))[2:]}'
        return res

    # Obfuscates integer literals
    def scramble_int(self, num):
        def xor_obfuscate(x, iterations):
            if iterations <= 0:
                return x, 0
            y = randint(1, 50000)
            z = x ^ y
            return z, *xor_obfuscate(y, iterations - 1)

        # Converts the int literal to octal and adds multiple XOR obfuscations
        num = int(num)
        num_list = xor_obfuscate(num, 10)[:-1]
        return '(' + '^'.join([oct(x).replace("o", "") for x in num_list]) + ')'

    # Removes optional whitespaces
    def remove_whitespace(self, input):
        input = input.replace('\n', '').replace('\r', '')
        return ' '.join(input.split())