import configparser
import os

def main():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'MAILING_APP', 'options.ini'))

    print(config.getboolean('DEFAULT', 'user_remind'))

main()