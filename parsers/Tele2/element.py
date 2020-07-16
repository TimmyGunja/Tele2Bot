from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from time import sleep

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)


class BasePageElement(object):
    def __set__(self, obj, value):
        driver = obj.driver
        sleep(3)
        WebDriverWait(driver, 25, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((self.by, self.locator))
        )
        driver.find_element(self.by, self.locator).clear()
        driver.find_element(self.by, self.locator).send_keys(value)

    def __get__(self, obj, owner):
        driver = obj.driver
        sleep(3)
        WebDriverWait(driver, 25, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((self.by, self.locator))
        )
        if self.many:
            element = driver.find_elements(self.by, self.locator)
        else:
            element = driver.find_element(self.by, self.locator)

        return element
