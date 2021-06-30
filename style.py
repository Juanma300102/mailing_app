import tkinter
import tkinter.font as tkFont

class Style(object):
    def __init__(self):
        self._set_fonts()
        self._set_colors()
        self._set_relief()

    def _set_fonts(self):
        self.TITLES = tkFont.Font(family='Ubuntu', size=26, weight='bold')

    def _set_colors(self):
        self.BG_COLOR = '#202020'
        self.BG_COLOR_LIGHT = '#303030'
        self.BG_COLOR_DARKER = '#171717'
        self.TITLE_COLOR = '#707070'
        self.TEXT_COLOR = '#FFFFFF'
        self.HINT_COLOR = '#808080'
        self.ACCENT_COLOR = '#3B83DB'
        self.ACCENT_COLOR_DARKER = '#19375C'

    def _set_relief(self):
        self.relief = tkinter.FLAT
