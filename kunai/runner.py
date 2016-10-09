# -*- coding: utf-8 -*-

import argparse
import textwrap
from ansi import term
from parser import ExecFileParser

LOGAPPNAME = "Interactive Shell Interface"


class KunaiRunner(object):
    """
    """

    def __init__(self):
        self.parser = ExecFileParser()

    def show_commands(self):
        print u"Available commands:\n"
        for n, d in self.parser.commands:
            print u"    {name}  {docstring}".format(
                name=n,
                docstring=d.replace('\n', ' ')
            )

    def run(self):
        exec self.parser.code_obj

    @property
    def command_names(self):
        return zip(*self.parser.commands)[0]


def get_argparser():
    from kunai import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='kunai <command>',
        description=textwrap.dedent(
            term(LOGAPPNAME, fg_color="red") +
            term(__logo__, fg_color="red", style="bold")
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    # List kunai commands found in loaded kunaifiles/source files
    parser.add_argument('-l', '--list',
                        action='store_true',
                        default=False,
                        help="print list of possible commands and exit")

    parser.add_argument('command',
                        nargs="?",
                        type=str)

    return parser


def main():
    kunai = KunaiRunner()
    parser = get_argparser()
    args = parser.parse_args()
    if args.list:
        kunai.show_commands()
    elif args.command in kunai.command_names:
        kunai.parser.pick_command(args.command)
        kunai.run()
    elif args.command is None:
        parser.print_help()
    else:
        print u"{command} is not kunai command".format(command=args.command)
