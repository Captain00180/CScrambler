from random import shuffle, randint

from pycparser import c_ast


class Scrambler:
    def __init__(self):
        # Dictionary containing mappings of old names to new names
        # key: old name
        # value: new name
        self.id_table = {}

    def traverse(self, node):
        if isinstance(node, (c_ast.Decl, c_ast.ID)):
            node.name = self.scramble_name(node.name, node.coord.column, node.coord.line)
        elif isinstance(node, c_ast.TypeDecl):
            # Variable declaration
            node.declname = self.scramble_name(node.declname, node.coord.column, node.coord.line)

        elif isinstance(node, c_ast.Constant):
            if node.type == 'string':
                node.value = self.scramble_string(node.value)
            if node.type == 'int':
                node.value = self.scramble_int(node.value)

        for child in node:
            self.traverse(child)

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

    def scramble_string(self, string):
        # Transforms the string to a sequence of escaped hex bytes
        res = ''
        for char in string:
            if char == '"':
                res += char
                continue
            res += r'\x' + f'{hex(ord(char))[2:]}'
        return res

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