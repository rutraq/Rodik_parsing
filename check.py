import requests
from lxml import html


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
    url_enter = "https://zozo.by/tovary-dlya-doma-i-sada/sadovaya-tehnika-osnastka-i-prinadlezhnosti/benzopily-i-pily-cepnye-elektricheskie?limit=100&page="
    check(4, url_enter)
