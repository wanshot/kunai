# -*- coding: utf-8 -*-
from imp import load_source


templa_api_name = ["fly"]


class FuncLoader(object):

    def __init__(self):
        self.funcs_dict = {}
        self._load_file()
        self.add_instance_method()

    def add_instance_method(self):
        setattr(self, 'make_bm_table', self.funcs_dict["make_bm_table"])

    def _load_file(self):
        for key, value in self._load_templa().items():
            if key.startswith("__"):
                continue
            elif key in templa_api_name:
                continue
            else:
                self.funcs_dict[key] = value

    def _load_templa(self):
        return vars(load_source("mdl", "/Users/wan/__.py"))


class CallTemplaFunctions(FuncLoader):
    pass


if __name__ == "__main__":
    a = FuncLoader()
    print a.make_bm_table("aaa", "e")
