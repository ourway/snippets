import os
from re import compile, IGNORECASE, DOTALL
import sys
from urllib.request import urlopen, url2pathname

with open(sys.argv[1]) as encoded:
    for url in encoded:
        page = urlopen(url).read()
        url_regex = compile('flv_url=(.*?)&amp;', IGNORECASE | DOTALL)
        title_regex = compile('<title>(.*?)</title>', IGNORECASE | DOTALL)
        vid_url = url2pathname(url_regex.search(str(page)).group(1))
        title = title_regex.search(str(page)).group(1)
        print('Downloading: ' + vid_url)
        os.system('wget -cO "' + title + '.mp4" "' + vid_url + '"')
