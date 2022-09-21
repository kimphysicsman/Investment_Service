import pandas as pd
import os

from user.services.batch_service import get_user

from investment.services.batch_service import (
    set_stock,
    get_investment,
    set_investment_stock
)

BASE_PATH = os.getcwd()
DATA_PATH = BASE_PATH + '\investment\scheduler\data'

def set_aaset_group_info():
    """자산그룹 및 종목 정보 셋팅 함수 
    """

    data_path = DATA_PATH + "\\asset_group_info_set.xlsx"
    stocks = pd.read_excel(data_path)
    
    for stock in stocks.iloc:
        try:
            set_stock(stock["ISIN"], stock["종목명"], stock["자산그룹"])
        except:
            continue

def set_investment_info():
    """투자 정보 셋팅 함수
    """

    data_path = DATA_PATH + "\\account_asset_info_set.xlsx"
    df = pd.read_excel(data_path)

    users = list(set(df["고객이름"]))
    for user in users:
        if not user:
            continue

        try:
            user_obj = get_user(user)
        except:
            continue
        
        user_df = df[ df["고객이름"]==user ]

        investments = list(set(user_df["계좌번호"]))
        for investment in investments:
            if not investment:
                continue

            investment_df = user_df[ user_df["계좌번호"] == investment ]

            bank_name = investment_df["증권사"].iloc[0]
            account_name = investment_df["계좌명"].iloc[0]
            account_num = investment_df["계좌번호"].iloc[0]

            if not (bank_name and account_name and account_num):
                continue
            
            try:
                investment_obj = get_investment(user_obj, account_name, account_num, bank_name)
            except:
                continue

            for investmentstock in investment_df.iloc:
                isin = investmentstock["ISIN"]
                order = investmentstock["보유수량"]
                current_price = investmentstock["현재가"]

                if not (isin and order and current_price):
                    continue

                stock_obj = set_stock(isin=isin)

                try:
                    set_investment_stock(investment_obj, stock_obj, current_price, order)
                except:
                    continue