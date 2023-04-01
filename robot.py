from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime
import warnings
import sys
from loguru import logger


class Robot:
    def __init__(self):
        warnings.filterwarnings('ignore')
        self.time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=self.options, executable_path='./chromedriver.exe')
        self.driver.get('https://kyfw.12306.cn/otn/resources/login.html')
        self.driver.maximize_window()
        while self.find_ele_xpath('//*[@id="ERROR"]'):
            self.driver.close()
            self.driver.get('https://kyfw.12306.cn/otn/resources/login.html')
    def log_t(self, msg):
        print(f'\033[1;31m{msg}\033[0m')
        logger.add(sys.stderr, format="{time} {level}", filter="my_module", level="INFO")
        logger.remove()
        logger.add(f'log_t/{self.time}')
        logger.info(f'{msg}')

    def wait_ele_click_xpath_safe(self, xpath, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.find_element_by_xpath(xpath).click()

    def wait_ele_xpath_safe(self, xpath, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        if self.driver.find_element_by_xpath(xpath):
            return True
        else:
            return False

    def find_ele_click_xpath(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def send_keys_xpath(self, xpath, keys):
        self.driver.find_element_by_xpath(xpath).clear()
        self.driver.find_element_by_xpath(xpath).send_keys(keys)

    def find_eles_xpath(self, xpath):
        eles = self.driver.find_elements_by_xpath(xpath)
        if eles:
            return eles
        return False

    def click_to_last_window_xpath(self, xpath):
        self.find_ele_click_xpath(xpath)
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[-1])

    def get_ele_text(self, xpath):
        return self.driver.find_element_by_xpath(xpath).text

    def input_clear_xpath(self, xpath):
        return self.driver.find_element_by_xpath(xpath).clear()

    def switch_last_window(self):
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[-1])

    def refresh(self):
        self.driver.refresh()

    def find_ele_xpath(self, xpath):
        try:
            ele = self.driver.find_element_by_xpath(xpath)
            return True
        except Exception:
            return False

    def close_window(self):
        self.driver.close()


