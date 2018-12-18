import os
from unittest import skipIf

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote import webdriver as remote
from selenium.webdriver.chrome import webdriver as chrome
from selenium.webdriver.support.wait import WebDriverWait

from library.api import ApiTest
from library.obj import DEFAULT_PASSWORD
from library.util import retry, SELENIUM_TIMEOUT, SLEEP

webdriver_type = os.environ.get('WEBDRIVER_TYPE', 'CHROME')
keep_browser = os.environ.get('KEEP_BROWSER')
skip_selenium_tests = os.environ.get('SKIP_SELENIUM_TESTS', 0)


def create_webdriver():
    if webdriver_type == 'CHROME':
        return chrome.WebDriver()
    
    if webdriver_type == 'REMOTE_CHROME':
        return remote.WebDriver(command_executor='http://selenium:4444/wd/hub',
                                desired_capabilities=DesiredCapabilities.CHROME)
    
    raise Exception(f"bad webdriver type {webdriver_type}")


class SeleniumTest(ApiTest):
    
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.webdriver = create_webdriver()
        
    @skipIf(skip_selenium_tests, "selenium tests disabled")
    def setUp(self):
        super().setUp()
    
    @classmethod
    def tearDownClass(self):
        if not keep_browser:
            self.webdriver.close()
        super().tearDownClass()

    def wait(self, cond=None, ret=None, timeout=SELENIUM_TIMEOUT, sleep=SLEEP):
        WebDriverWait(self.webdriver, timeout, sleep).until(cond)

    def wait_for_page(self, title=None):
        self.wait(lambda w: w.execute_script('return (document.readyState == "complete");'))
        if title:
            self.wait(lambda w: w.title == title)

    def login_member(self, member=None):
        member = member or self.api.member
        token = self\
            .post("/oauth/token", {"grant_type": "password",
                                   "username": member["email"],
                                   "password": DEFAULT_PASSWORD})\
            .expect(code=200)\
            .get("access_token")
        
        self.webdriver.get(f"{self.public_url}/member/login/{token}")

    def wait_for_element(self, id=None, name=None, tag=None, css=None, xpath=None,
                         timeout=SELENIUM_TIMEOUT, sleep=SLEEP):
        if id:
            def get():
                return self.webdriver.find_element_by_id(id)
        elif name:
            def get():
                return self.webdriver.find_element_by_name(name)
        elif tag:
            def get():
                return self.webdriver.find_element_by_tag_name(tag)
        elif css:
            def get():
                return self.webdriver.find_element_by_css_selector(css)
        elif xpath:
            def get():
                return self.webdriver.find_element_by_xpath(xpath)
        else:
            raise Exception("missing parameter")
        
        return retry(timeout=timeout, sleep=sleep, do_retry=lambda e: isinstance(e, NoSuchElementException))(get)()

    def browse_shop(self):
        self.webdriver.get(f"{self.public_url}/shop")
        self.wait_for_page(title="Makerspace Webshop")
        