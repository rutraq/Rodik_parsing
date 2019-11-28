import requests
from lxml import html
import re


def get_categories(url):
    r = requests.get(url)
    tree = html.fromstring(r.content)
    href = tree.xpath("//div[@class='thumbnail subcategory']/a/@href")
    for h in href:
        print(re.search('\w+$', h)[0])
        try:
            pages = get_pages("{0}?limit=100&page=".format(h))
            check(pages, "{0}?limit=100&page=".format(h))
        except IndexError:
            print("Нет таких товаров")
            pass


def get_pages(url):
    r = requests.get(url + '1')
    tree = html.fromstring(r.content)
    pages = tree.xpath('//*[@id="content"]/div[3]/div[2]')[0].text
    pages = re.search('\d+ ст', pages)
    return int(pages[0][:-3])


def check(pages, url):
    i = 1
    while i <= pages:
        print("Page: {0} of {1}".format(i, pages))
        r = requests.get(url + str(i))
        tree = html.fromstring(r.content)
        photo = tree.xpath("//div[@class='image']/a/img/@src")
        href = tree.xpath("//div[@class='name']/a/@href")
        for j in range(len(photo)):
            if photo[j] == "":
                print(href[j])
        i += 1


if __name__ == "__main__":
    url_enter = "https://zozo.by/stroitelnye-materialy/stroitelnye-i-otdelochnye-materialy"
    get_categories(url_enter)
