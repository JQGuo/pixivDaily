import os
from auth import login
from menu import initMenu


def main():
    username = None
    password = None

    if os.path.exists('pwd'):
        pwd = open('pwd', 'r')
        username = pwd.readline()
        password = pwd.readline()

    login(username, password)
    initMenu()

if __name__ == '__main__':
    main()
