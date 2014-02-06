from glob import glob
import sys
from urllib.request import urlopen

from pyquery import PyQuery as pq


def extract(page_url):
    extracted_cards = []
    page = pq(url=page_url,
              opener=lambda url, **kw: urlopen(url).read())
    front_list = page('div#cards>div>table>tr>td:even')
    back_list = page('div#cards>div>table>tr>td:odd')
    for card in zip(front_list, back_list):
        front = card[0].xpath('.//div[@class="cardContentWrapper"]/text()')
        back = card[1].xpath('.//div[@class="cardContentWrapper"]/text()')
        front = '<br />'.join(front) if isinstance(front, list) else front
        back = '<br />'.join(back) if isinstance(back, list) else back
        extracted_cards.append([front, back])
    return extracted_cards


def write_csv(cards, filename):
    with open(filename, 'w') as file:
        for front, back in cards:
            file.write(front + '\\' + back + '\n')

files = glob('*')
for file in files:
    url = 'file:///home/mrgee/flashcard/' + file
    res = extract(url)
    write_csv(res, url[url.rfind('/') + 1:url.find('.')])
