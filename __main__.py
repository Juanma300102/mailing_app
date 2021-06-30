import os
import tkinter as tk
from Screens.login_screen import LoginScreen
from Screens.main_menu import Menu
from Screens.mailing_screen import MailingScreen
from Screens.testings_screen import TestScreen

class Main(object):
    def __init__(self):
        self.root = tk.Tk()
        self.mailingScreen = MailingScreen(self.root)
        self.root.columnconfigure([i for  i in range(0, self.root.grid_size()[0])], weight=1)
        self.root.rowconfigure([i for i in range(0, self.root.grid_size()[1])], weight=1)

        while True:
            try:
                self.root.update()
                self.root.update_idletasks()
            except:
                print('Exited')
                break

    def _set_constants(self):
        self.ROOT_PROJECT_PATH = os.path.abspath('__main__.py')


if __name__ == '__main__':
    main = Main()
