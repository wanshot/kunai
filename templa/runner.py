# -*- coding: utf-8 -*-
import ast
import argparse
from manage import LoadConfig

TEMPLA_LOGO = """
 _________    _______       _____ ______       ________    ___           ________
|\___   ___\ |\  ___ \     |\   _ \  _   \    |\   __  \  |\  \         |\   __  \
\|___ \  \_| \ \   __/|    \ \  \\\__\ \  \   \ \  \|\  \ \ \  \        \ \  \|\  \
     \ \  \   \ \  \_|/__   \ \  \\|__| \  \   \ \   ____\ \ \  \        \ \   __  \
      \ \  \   \ \  \_|\ \   \ \  \    \ \  \   \ \  \___|  \ \  \____    \ \  \ \  \
       \ \__\   \ \_______\   \ \__\    \ \__\   \ \__\      \ \_______\   \ \__\ \__\
        \|__|    \|_______|    \|__|     \|__|    \|__|       \|_______|    \|__|\|__|
"""


class TemplaRunner(object):

    def __init__(self, func_name):
        self.fucn_name = func_name
        self.conf = LoadConfig()
        self.code_obj = self._pick_function()

    def _pick_function(self):

        file_name = self.conf.templa_file_path
        with open(file_name, "r") as f:
            code = f.read()

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == self.func_name:
                    return node

        exprs = ast.parse(code, self.conf.templa_file_path)
        _Transform().visit(exprs)
        return compile(exprs, self.conf.templa_file_path, "exec")

    def run(self):
        exec self.code_obj


def get_argparser():
    parser = argparse.ArgumentParser(description=TEMPLA_LOGO)
    parser.add_argument('function_name', type=str, help='Function Name')
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    return TemplaRunner(args.function_name).run()
