# -*- coding: utf-8 -*-

import argparse
import textwrap
from parser import TemplaParser

LOGAPPNAME = "Interactive Shell Interface"


class TemplaRunner(object):
    """
    """

    def __init__(self):
        self.parser = TemplaParser()

    def show_commands(self):
        print u"Available commands:\n"
        for n, d in self.parser.commands:
            print u"    {name}  {docstring}".format(name=n,
                                                    docstring=d.replace('\n', ' '))

    def run(self):
        exec self.parser.code_obj

    @property
    def command_names(self):
        return zip(*self.parser.commands)[0]


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
        templa.parser.pick_command(args.command)
        templa.run()
    elif args.command is None:
        parser.print_help()
    else:
        print u"{command} is not templa command".format(command=args.command)
