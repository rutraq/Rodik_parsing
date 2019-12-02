import requests
from lxml import html
import os
import shutil
import re
import file


class Parsing:
    def __init__(self):
        self.url = "http://www.tools.by/?q=kat/26/41"
        self.find_products(self.url)

    def find_products(self, url):
        r = requests.get(url)
        tree = html.fromstring(r.content)
        products = tree.xpath('//*/tbody/tr/td[3]/a[1]/@href')  # адекватный
        # products = tree.xpath('//*/td[2]/a[1]/@href')  # ебанутый
        # products = tree.xpath(
        #     "//*/tbody/tr/td[3]/a[contains(text(),'Аккум') or contains(text(),'л')]/@href")
        if products[0] == "http://remont.tools.by":
            del products[0]
        if os.path.exists("photos"):
            shutil.rmtree("photos")
        os.mkdir("photos")
        i = 1

        length = len(products)
        count_percents = length / 100
        clear_line = "--------------------------------------------------"
        progress_line = ""
        progress_plus = 2
        count = 0

        for product in products:
            r = requests.get(product)
            tree = html.fromstring(r.content)
            src = tree.xpath('//*[@id="show-img"]/@src')
            try:
                photo = requests.get(src[0])

                with open("photos/{0}.jpg".format(i), 'wb') as out:
                    out.write(photo.content)

                more_photos = tree.xpath('//*[@id="small-img-roll"]/div[2]/img/@src')
                if len(more_photos) != 0:
                    self.additional_photos(i, more_photos, tree)

                if (i / count_percents) >= progress_plus:
                    while progress_plus <= (i / count_percents):
                        progress_plus += 2
                        progress_line += "#"
                        count += 1
                    print("\r{0}% |{1}{2}| {3} of {4}".format(round(i / count_percents, 1), progress_line,
                                                              clear_line[count:], i, length),
                          end="")
                else:
                    print("\r{0}% |{1}{2}| {3} of {4}".format(round(i / count_percents, 1), progress_line,
                                                              clear_line[count:], i, length),
                          end="")
                i += 1
            except IndexError:
                print(src)
                print(product)
                pass

    @staticmethod
    def additional_photos(i, more_photos, tree):
        j = 1
        path = "http://www.tools.by/newkatfiles/products/"
        try:
            while True:
                photos = re.search(r'\d+_', more_photos[0])[0]
                src = "{0}{1}{2}.jpg".format(path, photos, j)
                photo = requests.get(src)
                with open("photos/{0}_{1}.jpg".format(i, j), 'wb') as out:
                    out.write(photo.content)
                j += 1
                more_photos = tree.xpath('//*[@id="small-img-roll"]/div[{0}]/img/@src'.format(j + 1))
                if len(more_photos) == 0:
                    break
        except IndexError:
            print("Index")
        except TypeError:
            pass


if __name__ == "__main__":
    info = Parsing()
    file.copy_files()
