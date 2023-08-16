from configparser import RawConfigParser
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, date
import re
import logging
from dateutil.relativedelta import relativedelta

class GetAttributes:

    def __init__(self, driver, logger):
        self.driver = driver
        self.config = RawConfigParser()
        self.path_config = os.path.join(os.path.abspath(os.path.join(os.getcwd(),
                                                                     os.pardir)), 'config')
        self.config.read(os.path.join(self.path_config, 'config.ini'), encoding='utf-8')
        self.timesleeplow = int(self.config['general_parameters']['timesleeplow'])
        self.timesleepmedium = int(self.config['general_parameters']['timesleepmedium'])
        self.timesleephigh = int(self.config['general_parameters']['timesleephigh'])
        self.regex_money_bool = self.config['general_parameters']['regex_money_bool']
        self.search_phrase = self.config['input_parameters']['search_phrase']
        self.news_section = self.config['input_parameters']['news_sections']
        self.number_months = self.config['input_parameters']['number_months']
        self.number_months = int(self.number_months)
        self.default_search_attribute = self.config['website_parameters'][
            'default_search_attribute']
        self.xpath_cards = self.config['website_parameters'][
            'xpath_cards']
        self.xpath_show_more_button = self.config['website_parameters'][
            'xpath_show_more_button']
        self.xpath_date= self.config['website_parameters'][
            'xpath_date']
        self.logger=logger

        self.list_data = []
        self.dict_month = {
            "Jan.": 1,
            "Feb.": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "Aug.": 8,
            "Sept.": 9,
            "Oct.": 10,
            "Nov.": 11,
            "Dec.": 12
        }

    def get_month_date_criteria(self):
        if self.number_months == 0 or self.number_months == 1:
            return date(datetime.now().year, datetime.now().month, 1)
        else:
            return date(datetime.now().year, datetime.now().month, 1)-relativedelta(months=
                                                         self.number_months-1)

    def get_last_date_available(self):
        time.sleep(self.timesleepmedium)
        search_result_elements = self.driver.find_elements(By.XPATH,
                  f"//ol[@{self.default_search_attribute}='{self.xpath_cards}']/li")
        date_ = ""
        for index in range(len(search_result_elements)-1, -1, -1):
            if date_ == "":
                try:
                    date_ = search_result_elements[index].find_elements(By.TAG_NAME, "span")[0].text
                    try:
                        if "ago" in date_:
                            month = datetime.now().month
                            day = datetime.now().day
                            year = datetime.now().year
                            date_ = date(year, month, day)
                        else:
                            data_split = date_.split(" ")
                            if len(data_split) == 2:
                                day = int(data_split[1])
                                month = self.dict_month[data_split[0]]
                                year = datetime.now().year
                                date_ = date(year, month, day)
                            else:
                                day = int(data_split[1])
                                month = self.dict_month[data_split[0]]
                                year = int(data_split[2])
                                date_ = date(year, month, day)
                        return date_
                    except Exception as error:
                        print(f'Error: {error}')
                except Exception as error:
                    print(f'Error: {error}')

    def preparing_cards_to_extract(self):
        date_criteria = self.get_month_date_criteria()
        last_date_available = self.get_last_date_available()
        while date_criteria <= last_date_available:
            click_show_more_results_ = self.click_show_more_results()
            if click_show_more_results_[0] == "error":
                return ["success", f""]
            last_date_available = self.get_last_date_available()
        return ["success", f""]

    def get_dates(self):
        print('Getting dates')
        self.logger.info('Getting dates')
        for data in self.list_data:
            try:
                if "ago" in data["date"]:
                    data["month"] = datetime.now().month
                    data["day"] = datetime.now().day
                    data["year"] = datetime.now().year
                    data["datetime"] = date(data["year"], data["month"], data["day"])
                else:
                    data_split = data["date"].split(" ")
                    if len(data_split) == 2:
                        data["day"] = int(data_split[1])
                        data["month"] = self.dict_month[data_split[0]]
                        data["year"] = datetime.now().year
                        data["datetime"] = date(data["year"], data["month"], data["day"])
                    else:
                        data["day"] = int(data_split[1])
                        data["month"] = self.dict_month[data_split[0]]
                        data["year"] = int(data_split[2])
                        data["datetime"] = date(data["year"], data["month"], data["day"])
            except:
                pass

    def click_show_more_results(self):
        print('Click in show more results')
        self.logger.info('Click in show more results')
        try:
            show_more_button = self.driver.find_elements(
                By.XPATH, f"//button[@{self.default_search_attribute}='{self.xpath_show_more_button}']")
            show_more_button[0].click()
            time.sleep(self.timesleeplow)
            return ["success", f""]
        except Exception as error:
            return ["error", f"No button available. Msg: {error}"]

    def get_info_card(self):
        print('Getting info from cards')
        self.logger.info('Getting info from cards')
        search_result_elements = self.driver.find_elements(By.XPATH,
                f"//ol[@{self.default_search_attribute}='{self.xpath_cards}']/li")
        for element in search_result_elements:
            try:
                title = element.find_element(By.TAG_NAME, "h4").text
                description = element.find_elements(By.TAG_NAME, "p")[1].text
                pic_url = element.find_elements(By.TAG_NAME, "img")[0].get_attribute("src")
                pic_file_name = element.find_elements(By.TAG_NAME, "img")[0].get_attribute("srcset")
                pic_file_name = pic_file_name.split(' ')[0].split('/')[-1]
                date = element.find_elements(By.TAG_NAME, "span")[0].text
                self.list_data.append(
                    {"title": title,
                     "description": description,
                     "date": date,
                     "pic_url": pic_url,
                     "pic_file_name": pic_file_name,
                     "day": "",
                     "month": "",
                     "year": "",
                     "money_bool": False,
                     "count_search_phrase": 0
                }
                )
                print(f'Collected info from card: {self.list_data[-1]}')
                self.logger.info(f'Collected info from card: {self.list_data[-1]}')
            except Exception as error:
                msg = f'Error extracting info from card. Msg: {error}'
                print(msg)
                self.logger.error(msg)
        self.get_dates()
        self.get_money_bool()
        self.get_count_sf_title_description()
        return self.list_data

    def get_count_sf_title_description(self):
        print('Counting search phrases in title or description')
        self.logger.info('Counting search phrases in title or description')
        for data in self.list_data:
            try:
                data["count_search_phrase"] = \
                    len(re.findall(fr"\b{self.search_phrase.lower()}\b", data["description"].lower())) + \
                    len(re.findall(fr"\b{self.search_phrase.lower()}\b", data["title"].lower()))
            except:
                pass

    def get_money_bool(self):
        '''
        Possible formats:
        $11.1 | $111,111.11 | 11 dollars | 11 USD"
        :return:
        '''
        print('Getting bool for money occurences in title and description')
        self.logger.info('Getting bool for money occurences in title and description')
        for data in self.list_data:
            try:
                if len(re.findall(fr"{self.regex_money_bool}", data["description"]))+ \
                        len(re.findall(fr"{self.regex_money_bool}", data["title"])) > 0:
                    data["money_bool"]=True
            except:
                pass

    def main(self):
        self.preparing_cards_to_extract()
        return self.get_info_card()