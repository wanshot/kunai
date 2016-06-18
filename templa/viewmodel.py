# -*- coding: utf-8 -*-


class ViewModel(object):

    def __init__(self, pager, view):
        self._model = pager

    def move_next_page(self):
        """Command
        >>> _list = [u"hoge", u"huga", u"piyo", u'templa', u'sushi']
        >>> model = Model(_list, 5, 3)  # width, height
        >>> print model.current_page  # [u'hoge ', u'huga ']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'piyo ', u'templa']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'sushi']
        >>> model.move_next_page()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        self._model.set_current_page(self._model.next_page_number())

    def move_prev_page(self):
        """Command
        >>> _list = [u"hoge", u"huga", u"piyo", u'templa', u'sushi']
        >>> model = Model(_list, 5, 3)
        >>> print model.current_page  # [u'hoge ', u'huga ']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'sushi']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'piyo ', u'templa']
        >>> model.move_prev_page()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        self._model.set_current_page(self._model.prev_page_number())

    def update(self):
        """Command
        >>> _list = [u"hoge", u"huga", u"piyo"]
        >>> model = Model(_list, 5, 3) # width, height
        >>> model.query = "h"
        >>> model.update()
        >>> print model.current_page  # [u'hoge ', u'huga ']
        """
        new_order = [v for v in self._model.order if self._model.query in v]
        self._model.pages = self._model.create_pages(new_order)
        self._model.set_current_page(self._model.FIRST_PAGE_NUMBER)

    def set_query(self):
        """stub function
        """
        # TODO use tty read character
        # self.model.keyword += curses.ascii.unctrl(key).decode("utf-8")
        ch = self.view.ch
        if ch is not None:
            if self._model.query is None:
                self._model.query = ch.decode("utf-8")
            else:
                self._model.query += ch.decode("utf-8")

    @property
    def current_page(self):
        return self.model.current_page
