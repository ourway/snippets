from urllib.request import urlopen
from sys import argv

from pyquery import PyQuery as pq


def extract_links(page_url):
    links = []
    page = pq(url=page_url,
              opener=lambda url, **kw: urlopen(url).read())
    for link in page('div.row.section>div.span7>div>a'):
        links.append('http://pyvideo.org' + link.get('href'))
    return links


def extract_video_link(page_url):
    page = pq(url=page_url,
              opener=lambda url, **kw: urlopen(url).read())
    return page('div#sidebar>dl>dd>a')[-1].get('href')


for video in extract_links(argv[-1]):
    print(extract_video_link(video))
