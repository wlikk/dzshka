import sys
import argparse
import toml
from lark import Lark, Transformer

GRAMMAR = r"""
    start: (comment | item)*
    item: NAME ":" value
    value: STRING | NUMBER | BOOL | struct
    struct: "struct" "{" pair ("," pair)* "}"
    pair: NAME "=" value
    
    STRING: /"[^"]*"/
    NUMBER: /[+-]?\d+(\.\d+)?/
    BOOL: "true" | "false"
    NAME: /[a-z]+/
    comment: "*>" /[^\n]*/
    
    %ignore " "
    %ignore "\\t"
    %ignore "\\n"
    %ignore comment
"""

class T(Transformer):
    def start(self, items):
        return dict(items)
    def item(self, items):
        return (items[0], items[1])
    def struct(self, items):
        return dict(items)
    def pair(self, items):
        return (items[0], items[1])
    def STRING(self, t):
        return str(t)[1:-1]
    def NUMBER(self, t):
        return float(t) if '.' in t else int(t)
    def BOOL(self, t):
        return str(t) == "true"
    NAME = str

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    
    text = sys.stdin.read()
    parser = Lark(GRAMMAR, parser='lalr', transformer=T())
    result = parser.parse(text)
    
    with open(args.output, 'w') as f:
        toml.dump(result, f)
    
    print(f"Сохранено в {args.output}")

if __name__ == '__main__':
    main()
