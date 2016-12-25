# -*- coding: utf-8 -*-
import collections
from math import ceil


class Paginator(object):

    def __init__(self, object_list, per_page):
        self.object_list = object_list
        self.per_page = per_page

    def page(self, number):
        """Returns a Page object for the given 1-based page number.
        """
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top >= self.count:
            top = self.count
        return self._get_page(self.object_list[bottom:top], number, self)

    def _get_page(self, *args, **kwargs):
        """
        Returns an instance of a single page.
        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)

    @property
    def count(self):
        """
        Returns the total number of objects, across all pages.
        """
        return len(self.object_list)

    @property
    def num_pages(self):
        """
        Returns the total number of pages.
        """
        if self.count == 0:
            return 0
        hits = max(1, self.count)
        return int(ceil(hits / float(self.per_page)))


class Page(collections.Sequence):

    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1

    def start_index(self):
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page
