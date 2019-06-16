import time
import sys
import autoit
from db import trading_service
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def run(from_date, to_date):

    d = datetime.strptime(from_date, "%Y-%m-%d %H:%M")
    d2 = datetime.strptime(to_date, "%Y-%m-%d %H:%M")

    output = d2 - d
    steps = output.total_seconds() / (60*5)
    steps = int(steps) + 2

    yymmdd = format(d, "%Y%m%d")
    hhmm = format(d, "%H%M")


    url = "https://kr.tradingview.com/chart/"

    obj = {}

    driver = init_browser_setting(url, yymmdd, hhmm)

    for i in range(1, steps):

        if i % 288 == 0:
            print('288개 수행 후 브라우져 재수행')
            driver.close()
            try:
                driver = init_browser_setting(url, yymmdd, hhmm)
            except:
                print("예외상황 한번 더 수행")
                driver.close()
                driver = init_browser_setting(url, yymmdd, hhmm)

        output = trading_service.find_one({'time': format(d, "%Y-%m-%d %H:%M")})

        if output is None:
            obj.clear()
            obj['time'] = format(d, "%Y-%m-%d %H:%M")

            yulgi = get_element_data(driver, '열기')
            high = get_element_data(driver, '고가')
            low = get_element_data(driver, '저가')
            jong = get_element_data(driver, '종')
            obj['열기'] = yulgi
            obj['고가'] = high
            obj['저가'] = low
            obj['종'] = jong

            print(obj)
            trading_service.insert(obj)

        d = d + timedelta(minutes=5)
        autoit.send("{RIGHT}")
        time.sleep(1)


def init_browser_setting(url, yymmdd, hhmm):
    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.find_element(By.XPATH, '//div[@class="layout__area--top"]//input').clear()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@class="layout__area--top"]//input').send_keys('NQ1!')
    driver.find_element(By.XPATH, '//div[@class="layout__area--top"]//input').send_keys(Keys.ENTER)
    driver.find_element(By.XPATH, '//div[@class="layout__area--top"]//div[text()="날"]').click()
    driver.find_element(By.XPATH, '//span[@style="pointer-events: auto;"]//div[text()="5 분"]').click()
    driver.find_element(By.XPATH, '//div[@data-name="data-window"]').click()

    driver.find_element(By.XPATH, '//div[@class="layout__area--center"]//div[text()="...로 가기"]').click()

    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/input').clear()
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/input').send_keys(
        yymmdd)
    time.sleep(1)

    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/input').click()

    for i in range(0, 5):
        driver.find_element(By.XPATH,
                            '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/input').send_keys(
            Keys.DELETE)
        driver.find_element(By.XPATH,
                            '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/input').send_keys(
            Keys.BACK_SPACE)

    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/input').clear()
    time.sleep(1)

    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[2]/div/div/div[1]/input').send_keys(
        hhmm)
    time.sleep(1)

    driver.find_element(By.XPATH,
                        '//*[@id="overlap-manager-root"]/div/div/div[1]/div[2]/div/div[3]/button/span[2]/span').click()

    element = driver.find_element(By.XPATH, "//td[contains(normalize-space(@class), 'chart-markup-table pane')]")
    style_str = element.get_attribute(
        'style')

    width = int(style_str.split('px;')[0].split(': ')[1])
    height = int(style_str.split('px;')[1].split(': ')[1])
    x_off = width / 2
    # print(x_off, y_off)
    location = element.location
    # print(location)
    x = int(x_off) + int(location['x'])
    y = int(height) + int(location['y']) + 80

    # print
    time.sleep(5)
    autoit.mouse_click("left", x, y, 2)

    return driver


def check_popup_exist(driver):
    try:
        driver.find_element_by_xpath('//div[@class="tv-gopro-dialog__section-header-logo"]')
    except NoSuchElementException:
        return False
    return True


def get_element_data(driver, name):
    try:
        data_string = driver.find_element(By.XPATH, '//div[@class="chart-data-window-item-title" and text()="'+name+'"]/../div/span').text
        return data_string
    except:
        time.sleep(2)
        data_string = driver.find_element(By.XPATH,
                                          '//div[@class="chart-data-window-item-title" and text()="' + name + '"]/../div/span').text
        return data_string


if __name__ == '__main__':
    from_date = "2019-05-29 21:05"
    to_date = "2019-06-14 06:55"

    run(from_date, to_date)
    autoit.mouse_move(798,846)






