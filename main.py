from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
from lxml import html
import os


class Driver:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('headless')
        load = DesiredCapabilities().FIREFOX
        load["pageLoadStrategy"] = "eager"
        self.driver = webdriver.Firefox(desired_capabilities=load,
                                        executable_path=r"C:/Users/Lenovo/Desktop/geckodriver.exe",
                                        firefox_options=options)


class Parsing(Driver):
    def __init__(self):
        super().__init__()
        self.url = "http://www.tools.by/?q=kat/53746/1230"
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 3)
        self.find_products(self.url)

    def find_products(self, url):
        r = requests.get("http://www.tools.by/?q=kat/53746/1230")
        tree = html.fromstring(r.content)
        products = tree.xpath(
            '//*/tbody/tr/td[3]/a[1]/@href')
        del products[0]
        print(products)
        for product in products:
            self.driver.get(product)

    # def find_products(self):
    #     categories = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.razdel_name a")))
    #     del categories[0:5]
    #     for i in range(len(categories)):
    #         categories = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.razdel_name a")))
    #         del categories[0:5]
    #         self.driver.get(categories[i].get_attribute("href"))
    #
    #         self.parse_one_category(self.driver.current_url)
    #
    #         self.driver.back()
    #         i += 1
    #
    # def parse_one_category(self, url):
    #     r = requests.get(url)
    #     tree = html.fromstring(r.content)
    #     products = tree.xpath('//*[@id="products"]/tbody/tr/td[3]/a[1]/@href')
    #     i = 1
    #     print(len(products))
    #     for product in products:
    #         r = requests.get(product)
    #         tree = html.fromstring(r.content)
    #         src = tree.xpath('//*[@id="show-img"]/@src')
    #         full_info = self.information(product)
    #         try:
    #             new_dir = full_info['name']
    #             os.mkdir(new_dir)
    #             f = open(new_dir + '/url.txt', 'w')
    #             f.write(product)
    #             f.close()
    #             photo = requests.get(src[0])
    #             with open(new_dir + "/photo.jpg", "wb") as out:
    #                 out.write(photo.content)
    #         except requests.exceptions.InvalidSchema:
    #             pass
    #         i += 1
    #         # self.driver.get(product)
    #         # self.driver.back()
    #
    # def information(self, url):
    #     full_info = dict()
    #     self.driver.get(url)
    #     try:
    #         name = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#product h1")))
    #         full_info['name'] = name.text[7::]
    #         price = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "price_block_n")))
    #         full_info['price'] = price.text
    #         description = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product_text")))
    #         full_info['description'] = description.text
    #         characteristic = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "xar")))
    #         full_info['characteristic'] = characteristic
    #         r = requests.get(url)
    #         tree = html.fromstring(r.content)
    #         links = tree.xpath('//tbody/tr[2]/td/div[3]/text()')
    #         full_info['links'] = links
    #     except TimeoutException:
    #         pass
    #     return full_info


if __name__ == "__main__":
    info = Parsing()
