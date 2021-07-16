import os
import tkinter as tk
from Screens.login_screen import LoginScreen
from Screens.main_menu import Menu
from Screens.mailing_screen import MailingScreen
from Screens.login_screen import LoginScreen
from Screens.testings_screen import TestScreen
from common_services import INIManager

class Main(object):
    mailingScreen: MailingScreen
    def __init__(self):
        self.root = tk.Tk()
        self.login_screen = TestScreen(self.root)#LoginScreen(self.root, self)
        
        self.fix_columns()
        self.loop()

    def fix_columns(self):
        self.root.columnconfigure([i for  i in range(0, self.root.grid_size()[0])], weight=1)
        self.root.rowconfigure([i for i in range(0, self.root.grid_size()[1])], weight=1)

    def loop(self):
        while True:
            try:
                self.root.update()
                self.root.update_idletasks()
            except:
                print('exited')
                break
            

if __name__ == '__main__':
    main = Main()