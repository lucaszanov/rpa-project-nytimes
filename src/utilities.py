import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options
import os
from configparser import RawConfigParser

class Utilities:
    '''
    Several functions to optimize development
    '''

    def __init__(self):
        self.config = RawConfigParser()
        self.path_config = os.path.join(os.path.abspath(os.path.join(os.getcwd(),
                                                                     os.pardir)), 'config')
        self.config.read(os.path.join(self.path_config, 'config.ini'), encoding='utf-8')
        self.version_chrome = self.config['browser_parameters']['chrome_version']

    def access_url_via_driver(self, url, service='chrome', options_text = ''):
        '''
        Access some URL and returns opened browser
        :param url:
        :param service: Chrome, Internet Explorer, Firefox, Opera or Edge
        :return: opened browser
        '''
        print(f'Accessing URL {url}')
        try:
            if service == 'chrome':
                if options_text == '':
                    option = Options()
                    option.add_argument('--disable-notifications')
                    driver = webdriver.Chrome(ChromeDriverManager(
                        version=self.version_chrome
                    ).install(), chrome_options=option)
                else:
                    options = webdriver.ChromeOptions()
                    extension_path = options_text
                    options.add_argument('--load-extension={}'.format(extension_path))
                    driver = webdriver.Chrome(ChromeDriverManager(
                        version=self.version_chrome
                    ).install(),
                        options=options)
            elif service == 'internet explorer':
                driver = webdriver.Ie(IEDriverManager().install())
            elif service == 'firefox':
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
            elif service == 'opera':
                driver = webdriver.Opera(executable_path=OperaDriverManager().install())
            elif service == 'edge':
                driver = webdriver.Edge(EdgeChromiumDriverManager().install())
            else:
                return f'Not possible to return driver'
            driver.maximize_window()
            driver.get(url)
            time.sleep(1)
            return driver
        except Exception as erro:
            print(f'Error: {erro}.')
            return f'Error: {erro}.'
