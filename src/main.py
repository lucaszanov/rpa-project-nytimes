from configparser import RawConfigParser
import os
import time
from utilities import Utilities
from download_pics import DownloadPics
from export_excel import ExportExcel
from get_attributes import GetAttributes
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from tqdm import tqdm

class Main:

    def __init__(self):
        self.date_now=datetime.now().strftime("%Y%m%d_%H%M%S")
        self.parent_path=os.path.dirname(os.getcwd())
        self.config = RawConfigParser()
        self.path_config = os.path.join(os.path.abspath(os.path.join(os.getcwd(),
                                                                     os.pardir)), 'config')
        self.config.read(os.path.join(self.path_config, 'config.ini'), encoding='utf-8')
        self.timesleeplow = int(self.config['general_parameters']['timesleeplow'])
        self.timesleepmedium = int(self.config['general_parameters']['timesleepmedium'])
        self.timesleephigh = int(self.config['general_parameters']['timesleephigh'])
        self.folder_name_outputs = self.config['general_parameters']['folder_name_outputs']
        self.folder_name_images = self.config['general_parameters']['folder_name_images']

        self.url_website = self.config['website_parameters']['url_website']
        self.search_phrase = self.config['input_parameters']['search_phrase']
        self.news_section = self.config['input_parameters']['news_sections']
        self.news_section=self.news_section.replace("[", "").replace("]", "").replace(
            " ", "")
        self.news_section=self.news_section.split(",")
        self.number_months = self.config['input_parameters']['number_months']
        self.url_website=self.url_website.replace("$TERM",self.search_phrase.replace(" ","+"))
        self.xpath_close_cookies_button = self.config['website_parameters'][
            'xpath_close_cookies_button']
        self.innertext_accept_terms_button = self.config['website_parameters'][
            'innertext_accept_terms_button']
        self.default_search_attribute = self.config['website_parameters'][
            'default_search_attribute']
        self.xpath_sections_button = self.config['website_parameters'][
            'xpath_sections_button']
        self.xpath_sections_boxes = self.config['website_parameters'][
            'xpath_sections_boxes']

    def get_driver(self):
        self.driver=Utilities().access_url_via_driver(url=self.url_website,service='chrome')

    def accept_terms(self):
        max_trials=5
        trials=0
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        while trials<max_trials:
            for button in buttons:
                if button.text.lower()==self.innertext_accept_terms_button:
                    button.click()
                    trials=max_trials
                    break
            trials+=1
            time.sleep(self.timesleepmedium)

    def close_cookies(self):
        close_cookies_button = self.driver.find_elements(
            By.XPATH, f"//button[@{self.default_search_attribute}='{self.xpath_close_cookies_button}']")
        close_cookies_button[0].click()
        time.sleep(self.timesleeplow)

    def filter_sections(self):
        sections_button = self.driver.find_elements(
            By.XPATH, f"//button[@{self.default_search_attribute}='{self.xpath_sections_button}']")
        sections_button[0].click()
        time.sleep(self.timesleeplow)
        search_result_elements = self.driver.find_elements(By.XPATH,
                   f"//ul[@{self.default_search_attribute}='{self.xpath_sections_boxes}']/li")
        for element in search_result_elements:
            try:
                section = element.text
                section = re.sub(r'\d+\.?\d*', '', section)
                if section in self.news_section:
                    print(f'Selecting {section}')
                    element.click()
            except Exception as error:
                print(error)
        time.sleep(self.timesleeplow)

    def create_images_folders(self):
        if not os.path.exists(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now)):
            os.mkdir(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now))
        if not os.path.exists(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now,
                                           self.folder_name_images)):
            os.mkdir(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now,
                                  self.folder_name_images))

    def main(self):
        self.create_images_folders()
        self.get_driver()
        self.accept_terms()
        self.close_cookies()
        self.filter_sections()
        list_data=GetAttributes(self.driver).main()
        for data in tqdm(list_data):
            print(data)
            DownloadPics().download_pic(data["pic_url"],
                                        os.path.join(self.parent_path,self.folder_name_outputs,
                                          self.date_now,self.folder_name_images,
                                         data["pic_file_name"]))
        time.sleep(self.timesleepmedium)
        ExportExcel().export_excel_file(list_data,os.path.join(
            self.parent_path,self.folder_name_outputs,self.date_now,self.date_now+".xlsx"))

if __name__ == "__main__":
    Main().main()
