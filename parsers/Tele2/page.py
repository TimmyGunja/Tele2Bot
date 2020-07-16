from parsers.Tele2.locator import *
from parsers.Tele2.element import BasePageElement
from selenium.webdriver.common.by import By


class SearchLinksElement(BasePageElement):
    by = By.CLASS_NAME
    locator = 'text-link'
    many = True


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    search_links = SearchLinksElement()

    def is_title_matches(self):
        return "Tele2" in self.driver.title


class SearchResultPage(BasePage):
    def is_results_found(self):
        return 'No results found.' not in self.driver.page_source