import pandas as pd
from datetime import datetime, date
from configparser import RawConfigParser
from dateutil.relativedelta import relativedelta
import os
class ExportExcel:

    def __init__(self):
        self.df_output = pd.DataFrame()
        self.config = RawConfigParser()
        self.path_config = os.path.join(os.path.abspath(os.path.join(os.getcwd(),
                                                                     os.pardir)), 'config')
        self.config.read(os.path.join(self.path_config, 'config.ini'), encoding='utf-8')
        self.number_months = self.config['input_parameters']['number_months']
        self.number_months = int(self.number_months)
    def get_month_date_criteria(self):
        if self.number_months == 0 or self.number_months == 1:
            return date(datetime.now().year, datetime.now().month, 1)
        else:
            return date(datetime.now().year, datetime.now().month, 1)-relativedelta(months=
                                                         self.number_months-1)
    def export_excel_file(self, list_registers, filename):
        for key in list_registers[0].keys():
            self.df_output[key] = [d[key] for d in list_registers]
        self.df_output['datetime'] = pd.to_datetime(self.df_output['datetime'], format='%Y-%m-%d')
        date_criteria = self.get_month_date_criteria()
        filtered_df = self.df_output.loc[self.df_output['datetime'] >= f'{date_criteria.year}-' \
                                                                   f'{date_criteria.month}-' \
                                                                   f'{date_criteria.day}']
        filtered_df = filtered_df.drop_duplicates()
        filtered_df.to_excel(filename, index=False, sheet_name="data_collected")