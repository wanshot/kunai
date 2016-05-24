# -*- coding: utf-8 -*-
import ast
import argparse
import textwrap
from config import LoadConfig

LOGAPPNAME = "Interactive Shell Interface"


class TemplaRunner(object):
    """
    """

    def __init__(self):
        self.conf = LoadConfig()
        self.commands = self._load_commands()
        self.code_obj = None

    def _get_templa_code(self):
        file_name = self.conf.templa_file_path
        with open(file_name, "r") as f:
            code = f.read()
        return code

    def _load_commands(self):
        ret = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                ret.append((node.name, ast.get_docstring(node)))
        exprs = ast.parse(self._get_templa_code(), self.conf.templa_file_path)
        _Transform().visit(exprs)
        # TODO funcitons overlap raise
        return ret

    def pick_command(self, command):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == command:
                    return node

        exprs = ast.parse(self._get_templa_code(), self.conf.templa_file_path)
        _Transform().visit(exprs)
        self.code_obj = compile(exprs, self.conf.templa_file_path, "exec")

    def show_commands(self):
        print u"Available commands:\n"
        for n, d in self.commands:
            print u"    {name}  {docstring}".format(name=n,
                                                    docstring=d.replace('\n', ' '))

    def run(self):
        exec self.code_obj

    @property
    def command_names(self):
        return zip(*self.commands)[0]


def get_argparser():
    from templa import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='templa <command>',
        description=textwrap.dedent(
            "{description}{logo}".format(description=LOGAPPNAME, logo=__logo__)),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    # List templa commands found in loaded templafiles/source files
    parser.add_argument('-l', '--list',
                        action='store_true',
                        default=False,
                        help="print list of possible commands and exit")

    parser.add_argument('command',
                        nargs="?",
                        type=str)

    return parser


def main():
    templa = TemplaRunner()
    parser = get_argparser()
    args = parser.parse_args()
    if args.list:
        templa.show_commands()
    elif args.command in templa.command_names:
        templa.pick_command(args.command)
        templa.run()
    elif args.command is None:
        parser.print_help()
    else:
        print u"{command} is not templa command".format(command=args.command)
