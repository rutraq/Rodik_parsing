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
        self.driver.get("http://www.tools.by/")
        self.wait = WebDriverWait(self.driver, 3)
        self.find_products()

    def find_products(self):
        categories = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.razdel_name a")))
        del categories[0:5]
        for i in range(len(categories)):
            categories = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.razdel_name a")))
            del categories[0:5]
            self.driver.get(categories[i].get_attribute("href"))
            try:
                self.parse_one_category(self.driver.current_url)
            except TimeoutException:
                pass
            self.driver.back()
            i += 1

    def parse_one_category(self, url):
        r = requests.get(url)
        tree = html.fromstring(r.content)
        products = tree.xpath('//*[@id="products"]/tbody/tr/td[3]/a[1]/@href')
        i = 1
        for product in products:
            r = requests.get(product)
            tree = html.fromstring(r.content)
            src = tree.xpath('//*[@id="show-img"]/@src')
            try:
                new_dir = str(i)
                os.mkdir(new_dir)
                f = open(new_dir + '/url.txt', 'w')
                f.write(product)
                f.close()
                photo = requests.get(src[0])
                with open(new_dir + "/photo.jpg", "wb") as out:
                    out.write(photo.content)
            except requests.exceptions.InvalidSchema:
                pass
            i += 1
            # self.driver.get(product)
            # self.driver.back()


if __name__ == "__main__":
    info = Parsing()
