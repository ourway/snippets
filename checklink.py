from urllib.request import urlopen
import urllib.parse
import re
import sys
import os.path

from pyquery import PyQuery as pq

filename = sys.argv[1]
path = sys.argv[2]
filelist = []

with open(filename) as fd:
    for link in fd:
        try:
            page = pq(url=link, opener=lambda url, **kw: urlopen(url).read())
            requested = page('div#content center font font').text()
            filename = requested.split('/')[-1].replace('*', '_').strip()
            if not os.path.exists(os.path.join(path, filename)):
                print(link[:-1] + ' ' + filename)
        except (urllib.request.HTTPError, urllib.request.URLError,
                AttributeError) as e:
            print('Error in ' + link[:-1] + e.message)
