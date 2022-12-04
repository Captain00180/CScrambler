import argparse
from pycparser import parse_file, c_generator
from scrambler import Scrambler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='CScrambler',
        description='Simple C source code obfuscator.'
    )

    parser.add_argument('filename')

    args = parser.parse_args()
    print(args)

    ast = parse_file('pycparser-master/examples/c_files/test.c')
    ast.show(offset=2, attrnames=True)

    scrambler = Scrambler()
    scrambler.traverse(node=ast)

    gen = c_generator.CGenerator()
    output = gen.visit(ast)
    output = output.replace('\n', '').replace('\r', '')
    output = ' '.join(output.split())
    print(output)
        