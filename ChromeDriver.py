
from selenium.webdriver.chrome.options import Options
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SpiderWork(object):

    def __init__(self):

        self.fail_flag = 0
        self.finished_airline = 0
        self.finished_date = set()

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19')
        # self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
        # self.driver.set_window_size(360, 640)
        print('init finish')

    def nextday(self, date):
        date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
        delta = datetime.timedelta(days=+1)
        nextday = date + delta
        nextday = nextday.strftime('%Y-%m-%d')
        return nextday

    def onload(self, driver, wait_time):
        time.sleep(wait_time)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

    def execute(self, driver, drop_down_number, wait_time):
        for i in range(drop_down_number):
            self.onload(driver, wait_time)

    def std_date_to_ctrip_date(self, date):
        return str(date[5:7]) + '/' + str(date[8:10])

    def filter_ctrip_date(self, date):
        return date[0:5]

    def deal_flightInfo(self, string):
        flightID = re.findall('[0-9a-zA-Z_]+', string)[0]
        airline = re.findall('[\u4e00-\u9fa5]+', string)[0]
        return airline, flightID


    def nextday(self, date):
        date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
        delta = datetime.timedelta(days=+1)
        nextday = date + delta
        nextday = nextday.strftime('%Y-%m-%d')
        return nextday

    def camouflage_broewser(self):

        search_date = '2018-07-22'
        url = 'https://m.ctrip.com/html5/flight/swift/domestic/SHA/KMG/2018-07-22'
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.driver.implicitly_wait(2)
        print('Waiting...')
        self.driver.get(url)
        print('Waiting...')

        try:
            self.driver.find_elements_by_class_name('page-back-button')[-1].click()
        except (Exception) as e:
            print(e)
            self.driver.implicitly_wait(2)
            self.driver.find_elements_by_class_name('page-back-button')[-1].click()

        for i in range(2):
            time.sleep(3)
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

        self.driver.find_element_by_class_name('button-primary').click()

        time.sleep(3)

        no_more_button_flag = False

        while True:
            date_buttons = self.driver.find_elements_by_class_name('day')

            if self.finished_airline > 180:
                self.finished_airline = 0
                break

            if no_more_button_flag:
                self.driver.find_element_by_class_name('more').click()

                day_buttons = self.driver.find_elements_by_class_name('calendar-day-item')
                contrast_text = ' '

                for each in self.driver.find_elements_by_class_name('calendar-day-current'):
                    contrast_text = each.text
                    break

                currect_btn = False
                for each in day_buttons:
                    if currect_btn:
                        each.click()
                        break
                    if each.text == contrast_text:
                        currect_btn = True

                no_more_button_flag = False
                time.sleep(2)

            for each in date_buttons:

                no_more_button_flag = True

                if self.filter_ctrip_date(each.text) in self.finished_date:
                    continue

                print('--------' + self.filter_ctrip_date(each.text) + '--------')
                search_date = self.nextday(search_date)
                self.finished_date.add(self.filter_ctrip_date(each.text))
                each.click()
                no_more_button_flag = False
                time.sleep(1)
                break

            self.finished_airline += 1

        self.driver.quit()
        self.fail_flag = 0
        self.finished_airline = 0
        self.finished_date.clear()

    def crawl(self):

        print("爬虫进程开始运行")
        while (True):
            self.camouflage_broewser()

if __name__=="__main__":
    spider = SpiderWork()
    print("连接成功")
    spider.crawl()
