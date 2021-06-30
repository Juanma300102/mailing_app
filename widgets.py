import tkinter as tk
from style import Style
from tkinter import font
from tkinter import ttk

def _has_hint(hint):
    return True if hint is not None else False

class Entry(tk.Entry):
    def __init__(self, _master, show_=None, hint=None):
        tk.Entry.__init__(self, master=_master)
        self.strVar = tk.StringVar(self)
        self.configure(textvariable=self.strVar)
        self.style = _master.style
        self.configure(relief=tk.FLAT,
                       bg=self.style.BG_COLOR_LIGHT,
                       fg=self.style.TEXT_COLOR,
                       highlightcolor=self.style.ACCENT_COLOR,
                       highlightbackground=self.style.BG_COLOR_DARKER,
                       show=show_)  # for password entries
        self.hint = hint
        self.show = show_
        self._set_event_if_hint(self.hint)

    def _clear_hint(self, event):
        if _has_hint(self.hint):
            if self.strVar.get() == self.hint:
                self.strVar.set('')
        if self.show is not None:
            self.configure(show=self.show)
        self.configure(fg=self.style.TEXT_COLOR)

    def _show_hint(self, var):
        # print(len(var.get()), self.focus_get(), self)
        if len(var.get()) == 0 and self.focus_get() != self:
            if self.show is not None:
                self.configure(show='')
            self.configure(fg=self.style.HINT_COLOR)
            self.insert(0, self.hint)

    def _set_event_if_hint(self, hint):
        if _has_hint(hint):
            self._show_hint(self.strVar)
            self.bind('<FocusIn>', self._clear_hint)
            self.strVar.trace('w', lambda name, index, mode, var=self.strVar: self._show_hint(var))
            self.bind('<FocusOut>', lambda name, var=self.strVar: self._show_hint(var))


class Title(tk.Label):
    def __init__(self, _master, _text=''):
        tk.Label.__init__(self, master=_master, text=_text)
        self.style = _master.style
        self.configure(bg=self.style.BG_COLOR,
                       fg=self.style.TITLE_COLOR,
                       font=self.style.TITLES)


class Button(tk.Button):
    def __init__(self, _master, _text = None, _command = None):
        tk.Button.__init__(self, master=_master, text=_text, command=_command)
        self.style = _master.style
        self.configure(bg=self.style.ACCENT_COLOR_DARKER,
                       activebackground=self.style.ACCENT_COLOR,
                       fg=self.style.TEXT_COLOR,
                       activeforeground=self.style.TEXT_COLOR,
                       relief=self.style.relief,
                       highlightbackground=self.style.BG_COLOR)


class MultiColumnListbox(object):
    def __init__(self, headers):
        self.fontsAndColors = Style()
        self.tree = None
        self.headers = headers
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        self.tree = ttk.Treeview(columns=self.headers, show="headings")

    def _build_tree(self):
        for col in self.headers:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=font.Font().measure(col.title()))


class LabelFrame(tk.LabelFrame):
    def __init__(self, _master, _text=None):
        tk.LabelFrame.__init__(self, master=_master, text=_text)
        self.style = _master.style
        self.configure(bg=self.style.BG_COLOR,
                       fg=self.style.TEXT_COLOR,
                       relief=self.style.relief,
                       pady=5,
                       padx=5)

    def adjust_grid_weight(self):
        self.columnconfigure([i for i in range(0, self.grid_size()[0])], weight=1)
        self.rowconfigure([i for i in range(0, self.grid_size()[1])], weight=1)


class Text(tk.Text):
    def __init__(self, _master):
        tk.Text.__init__(self, master=_master)
        self.style = _master.style
        self.configure(bg=self.style.BG_COLOR_LIGHT,
                       fg=self.style.TEXT_COLOR,
                       relief=self.style.relief,
                       highlightcolor=self.style.ACCENT_COLOR,
                       highlightbackground=self.style.BG_COLOR,
                       height=10)

    def get_content(self):
        content = self.get('1.0', tk.END)
        return content
