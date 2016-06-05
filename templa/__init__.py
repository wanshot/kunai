# -*- coding: utf-8 -*-

__version__ = '0.0.0'
__license__ = 'MIT License',
__author__ = 'wanshot'
__author_email__ = 'nishikawa0228@sj9.so-net.ne.jp'

__logo__ = """
   __                 __
  / /____ __ _  ___  / /__ _
 / __/ -_)  ' \/ _ \/ / _ `/
 \__/\__/_/_/_/ .__/_/\_,_/
             /_/
"""

from .core import Core


def fry(*args, **kwargs):
    # call @fry
    if len(args) == 1 and callable(args[0]):
        return Core(args[0], **kwargs)

    def inner(obj):
        # call @fry()
        return Core(obj, **kwargs)
    return inner
