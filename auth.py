import os
import time
import getpass
import json

from settings import session, BASE_URL, LOGIN_URL
from bs4 import BeautifulSoup

'''
The post key is some kind of token that is required for the pixiv POST request.
Seems to be auto-generated and is supplied in a hidden input form which seems to
hold default values for something.
'''
def getPostKey():
    r = session.get(LOGIN_URL)

    postkey = BeautifulSoup(r.text, 'html.parser')
    postkey = postkey.find("input", class_="json-data")
    postkey = postkey.attrs['value']
    postkey = json.loads(postkey)
    postkey = postkey["pixivAccount.postKey"]

    return postkey

'''
Attempts to login by POST request using supplied credentials.
Uses the response content to determine success, as the status code 
does not indicate validation error, only errors in using REST requests.
'''
def login(user=None, pw=None):

    # login headers for the post request, some of these may not be needed
    login_headers = {
        'Host': 'accounts.pixiv.net',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://accounts.pixiv.net/login?lang=en&source=pc&view_type=page&ref=wwwtop_accounts_index',
        'DNT': '1'
    }

    # login data for the post request, some of these may not be needed
    login_data = {
        'post_key': getPostKey(),
        'captcha': '',
        'g_captcha_response': '',
        'source': 'pc',
        'ref': 'wwwtop_accounts_index',
        'return_to': 'https://www.pixiv.net/'
    }

    logged_in = False

    while not logged_in:
        os.system('clear')

        if user is None:
            username = input('Username: ')
            password = getpass.getpass()
        else:
            username = user
            password = pw

            # ask for credentials if saved ones are invalid
            user = None
            pw = None

        login_data['pixiv_id'] = username
        login_data['password'] = password

        r = session.post(BASE_URL + '/api/login?lang=en', data=login_data, headers=login_headers)

        # pixiv auth returns JSON indicating validation error or success
        content_response = r.json()['body']

        if r.status_code == 200 and 'success' in content_response:
            logged_in = True
        else:
            print('Login unsuccessful. Check errors: ')
            print( content_response )
            print('Warning: Pixiv can temporarily block you for too '
                            'many failed login attempts.')
            time.sleep(1)

    print('Login successful, as {}'.format(username))


'''
Sends a GET request to the logout API when exiting the program.
Probably not needed as we aren't a browser.
'''
def exitProg():
    print('Logging out...')
    session.get(BASE_URL + '/logout.php')
    print('Exiting program.')
    exit(0)

