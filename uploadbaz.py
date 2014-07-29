import re
import time
from getpass import getpass
import urllib2

import mechanize
from pyquery import PyQuery as pq



def main():
    br = mechanize.Browser()

    if not login(br):
        print('Login Issue')
        exit(1)
    with open('download_list') as links, open('direct_links', 'w') as direct, open('processed_links', 'a') as processed:
        for link in links:
            try:
                result = get_download_link(br, link)
                if result.startswith('http'):
                    direct.write('{}\n'.format(result.encode('UTF-8')))
                    processed.write('*{}:{}\n'.format(link.strip(), result.encode('UTF-8')))
                    print(result.encode('UTF-8'))
                    break
                else:
                    print('{}: {}\n'.format(link, result.encode('UTF-8')))
                time.sleep(30)
            except mechanize.FormNotFoundError:
                print('Form not found for {}'.format(link.strip()))
            except WrongCaptcha:
                processed.write('@{}\n'.format(link.strip()))
            else:
                print('Direct successfully generated for {}'.format(link.strip()))
                processed.write('*{}:{}\n'.format(link.strip(), result.encode('UTF-8')))


def login(br):
    br.open('http://uploadbaz.com/')
    br.select_form(nr=0)
    # br.form['login'] = raw_input('Username: ')
    br.form['login'] = ''
    # br.form['password'] = getpass()
    br.form['password'] = ''
    br.submit()
    return br.geturl() == 'http://www.uploadbaz.com/?op=my_files'


def get_download_link(br, link):
    br.open(link)
    br.select_form(nr=0)
    br.submit('method_free')

    page = pq(br.response().read())
    captcha = {}

    for span in page.find('span')[-4:]:
        style = span.items()[0][1]
        pos = int(re.findall('padding-left:([0-9]+)px', style)[0])
        captcha[pos] = span.text
    captcha_text = ''.join([captcha[pos] for pos in sorted(captcha)])
    br.select_form(nr=0)
    br.form['code'] = captcha_text
    br.submit()

    response = br.response().read()
    if 'File Download Link Generated' in response:
        page = pq(response)
        return max(map(lambda x: x.text, page.find('a')))
    elif 'Wrong captcha' in response:
        raise WrongCaptcha

    return pq(response).text()


class WrongCaptcha(Exception):
    pass

if __name__ == '__main__':
    main()
