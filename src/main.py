from configparser import RawConfigParser
import os
import time
from utilities import Utilities
from selenium.webdriver.common.by import By
import re
from datetime import datetime
from tqdm import tqdm
import logging
from download_pics import DownloadPics
from export_excel import ExportExcel
from get_attributes import GetAttributes

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

    def validate_inputs(self):
        try:
            self.number_months=int(self.number_months)
        except Exception as error:
            return ["error", f"Error validating number_months. Msg: {error}"]
        try:
            self.news_section = self.news_section.replace("[", "").replace("]", "").replace(
                " ", "")
            self.news_section = self.news_section.split(",")
        except Exception as error:
            return ["error", f"Error validating news_section. Msg: {error}"]
        return ["success",""]

    def create_log_file(self):
        logging.basicConfig(filename=os.path.join(self.parent_path, self.folder_name_outputs,
                            self.date_now, f'{self.date_now}.log'),
                            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                            encoding='utf-8')
        self.logger = logging

    def get_driver(self):
        self.driver = Utilities().access_url_via_driver(url=self.url_website,service='chrome')

    def accept_terms(self):
        print('Accepting terms')
        self.logger.info('Accepting terms')
        max_trials = 10
        trials = 0
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        while trials < max_trials:
            for button in buttons:
                if button.text.lower() == self.innertext_accept_terms_button:
                    button.click()
                    trials = max_trials
                    break
            trials += 1
            time.sleep(self.timesleepmedium)

    def close_cookies(self):
        print('Closing cookies popup')
        self.logger.info('Closing cookies popup')
        close_cookies_button = self.driver.find_elements(
            By.XPATH, f"//button[@{self.default_search_attribute}='{self.xpath_close_cookies_button}']")
        close_cookies_button[0].click()
        time.sleep(self.timesleeplow)

    def filter_sections(self):
        print(f'Filtering sections: {self.news_section}')
        self.logger.info(f'Filtering sections: {self.news_section}')
        sections_button = self.driver.find_elements(
            By.XPATH, f"//button[@{self.default_search_attribute}='{self.xpath_sections_button}']")
        sections_button[0].click()
        time.sleep(self.timesleeplow)
        search_result_elements = self.driver.find_elements(By.XPATH,
                   f"//ul[@{self.default_search_attribute}='{self.xpath_sections_boxes}']/li")
        if search_result_elements==[]:
            return ["error", f"No sections available. No results"]
        for element in search_result_elements:
            try:
                section = element.text
                section = re.sub(r'\d+\.?\d*', '', section)
                if section.lower() in [x.lower() for x in self.news_section]:
                    print(f'Selecting {section}')
                    self.logger.info(f'Selecting {section}')
                    element.click()
                else:
                    print(f'Section {section} available but not selected')
                    self.logger.info(f'Section {section} available but not selected')
            except Exception as error:
                msg = f'Error filtering sections. Msg: {error}'
                print(msg)
                self.logger.error(msg)
        time.sleep(self.timesleeplow)
        print('-'*50)
        return ["success", f""]

    def create_images_folders(self):
        if not os.path.exists(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now)):
            os.mkdir(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now))
        if not os.path.exists(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now,
                                           self.folder_name_images)):
            os.mkdir(os.path.join(self.parent_path,self.folder_name_outputs,self.date_now,
                                  self.folder_name_images))

    def main(self):
        print(f'\n============================= Execution Initialized =============================\n')
        validate_inputs_ = self.validate_inputs()
        if validate_inputs_[0] != "success":
            print(f"Error: {validate_inputs_[1]}")
            return f"Error: {validate_inputs_[1]}"
        self.create_images_folders()
        self.create_log_file()
        self.get_driver()
        self.accept_terms()
        self.close_cookies()
        filter_sections_ = self.filter_sections()
        if filter_sections_[0] != "success":
            print(f"Error: {filter_sections_[1]}")
            return f"Error: {filter_sections_[1]}"
        list_data=GetAttributes(self.driver, self.logger).main()
        for data in tqdm(list_data):
            print(f'Collected data: {data}')
            print(f'Downloading pic: {data["pic_file_name"]}')
            self.logger.info(f'Downloading pic: {data["pic_file_name"]}')
            DownloadPics().download_pic(data["pic_url"],
                                        os.path.join(self.parent_path,self.folder_name_outputs,
                                          self.date_now,self.folder_name_images,
                                         data["pic_file_name"]))
        time.sleep(self.timesleepmedium)
        print(f'Exporting results to Excel file: {self.date_now+".xlsx"}')
        self.logger.info(f'Exporting results to Excel file: {self.date_now+".xlsx"}')
        ExportExcel().export_excel_file(list_data,os.path.join(
            self.parent_path,self.folder_name_outputs,self.date_now,self.date_now+".xlsx"))
        print(f'\n============================= Execution Finalized =============================\n')

if __name__ == "__main__":
    Main().main()
