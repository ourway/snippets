from urllib.request import urlopen
import urllib.parse
import re
import sys
import os.path


filename = sys.argv[1]
path = sys.argv[2]
filelist = []

with open(filename) as fd:
    for link in fd:
        try:
            page = urlopen(link).read()
            regex = re.compile('You have requested <font color="red">' +
                               link[:-1] + '/(.*?)</font>', re.DOTALL)
            filename = regex.search(str(page)).group(1)
            filename.replace('*', '_')
            if not os.path.exists(os.path.join(path, filename)):
                print(link[:-1] + ' ' + filename)
        except (urllib.request.HTTPError, urllib.request.URLError):
            print('Error in ' + link[:-1])
