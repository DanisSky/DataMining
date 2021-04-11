import asyncio
import json
import re

import requests

from bs4 import BeautifulSoup


def get_page_links(URL, depth, page_and_links, links, max_depth):
    if depth < max_depth:
        li = []
        if URL in page_and_links.keys():
            li = page_and_links.get(URL)

        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser').find_all('a')
        urls = [link.get('href') for link in soup]
        depth = depth + 1
        regex = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

        for link in urls:
            if str(link).startswith("/"):
                link = str(URL) + str(link)
            if str(link) is not None and re.match(regex, str(link)):
                li.append(link)
                page_and_links[URL] = li
                get_page_links(link, depth, page_and_links, links, max_depth)


def clean_slash(url: str):
    if url.startswith('https://'):
        url.replace('https://', '')

        url.replace('//', '/')
        return 'https://' + url

    elif url.startswith('http://'):
        url.replace('http://', '')

        url.replace('//', '/')
        return 'http://' + url


def extractor_links(URL):
    list_of_urls = []
    try:
        html = requests.get(URL).text
        soup = BeautifulSoup(html, 'html.parser').find_all('a')
        urls = [link.get('href') for link in soup]
        regex = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"

        for link in urls:
            if str(link).startswith("/"):
                link = clean_slash(str(URL) + str(link))
            if str(link) is not None and re.match(regex, str(link)):
                list_of_urls.append(link)
    except Exception as e:
        print(e, URL)

    return list(set(list_of_urls))


def get_page_links_v2(url):
    main_link = {url: extractor_links(url)}
    main_link = asyncio.run(consumer(main_link, url))

    links1 = main_link[url]
    for link1 in links1:
        link1: dict
        links2 = link1[list(link1.keys())[0]]
        new_links2 = []
        for link2 in links2:
            new_links2.append(
                {link2: extractor_links(link2)}
            )
        link1[list(link1.keys())[0]] = new_links2

    with open('dataqqq.json', 'w') as outfile:
        json.dump(main_link, outfile)

    return main_link


async def consumer(main_link, url):
    queue = asyncio.Queue()
    count = 0
    links: list = main_link[url]

    for link in links:
        asyncio.create_task(producer(link, queue))

    while count < len(links):
        data = await queue.get()
        link_: str = data['link']
        urls_: list = data['urls']

        links[links.index(link_)] = {link_: urls_}

        queue.task_done()
        count += 1
    main_link[url] = links

    with open('data.json', 'w') as outfile:
        json.dump(main_link, outfile)

    return main_link


async def producer(link, queue):
    await queue.put(dict(link=link, urls=extractor_links(link)))
