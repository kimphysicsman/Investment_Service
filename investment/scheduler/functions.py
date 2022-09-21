import pandas as pd
import os

from investment.services.model_service import (
    set_stock
)

BASE_PATH = os.getcwd()
DATA_PATH = BASE_PATH + '\investment\scheduler\data'

def set_aaset_group_info():
    data_path = DATA_PATH +"\\asset_group_info_set.xlsx"
    stocks = pd.read_excel(data_path)
    
    for stock in stocks.iloc:
        set_stock(stock["종목명"], stock["ISIN"], stock["자산그룹"])
        
