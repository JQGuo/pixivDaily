import os
import time
from dl import getDailyFavs, illustPager
from auth import exitProg
from settings import SAVE_DIR


'''
Composable menu class which is only used to compose the menu tree.
The Prompt class is a helper used to interact with it. Menu action 
functionality should be provided through the setAction method.
'''
class Menu:

    def __init__(self, parent=None):
        self.action = None
        self.params = None

        if parent:
            self.childInfo = ['Go back to previous menu.']
            self.children = [parent]
        else:
            self.childInfo = []
            self.children = []

    def printMenu(self):
        print('Please select an option.')

        for index, item in enumerate(self.childInfo):
            print('[%s] %s' % (index, item) )

    def setAction(self, action, params=None):
        self.action = action
        self.params = params

    def doAction(self):
        if self.action is not None:
            if self.params:
                self.action(**self.params)
            else:
                self.action()

    def hasChildren(self):
        return self.children is not []

    def addChild(self, msg, child):
        self.childInfo.append(msg)
        self.children.append(child)


'''
The Prompt class provides the loop method which is the code entrypoint
to the menu interface.
'''
class Prompt:

    def __init__(self, root):
        self.current = root

    def loop(self):
        menu = self.current
        while True:
            menu.doAction()
            if menu.hasChildren:
                menu.printMenu()
                x = None

                try:
                    x = int(input('> '))
                except ValueError:
                    pass

                os.system('clear')
                if (type(x) is not int or
                        x not in range(len(menu.children))):
                    print('Invalid input.\n')
                else:
                    menu = menu.children[x]


'''
Initializes the menus and associated functionalities for the program.
'''
def initMenu():
    # Root
    root = Menu()

    # - Daily Favorites
    dailyFavorites = Menu(root)

    # -- Today's Daily Favorites
    dailyFavoritesToday = Menu(dailyFavorites)
    dailyFavoritesToday.setAction(getDailyFavs)

    # -- Daily Favorites by Date
    dailyFavoritesByDate = Menu(dailyFavorites)
    params = {
        'specifyDate': True
    }
    dailyFavoritesByDate.setAction(getDailyFavs, params)
    dailyFavorites.addChild('Top Ranked for Today', dailyFavoritesToday)
    dailyFavorites.addChild('Top Ranked for Specified Date', dailyFavoritesByDate)

    # - Explore
    explore = Menu(root)

    # -- Explore Artist Illustration from Existing Artist in Collection
    exploreIllustFromExistingArtist = Menu(explore)
    exploreIllustFromExistingArtist.setAction(illustPager)
    exploreIllustFromExistingArtist.addChild('Try again with random artist?', exploreIllustFromExistingArtist)

    # -- Explore Bookmarked Illustrations from Existing Artist in Collection
    exploreBookmarkFromExistingArtist = Menu(explore)
    params = {
        'bookmarks': True
    }
    exploreBookmarkFromExistingArtist.setAction(illustPager, params)
    exploreBookmarkFromExistingArtist.addChild('Try again with random artist?', exploreBookmarkFromExistingArtist)
    explore.addChild('Explore illustrations by an existing artist.', exploreIllustFromExistingArtist)
    explore.addChild('Explore illustrations bookmarked by an existing artist.', exploreBookmarkFromExistingArtist)

    # - Quit
    quit = Menu(root)
    quit.setAction(exitProg)

    root.addChild('Daily Rankings', dailyFavorites)
    root.addChild('Explore', explore)
    root.addChild('Quit', quit)

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
        time.sleep(1)
    os.chdir(os.getcwd() + '/' + SAVE_DIR)

    prompt = Prompt(root)
    prompt.loop()

