import argparse
from pycparser import parse_file, c_generator
from scrambler import Scrambler

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='CScrambler',
        description='Simple C source code obfuscator.'
    )

    parser.add_argument('filename')
    parser.add_argument('-i', action='store_true', help='Obfuscate function and variable names', required=False)
    parser.add_argument('-s', action='store_true', help='Obfuscate string literals', required=False)
    parser.add_argument('-n', action='store_true', help='Obfuscate integer literals', required=False)
    parser.add_argument('-w', action='store_true', help='Remove optional whitespaces', required=False)

    args = parser.parse_args()

    filename = args.filename
    identifiers = args.i
    strings = args.s
    integers = args.n
    whitespaces = args.w

    if not (identifiers or strings or integers or whitespaces):
        identifiers = True
        strings = True
        integers = True
        whitespaces = True

    ast = parse_file(filename)
    ast.show(offset=2, attrnames=True)

    scrambler = Scrambler()
    scrambler.set_options(identifiers, strings, integers, whitespaces)
    scrambler.obfuscate(node=ast)

    gen = c_generator.CGenerator()
    output = gen.visit(ast)

    if whitespaces:
        output = scrambler.remove_whitespace(output)
    # output = output.replace('\n', '').replace('\r', '')
    # output = ' '.join(output.split())
    print(output)
        