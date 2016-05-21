# -*- coding: utf-8 -*-
import ast
import argparse
import textwrap
from manage import LoadConfig

LOGAPPNAME = "Interactive Shell Interface"


class TemplaRunner(object):

    def __init__(self, func_name):
        self.conf = LoadConfig()
        self.code_obj = self._pick_function(func_name)

    def _pick_function(self, func_name):

        file_name = self.conf.templa_file_path
        with open(file_name, "r") as f:
            code = f.read()

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == func_name:
                    return node

        exprs = ast.parse(code, self.conf.templa_file_path)
        _Transform().visit(exprs)
        return compile(exprs, self.conf.templa_file_path, "exec")

    def run(self):
        exec self.code_obj


def get_argparser():
    from templa import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='templa <function name>',
        description=textwrap.dedent(
            "{description}{logo}".format(description=LOGAPPNAME, logo=__logo__)),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    parser.add_argument('function_name', type=str)
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    return TemplaRunner(args.function_name).run()
