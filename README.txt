pixivDaily is an exercise on web crawling. It
automates downloading the top daily favorited
artwork on Pixiv. Individual pieces of artwork in
the rankings are downloaded, but no ugoira or collections
are downloaded.

Pixiv is a social network for artists, primarily based
in Japan/East Asia. There are some very talented artists on this site.
As such, I wanted an easy way to gather their artwork.

You will need a pixiv account to use this script though, orz.

Requirements can be installed with:

sudo pip3 install -r requirements.txt

You can create a file called pwd, and put your email
and password on separate lines in order to log in
automatically.

To run, do python3 dl.py.

From the console menu, you can:

Download:
- download the top X illustrations of the day
- download the top X illustrations of a specified day

Explore:
- explore other illustrations from existing artists
  in your collection
- explore other illustrations that are favorited by
  existing artists in your collection
