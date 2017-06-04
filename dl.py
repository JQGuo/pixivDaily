from bs4 import BeautifulSoup
import os
import time
import random
from PIL import Image

from settings import session, BASE_URL, LOGIN_URL


'''
Downloads image from pixiv if it does not already exist.
Strips the filename from the url.
'''
def downloadPixivImage(orig_image_url):
    file_name = orig_image_url[orig_image_url.rfind('/') + 1:]

    print('Image URL: ' + orig_image_url)

    # Assume pixiv's url/filename scheme is unique
    if os.path.exists(file_name):
        print('Duplicate')
        return

    # Download the image with streaming option
    image = session.get(orig_image_url, stream=True)
    print('Downloading...')
    
    with open(file_name, 'wb') as f:
        for chunk in image.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()

    print('Finished.')
    image.close()


'''
Works can be a single illustration or a collection (manga). Manga is
displayed on a different display page than single illustrations, so
we have to pick out the images from a list of pages.
'''
def getMangaFromDisplayPage(url):
    # Get url of original image from crawling the manga display page
    illust_page = session.get(url)
    illust_page = BeautifulSoup(illust_page.text, 'html.parser')
    manga_pages = illust_page.select('img.image')

    for image_url in manga_pages:
        downloadPixivImage(image_url['data-src'])


'''
Given the url of the display page for an illustration (/member_illust.php?id=...),
download the original resolution image(s) for that illustration/manga.
'''
def getImagesFromDisplayPage(url):
    # Get url of original image from crawling the display page
    illust_page = session.get(url)
    illust_page = BeautifulSoup(illust_page.text, 'html.parser')
    image_url = illust_page.select('.original-image')

    if image_url:
        image_url = image_url[0]['data-src']
        # referer is the current display page
        session.headers.update({'referer': url})
        downloadPixivImage(image_url)
    else:
        image_url = illust_page.select('a.multiple')[0]['href']
        image_url = "%s/%s" % (BASE_URL, image_url)
        # referer is the manga display page
        session.headers.update({'referer': image_url})
        getMangaFromDisplayPage(image_url)


'''
Download individual illustrations in the rankings for the current day
if specifyDate=False, or the rankings as of "specifyDate".

'''
def getDailyFavs(specifyDate=False):
    # Specify optional date and number of images to download
    if specifyDate:
        date = input('[YYYYMMDD] For rankings as of: ')
    toDownload = int(input('Download Top: '))

    index, page = 0, 0
    while index < toDownload:
        page += 1

        # get all thumbnails on current page
        if specifyDate:
            daily_page = session.get(BASE_URL + '/ranking.php?mode=daily&content=illust&date=%s&p=%s' % (date, page))
        else:
            daily_page = session.get(BASE_URL + '/ranking.php?mode=daily&content=illust&p=%s' % page)

        daily_page = BeautifulSoup(daily_page.text, 'html.parser')
        thumbs = daily_page.select('.ranking-image-item')

        # for each thumbnail, get the illustration url
        for item in thumbs:
            # sometimes pixiv ends the connection, possibly due to API rate limiting
            time.sleep(0.5)
            if index >= toDownload:
                break

            ranked_image = item.select('a')[0]

            img_url = ranked_image['href']
            getImagesFromDisplayPage("%s/%s" % (BASE_URL, img_url) )

            index += 1

'''
Shows a picture in the user's collection and asks for feedback. Returns
the author id for the picture if favorable feedback is given.
'''
def exploreExistingImage():
    all_pics = os.listdir(os.getcwd())
    show_pic = all_pics[random.randint(0, len(all_pics) - 1)]
    img = Image.open(show_pic)
    img.show()

    illust_page = session.get(BASE_URL + '/member_illust.php?mode=medium&illust_id=%s' % show_pic.split('_')[0])
    illust_page = BeautifulSoup(illust_page.text, 'html.parser')
    author = illust_page.select('.user')[0].text.strip()
    author_id = illust_page.select('.user-link')[0]['href'].split('=')[1]

    prompt = input('Would you like to explore more from this author - %s? (y/n) ' % author)
    if prompt == 'y':
        return author_id
    else:
        return None


'''
First shows an existing image in the collection. If the user would like to explore
further, either display more of that author's illustrations or the illustrations in
his/her bookmarks, which is given as a parameter.
'''
def illustPager(bookmarks=False):
    author_id = exploreExistingImage()

    if author_id:
        page = 1
        query_url = None

        # Pager loop
        while(True):
            os.system('clear')
            if bookmarks:
                query_url = '/bookmark.php?type=illust&id=%s&p=%s' % (author_id, page)
            else:
                query_url = '/member_illust.php?type=illust&id=%s&p=%s' % (author_id, page)

            auth_works = session.get(BASE_URL + query_url)
            auth_works = BeautifulSoup(auth_works.text, 'html.parser')
            image_items = auth_works.select('._image-items > .image-item')
            print('There are %s illustrations on the page %s' % (len(image_items), page))
            print('-------------------------------------------')

            index = None
            if bookmarks:
                for index, image in enumerate(image_items):
                    title = image.select('.title')[0].text
                    author = image.select('.ui-profile-popup')[0]['data-user_name']
                    bookmark_count = image.select('.bookmark-count')[0].text

                    print('[%s] %s by %s, with %s bookmarks' % (index, title, author, bookmark_count))
            else:
                for index, image in enumerate(image_items):
                    print('[%s] %s' % (index, image.text))

            prev = auth_works.select('.pager-container > .prev > a')
            _next = auth_works.select('.pager-container > .next > a')

            index += 1
            print('\n')
            prev_index, next_index = None, None

            print('Enter *p to go directly to skip to page p')

            if prev:
                prev_index = index
                print('[%s] Go back a page' % index)
                index += 1

            # because next is a keyword
            if _next:
                next_index = index
                print('[%s] Go forward a page' % index)
                index += 1

            print('[%s] Quit' % index)

            # Input handle loop
            while(True):
                option = input('> ')

                if '*' in option:
                    try:
                        page = int(option.split('*')[1])
                        break
                    except ValueError:
                        print('Invalid input.\n')
                        continue
                    
                try:
                    option = int(option)
                except ValueError:
                    print('Invalid input.\n')
                    continue

                if option < len(image_items):
                    illust_url = image_items[option].select('a')[0]['href']
                    getImagesFromDisplayPage(BASE_URL + illust_url)

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
                    print('Invalid input.\n')

