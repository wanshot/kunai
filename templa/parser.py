# -*- coding: utf-8 -*-

import ast

from config import Config


def add_method(cls, method):
    setattr(cls, method.__name__, method)


class ExecFileParser(object):

    def __init__(self):
        self.conf = Config()
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
