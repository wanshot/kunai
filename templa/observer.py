# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ModelLisner(object):
    # XXX use pull type
    __metaclass__ = ABCMeta

    def __init(self, model, keyword, list_):
        self.model = model
        self.keyword = keyword
        self.list_ = list_

    def update(self):
        updated = [x for x in self.list_ if self.keyword in x]
        self.pages = self.model._create_pages(updated)
        self.page_number = 1
