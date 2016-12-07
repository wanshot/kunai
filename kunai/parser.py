# -*- coding: utf-8 -*-

import ast
import inspect

import __future__
PyCF_MASK = sum(v for k, v in vars(__future__).items() if k.startswith('CO_FUTURE'))

from config import Config


class ExecFileParser(object):

    def __init__(self):
        self.conf = Config()
        self.commands = self._load_commands()
        self.code_obj = None

    def _get_kunai_code(self):
        file_name = self.conf.kunai_file_path
        with open(file_name, 'r') as f:
            code = f.read()
        return code

    def _load_commands(self):
        ret = []

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                ret.append((node.name, ast.get_docstring(node)))
        exprs = ast.parse(self._get_kunai_code(), self.conf.kunai_file_path)
        _Transform().visit(exprs)
        # TODO funcitons overlap raise
        return ret

    def pick_command(self, command):

        class _Transform(ast.NodeTransformer):

            def visit_FunctionDef(self, node):
                if node.name == command:
                    return node

        exprs = ast.parse(self._get_kunai_code(), self.conf.kunai_file_path)
        _Transform().visit(exprs)
        self.code_obj = compile(exprs, self.conf.kunai_file_path, 'exec')

    def set_importmodule_code(self, code_obj):
        """set import module code
        """
        source = self._uncompile(code_obj)
        s = ['from kunai import render']
        s.extend(source)
        exprs = ''
        for line in s:
            exprs += line + '\n'
        self.code_obj = compile(exprs, '<kunai>', 'exec')

    def _uncompile(self, code_obj):
        """uncompile(codeobj) -> source
        """
        if code_obj.co_flags & inspect.CO_NESTED or code_obj.co_freevars:
            # XXX
            raise TypeError('nested functions not supported')
        if code_obj.co_name == '<lambda>':
            raise TypeError('lambda functions not supported')
        if code_obj.co_filename == '<string>':
            raise TypeError('code without source file not supported')

        try:
            lines = inspect.getsourcelines(code_obj)[0]
        except IOError:
            # XXX
            raise TypeError('source code not available')

        return lines
