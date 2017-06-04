import os
from auth import login
from menu import initMenu


'''
Entrypoint for pixiv daily. Attempts to login and then display the menu.
'''
def main():
    username = None
    password = None

    if os.path.exists('pwd'):
        pwd = open('pwd', 'r')
        creds = pwd.read().splitlines()
        username = creds[0]
        password = creds[1]

    login(username, password)
    initMenu()

if __name__ == '__main__':
    main()

