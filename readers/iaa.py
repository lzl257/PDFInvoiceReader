import os
import re
import pandas as pd
from .reader import PDFReader

from IPython.display import clear_output


class IAAInvReader(PDFReader):
    
    def __init__(self, upload_widget):
        super().__init__(upload_widget=upload_widget)
        
        
    def __reg_basic(self, str_content):
        return re.findall('Page:\\n\\n(.*?)\\n(.*?)\\n(.*?)\n1', str_content)
    
    
    def __reg_weight(self, str_content):
        return re.findall('Chargeable\ weight\\n(.*?)\\n', str_content)
    
    
    def __reg_total(self, str_content):
        return re.findall('Total\ amount\ due\\n\\n(.*?)\\n', str_content)

    
    def get_info(self):
        # First read the uploaded files.
        super().upload()
        
        info_list = []
        for pdf in os.listdir(self.temp_dir):
            if pdf.endswith(".pdf"):
                os.system(f"pdf2txt.py -o {pdf[:-4]}.txt -t text  {self.temp_dir}/{pdf}")
                with open(f"{pdf[:-4]}.txt", 'r') as text:
                    print(f"Rechnung {pdf[:-4]}")
                    text_str = text.read()
                    if not "International Airfreight Associates B.V." in text_str:
                        print(f"The invoice {pdf[:-4]} does not belong to IAA!")
                        info_list.append(pd.DataFrame(columns=["Invoice number", "Invoice date", "Invoice due date",
                                                  "Chargeable weight", "Total amount due"]))
                    
                    cap_basic = self.__reg_basic(text_str)
                    cap_weight = self.__reg_weight(text_str)
                    cap_total = self.__reg_total(text_str)

                    cap_dict = {"Basic info": cap_basic, "Weight info": cap_weight, "Credit info": cap_total}

                    df_dict = {}
                    for key, cap_content in cap_dict.items():                
                        if len(cap_content) != 0:
                            cap_value = cap_content[0]
                            if key == "Basic info":
                                df_dict["Invoice number"] = cap_value[0]
                                df_dict["Invoice date"] = cap_value[1]
                                df_dict["Invoice due date"] =  cap_value[2]
                            elif key == "Weight info":
                                df_dict["Chargeable weight"] = cap_value
                            else:
                                df_dict["Total amount due"] = cap_value
                        else:
                            print(f"Capturing {key} failed. Please re-check!")

                info_list.append(pd.DataFrame(df_dict, index=[0]))

        info = pd.concat(info_list).dropna().reset_index(drop=True)
        
        return info