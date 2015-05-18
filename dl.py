from bs4 import BeautifulSoup
import os
import time
import logging
import random
from PIL import Image

from settings import session, BASE_URL

logging.basicConfig(level=logging.WARNING, format='%(message)s')


def getImageFromDisplayPage(url):
    '''
    Given the url of the display page for an illustration (/member_illust.php?id=...),
    download the highest resolution image for that illustration.
    '''
    illust_page = session.get(url)
    illust_page = BeautifulSoup(illust_page.text)
    image_url = illust_page.select('.original-image')[0]['data-src']
    session.headers.update({'referer': url})
    file_name = image_url[image_url.rfind('/') + 1:]

    logging.warning('Image URL: ' + image_url)
    if os.path.exists(file_name):
        logging.warning('Duplicate')
        return

    image = session.get(image_url, stream=True)
    logging.warning('Downloading...')
    with open(file_name, 'wb') as f:
        for chunk in image.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    logging.warning('Finished.')
    image.close()


def getDailyFavs(specifyDate=False):
    '''
    Download individual illustrations in the rankings for the current day
    if specifyDate=False, or the rankings as of "specifyDate".

    '''

    if specifyDate:
        date = input('[YYYYMMDD] For rankings as of: ')
    toDownload = int(input('Download Top: '))

    index, page = 0, 0
    while index < toDownload:
        page += 1

        if specifyDate:
            daily_page = session.get(BASE_URL + 'ranking.php?mode=daily&content=illust&date=%s&p=%s' % (date, page))
        else:
            daily_page = session.get(BASE_URL + 'ranking.php?mode=daily&content=illust&p=%s' % page)

        daily_page = BeautifulSoup(daily_page.text)
        thumbs = daily_page.select('.ranking-image-item')

        for item in enumerate(thumbs):
            time.sleep(0.5)
            if index > toDownload:
                break

            ranked_image = item.select('a')[0]

            # don't download collections
            if('multiple' in ranked_image.get('class')):
                continue

            img_url = ranked_image['href']
            getImageFromDisplayPage(BASE_URL + img_url)


def exploreExistingImage():
    '''
    Shows a picture in the user's collection and asks for feedback. Returns
    the author id for the picture if favorable feedback is given.
    '''
    all_pics = os.listdir(os.getcwd())
    show_pic = all_pics[random.randint(0, len(all_pics) - 1)]
    img = Image.open(show_pic)
    img.show()

    illust_page = session.get(BASE_URL + 'member_illust.php?mode=medium&illust_id=%s' % show_pic.split('_')[0])
    illust_page = BeautifulSoup(illust_page.text)
    author = illust_page.select('.user')[0].text.strip()
    author_id = illust_page.select('.user-link')[0]['href'].split('=')[1]

    prompt = input('Would you like to download another picture from this author - %s? (y/n) ' % author)
    if prompt == 'y':
        return author_id
    else:
        return None


def illustPager(bookmarks=False):
    '''
    Displays illustrations for an author's illustrations or bookmarks, which is
    given as a parameter.
    '''
    author_id = exploreExistingImage()

    if author_id:
        page = 1
        query_url = None
        while(True):
            os.system('clear')
            if bookmarks:
                query_url = 'bookmark.php?type=illust&id=%s&p=%s' % (author_id, page)
            else:
                query_url = 'member_illust.php?type=illust&id=%s&p=%s' % (author_id, page)

            auth_works = session.get(BASE_URL + query_url)
            auth_works = BeautifulSoup(auth_works.text)
            image_items = auth_works.select('._image-items > .image-item')
            logging.warning('There are %s illustrations on the page %s' % (len(image_items), page))
            logging.warning('--------------------------------------')

            index = None
            if bookmarks:
                for index, image in enumerate(image_items):
                    title = image.select('.title')[0].text
                    author = image.select('.ui-profile-popup')[0]['data-user_name']
                    bookmark_count = image.select('.bookmark-count')[0].text

                    logging.warning('[%s] %s by %s, with %s bookmarks' % (index, title, author, bookmark_count))
            else:
                for index, image in enumerate(image_items):
                    logging.warning('[%s] %s' % (index, image.text))

            prev = auth_works.select('.pager-container > .prev > a')
            _next = auth_works.select('.pager-container > .next > a')

            index += 1
            logging.warning('\n')
            prev_index, next_index = None, None

            logging.warning('Enter *p to go directly to skip to page p')

            if prev:
                prev_index = index
                logging.warning('[%s] Go back a page' % index)
                index += 1

            if _next:
                next_index = index
                logging.warning('[%s] Go forward a page' % index)
                index += 1

            logging.warning('[%s] Quit' % index)

            while(True):
                option = input('> ')
                if '*' in option:
                    page = int(option.split('*')[1])
                    break

                option = int(option)
                if option < len(image_items):
                    illust_url = image_items[option].select('a')[0]['href']
                    getImageFromDisplayPage(BASE_URL + illust_url)

                elif option == prev_index:
                    page -= 1
                    break
                elif option == next_index:
                    page += 1
                    break
                elif option == index:
                    os.system('clear')
                    return
                else:
                    logging.warning('Invalid input.\n')
