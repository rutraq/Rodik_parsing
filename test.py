import requests
import re
from selenium import webdriver
from time import sleep
from pywinauto.keyboard import send_keys as keys
from selenium.common.exceptions import NoAlertPresentException


def accept():
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        sleep(1)
        accept()


photos = []
payload = {"username": "admin",
           "password": "765tgrfvc76trg",
           "dir": "C:/1",
           "first_directory": '//*[@id="filemanager"]/div/div[2]/div[2]/div[3]/div/a/i',
           "second_directory": '//*[@id="filemanager"]/div/div[2]/div[2]/div[1]/div/a/i'}


def get_photo_number():
    f = open("number_photo.txt")
    photo_number_txt = int(f.read())
    f.close()
    return photo_number_txt


def check_photos():
    import os

    global photos
    files = os.listdir(payload["dir"])
    photo_number = get_photo_number()
    for i in range(len(files)):
        src = "{0}.jpg".format(photo_number)
        if src in files:
            photos.append(src)  # загрузка главного фото
        else:
            break
        j = 1
        while True:
            additional_src = "{0}_{1}.jpg".format(photo_number, j)
            if additional_src in files:
                photos.append(additional_src)  # загрузка дополнительного фото, вставь код для additional_images
                j += 1
            else:
                break
        photo_number += 1


# with requests.session() as session:
#     content = session.post("https://zozo.by/admin/index.php?route=common/login", data=payload).content
#     token = re.search(r'token=\w+"', str(content))[0]
#     token = token[6:-1]
#     add = session.get("https://zozo.by/admin/index.php?route=catalog/product/add&token=" + token)

check_photos()
driver = webdriver.Firefox(executable_path=r"C:/Users/Lenovo/Desktop/geckodriver.exe")
driver.get("https://zozo.by/admin/index.php?route=catalog/product/add")
user = driver.find_element_by_id("input-username")
user.send_keys(payload['username'])
password = driver.find_element_by_id("input-password")
password.send_keys(payload['password'])
password.submit()

sleep(3)
driver.find_element_by_xpath('//*[@id="form-product"]/ul/li[10]/a').click()
driver.find_element_by_xpath('//*[@id="thumb-image"]/img').click()
driver.find_element_by_id("button-image").click()

token = driver.current_url
token = re.search(r'=\w+$', token)[0][1:]

sleep(1)
driver.find_element_by_xpath(payload["first_directory"]).click()
sleep(.5)
driver.find_element_by_xpath(payload["second_directory"]).click()
print(len(photos))
for photo in photos:
    driver.find_element_by_id("button-upload").click()
    keys('C:\\1\\' + photo, with_spaces=True)
    sleep(.1)
    keys('{ENTER}')
    with open("number_photo.txt", 'w') as f:
        f.write(photo[:-4])
    accept()

