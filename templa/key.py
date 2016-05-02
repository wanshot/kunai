# -*- coding: utf-8 -*-

import curses


# class KeyHandler(object):
#
#     def __init__(self, stdscr):
#         self.stdscr = stdscr
#
#     def get_key_for(self, ch):
#         k = None
#
#         if self.is_displayable_key(ch):
#             k = self.displayable_key_to_str(ch)
#         elif ch in SPECIAL_KEYS:
#             k = SPECIAL_KEYS[ch]
#         elif self.is_ctrl_masked_key(ch):
#             k = self.ctrl_masked_key_to_str(ch)
#         elif ch == KEY_ESCAPE:
#             if escaped:
#                 k = "ESC"
#             else:
#                 k = "M-" + self.get_key_for(self.screen.getch(), escaped = True)
#         elif ch == -1:
#             k = "C-c"
#         return k
#
#     def get_key(self):
#

