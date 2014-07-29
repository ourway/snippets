#!/usr/bin/env python
from datetime import datetime
from os.path import abspath
from os import system, remove
from random import randrange
from sys import argv
from urllib.request import urlopen

from jinja2 import Environment, PackageLoader
from pyquery import PyQuery as pq
BASE_URL = 'http://www.collinsdictionary.com/dictionary/american/'


def extract(word):
    ex_info = {}
    page = pq(url=BASE_URL + word,
              opener=lambda url, **kw: urlopen(url).read())

    word_definition = page('div.homograph-entry')

    try:
        ex_info['word'] = word_definition('h2.orth').text().split('(')[0][:-1]
        ex_info['pron'] = word_definition('h2.orth').text().split('(')[1][:-2]
    except IndexError:
        ex_info['word'] = word_definition('h2.orth').text().split('(')[0]
        print('No pron for {0}'.format(ex_info['word']))

    ex_info['definitions'] = []
    for definition in word_definition('div.definitions div ol ' +
                                      'li:first-child>span.def'):
        ex_info['definitions'].append(definition.text)

    try:
        ex_info['synonyms'] = set()
        synonyms = page('div.thesaurus_synonyms span.synonym')
        while len(ex_info['synonyms']) < int(len(synonyms) / 5 + 1):
            rand_num = randrange(len(synonyms) - 1)
            ex_info['synonyms'].add(synonyms.eq(rand_num).text())
    except ValueError:
        print('No synonym for {0}'.format(ex_info['word']))

    try:
        ex_info['examples'] = set()
        examples = page('div#examples_box blockquote')
        while len(ex_info['examples']) < int(len(examples) / 5 + 1):
            rand_num = randrange(len(examples) - 1)
            ex_info['examples'].add(examples.eq(rand_num).text())
    except ValueError:
        print('No example for {0}'.format(ex_info['word']))

    print('Extraction finished for {0}'.format(ex_info['word']))

    return ex_info


def write_html(words, out_file):
    env = Environment(loader=PackageLoader('get_and_mail_words', 'templates'))
    template = env.get_template('template.html')
    rendered = template.render(words=words, date=datetime.now().isoformat(' '))
    with open('{0}.html'.format(out_file), 'w') as html:
        html.write(rendered)


def convert_pdf(out_file):
    url = 'file://{0}/{1}.html'.format(abspath('.'), out_file)
    system('phantomjs rasterize.js {0} {1}.pdf {2}'.format(url,
                                                           out_file, 'A4'))
    remove('templates/out.html')


def main(words_list, out_file):
    words = []
    with open(words_list) as words_file:
        for word in words_file:
            words.append(extract(word.replace(' ', '-')[:-1]))
    write_html(words, out_file)
    # convert_pdf(out_file)
    return words

if __name__ == '__main__':
    words = main(argv[1], argv[2])
    # from IPython import embed
    # embed()
