import pandas as pd

class ExportExcel:

    def __init__(self):
        self.df_output=pd.DataFrame()

    def export_excel_file(self, list_registers, filename):
        for key in list_registers[0].keys():
            self.df_output[key]=[d[key] for d in list_registers]
        self.df_output.to_excel(filename,index=False)