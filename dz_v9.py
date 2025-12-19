import argparse
import sys
from typing import Any, Dict, List, Tuple, Optional

import lark
import tomli_w

grammar = r"""
start: statement*

statement: NAME ":" value

?value: number
      | string
      | dict
      | expr

number: SCI_NUMBER | INT_NUMBER
string: STRING
dict: "struct" "{" [dict_item ("," dict_item)*] "}"
dict_item: NAME "=" value
expr: "!" "(" infix_expr ")"

?infix_expr: infix_expr "+" term   -> add
           | infix_expr "-" term   -> sub
           | term

?term: mod_call
     | atom

mod_call: "mod" "(" infix_expr "," infix_expr ")"

?atom: NUMBER        -> number_expr
     | NAME          -> name_expr
     | "(" infix_expr ")"

SCI_NUMBER: /[+-]?\d+(\.\d*)?[eE][+-]?\d+/
INT_NUMBER: /[+-]?\d+/
NUMBER: /[+-]?\d+/
NAME: /[a-z][a-z0-9_]*/
STRING: /\"[^\"]*\"/

%ignore /\*>[^\n]*/     # комментарии вариант 9
%ignore /[ \t\r\n]+/
"""

class BuildAST(lark.Transformer):
    def start(self, items):
        return items
    
    def statement(self, items):
        name, value = items
        return (str(name), value)
    
    def number(self, items):
        (token,) = items
        if 'e' in token.lower():
            return float(token)
        return int(token)
    
    def string(self, items):
        (token,) = items
        s = str(token)
        return s[1:-1]
    
    def dict(self, items):
        return ("dict", items)
    
    def dict_item(self, items):
        name, value = items
        return (str(name), value)
    
    def expr(self, items):
        (node,) = items
        return ("expr", node)
    
    def number_expr(self, items):
        (token,) = items
        return ("num", int(token))
    
    def name_expr(self, items):
        (token,) = items
        return ("name", str(token))
    
    def add(self, items):
        left, right = items
        return ("+", left, right)
    
    def sub(self, items):
        left, right = items
        return ("-", left, right)
    
    def mod_call(self, items):
        a, b = items
        return ("mod", a, b)

def eval_config(ast: List[Tuple[str, Any]]) -> Dict[str, Any]:
    env: Dict[str, Any] = {}
    result: Dict[str, Any] = {}
    
    def eval_value(node: Any) -> Any:
        if isinstance(node, (int, float)):
            return node
        if isinstance(node, str):
            return node
        if isinstance(node, tuple):
            tag = node[0]
            if tag == "dict":
                dict_items = {}
                for name, value_node in node[1]:
                    dict_items[name] = eval_value(value_node)
                return dict_items
            if tag == "expr":
                return eval_expr(node[1])
        raise ValueError(f"invalid value node {node!r}")
    
    def eval_expr(node: Any) -> int:
        tag = node[0]
        if tag == "num":
            return node[1]
        if tag == "name":
            name = node[1]
            if name not in env:
                raise ValueError(f"unknown constant {name}")
            value = env[name]
            if not isinstance(value, (int, float)):
                raise ValueError(f"constant {name} is not numeric")
            return value
        if tag in {"+", "-"}:
            a = eval_expr(node[1])
            b = eval_expr(node[2])
            if tag == "+":
                return a + b
            else:
                return a - b
        if tag == "mod":
            a = eval_expr(node[1])
            b = eval_expr(node[2])
            return a % b
        raise ValueError(f"invalid expr node {node!r}")
    
    for name, value_ast in ast:
        value = eval_value(value_ast)
        env[name] = value
        result[name] = value
    
    return result

parser = lark.Lark(grammar, parser="lalr")

def main(argv: Optional[List[str]] = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Input config file")
    args = ap.parse_args(argv)
    
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"cannot open input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        tree = parser.parse(text)
    except lark.LarkError as e:
        print(f"syntax error: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        ast = BuildAST().transform(tree)
        data = eval_config(ast)
    except Exception as e:
        print(f"semantic error: {e}", file=sys.stderr)
        sys.exit(1)
    
    with open("result.toml", "w", encoding="utf-8") as f:
        f.write(tomli_w.dumps(data))
    print("Successfully written to result.toml")

if __name__ == "__main__":
    main()