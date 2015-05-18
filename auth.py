import os
import getpass
import logging
from dl import session, BASE_URL


def login(user=None, pw=None):
    login_data = {'mode': 'login',
                  'return_to': '/'}

    logged_in = False

    while not logged_in:
        os.system('clear')

        if user is None:
            username = input('Username: ')
            password = getpass.getpass()
        else:
            username = user
            password = pw
            user = None
            pw = None

        login_data['pixiv_id'] = username
        login_data['pass'] = password

        r = session.post(BASE_URL + 'login.php', login_data)

        if r.url == BASE_URL + 'mypage.php':
            logged_in = True
        else:
            logging.warning('Login unsuccessful.')
            logging.warning('Warning: Pixiv can temporarily block you for too '
                            'many failed login attempts.')

    logging.warning('Login successful, as {}'.format(username))


def exitProg():
    logging.warning('Logging out...')
    session.get(BASE_URL + 'logout.php')
    logging.warning('Exiting program.')
    exit(0)
