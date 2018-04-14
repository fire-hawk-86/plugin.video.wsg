import sys
import xbmcgui, xbmcplugin
from urllib import urlencode
from urlparse import urlparse, parse_qsl
import requests
import re
from bs4 import BeautifulSoup as Soup

_url = sys.argv[0]
_handle = int(sys.argv[1])
_args = dict(parse_qsl(sys.argv[2][1:]))

index_url = 'https://boards.4chan.org/wsg/'
thread_url = 'https://boards.4chan.org/wsg/thread/%s'


def index(page=''):
    soup = Soup(requests.get(index_url + str(page)).text, 'html.parser')

    for br in soup.find_all("br"):
        br.replace_with("\n")

    for thread in soup.find_all(class_='thread'):
        id_ = thread['id'][1:]
        title = thread.div.find(class_='subject').text
        description = thread.div.find(class_='postMessage').text
        image = 'http:' + thread.div.img['src']

        item=xbmcgui.ListItem(title)
        item.setArt({'poster': image})
        xbmcplugin.addDirectoryItem(_handle, url=_url+'?action=thread&id='+id_, listitem=item, isFolder=True)

    if page == '': page = 1
    item=xbmcgui.ListItem('Next Page (%s)' % (str(page+1)))
    xbmcplugin.addDirectoryItem(_handle, url=_url+'?action=index&page='+str(page+1), listitem=item, isFolder=True)

    xbmcplugin.endOfDirectory(_handle)


def thread(id_):
    xbmcplugin.setContent(_handle, 'videos')
    soup = Soup(requests.get(thread_url % (id_)).text, 'html.parser')

    for file_ in soup.find_all(class_='file'):
        name = file_.a.text
        media = 'http:' + file_.a['href']
        thumbnail = 'http:' + file_.img['src']

        item=xbmcgui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
        item.setArt({'poster': thumbnail})
        item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(_handle, url=media, listitem=item)
        
    xbmcplugin.endOfDirectory(_handle)


if __name__ == '__main__':
    if 'action' in _args:
        if _args['action'] == 'thread':
            thread(_args['id'])
        if _args['action'] == 'index':
            if 'page' in _args:
                index(int(_args['page']))
            else:
                index()
    else:
        index()
