import requests
from lxml import html
import re


def get_pages(url):
    r = requests.get(url + '1')
    tree = html.fromstring(r.content)
    pages = tree.xpath('//*[@id="content"]/div[3]/div[2]')[0].text
    pages = re.search('\d+ ст', pages)
    return int(pages[0][:-3])


def check(pages, url):
    i = 1
    while i <= pages:
        r = requests.get(url + str(i))
        tree = html.fromstring(r.content)
        photo = tree.xpath("//div[@class='image']/a/img/@src")
        href = tree.xpath("//div[@class='name']/a/@href")
        for j in range(len(photo)):
            if photo[j] == "":
                print(href[j])
        print("Page: {0}".format(i))
        i += 1


if __name__ == "__main__":
    url_enter = "https://zozo.by/tovary-dlya-doma-i-sada/sadovaya-tehnika-osnastka-i-prinadlezhnosti/nasosy-i-nasosnye-stancii?limit=100&page="
    check(get_pages(url_enter), url_enter)
