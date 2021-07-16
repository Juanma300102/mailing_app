import configparser
import os
from common_services import INIManager

class StartOptionsGUIController(object):
    def __init__(self, _master):
        self.master = _master
        self.options = configparser.ConfigParser()
        self.options.read(os.path.join(os.getcwd(),'options.ini'))
        
    def get_options_sections(self):
        return self.options.sections()

    def get_user_remind(self):
        return self.options.getboolean('DEFAULT', 'user_remind')

    def get_user(self):
        return self.options.get('DEFAULT', 'user')
    
    def get_pass(self):
        return self.options.get('DEFAULT', 'password')
    
    def get_host_of(self, section:str):
        return self.options.get(section, 'host')
    
    def get_port_of(self, section:str):
        return self.options.get(section, 'port')
    
    def get_template(self):
        return self.options.get('DEFAULT', 'template')

    def set_user_remind(self, _option:bool):
        self.options.set('DEFAULT', 'user_remind', _option)

    def set_user(self, user:str):
        return self.options.set('DEFAULT', 'user', user)

    def set_pass(self, _pass:str):
        self.options.set('DEFAULT', 'password', _pass)

    def _act_host_provider(self, choice:str):
        self.options.set('DEFAULT', 'host_selected', choice)