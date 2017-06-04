# Pixiv Daily

## Summary
pixivDaily is an exercise on web crawling. It
automates downloading the top daily favorited
artwork on Pixiv. Individual pieces of artwork and
manga in the rankings are downloaded, but ugoira is
currently not supported.

Pixiv is a social network for artists, primarily those based
in Japan/East Asia. There are some very talented artists on this site; 
some may be professional already, others are the up and coming.
As such, I wanted an easy way to find and gather their artwork.

You will need a pixiv account to use this script though, orz.


## Requirements
Requires python3 and pip3 to be installed. You can use a virtualenv if desired.

Requirements can be installed (**note: system-wide**) with:

```sh
sudo pip3 install -r requirements.txt
```

Drop the sudo when you're installing in a virtualenv.

You can create a file called pwd, and put your email
and password on separate lines in order to log in
automatically.

## Usage
To run, enter:

```sh
python3 dl.py
```

From the console menu, you can:

1. Download:
    - download the top X works of the day
    - download the top X works of a specified day

This is straightforward and what you came here looking for.

Works can be single-page illustrations or multi-page mangas. PixivDaily also
works with multi-page mangas, but it is treated as one work to download.

Ugoira is canvas-based, and is not supported at the moment.

2. Explore:
    - explore other illustrations from existing artists
in your collection
    - explore other illustrations that are favorited by
existing artists in your collection

This is experimental. The idea is the user is shown an image from their collection,
which they may or may not remember having (once their collection has grown). The
user then can choose whether or not to continue exploring.

The first menu option brings up a pagable list of works from the author of the work
you just saw. The second does the same, but for works which that author bookmarked.

This allows the user to obtain new artwork from artists which have been featured in
the top rankings before, or to see what those top artists appreciate amongst their
own circle of friends.


## Known Issues
1. When using virtualenvwrapper, it seems that using -r requirements.txt will install
packages system-wide. In this case, just pip3 install each package individually.
I have not tested with vanilla virtualenv.

2. Occasionally the program will exit during an HTTP request due to an unexpected closed
connection from pixiv.

This may be due to API rate limiting, or just the occasional hiccup in their servers.
Just restart the program and continue using.


## Future Considerations
Right now, the script makes it easy to batch download images for a given day, as that
was its main purpose. It can also used as a console browser of illustrations on authors' pages.

- Add the ability to filter images based on how many people liked or bookmarked them.

- Use a database to retain information about tags or metadata.

- Keep track of artists which have been spotlighted over time, and somehow remind the user
of them when they are looking to explore for other nice illustrations.

