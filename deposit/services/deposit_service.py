from django.contrib.auth.hashers import make_password, check_password

from investment.models import (
    Investment as InvestmentModel,
    InvestmentStock as InvestmentStockModel,
)
from investment.services.batch_service import (
    create_investment_stock,
    set_stock
)
from deposit.serializer import DepositModelSerializer
from deposit.models import Deposit as DepositModel


def create_deposit(user_obj, account_number, transfer_amount):

    investment_obj = InvestmentModel.objects.get(account_num=account_number)
    
    data = {
        "user": user_obj.id,
        "investment": investment_obj.id,
        "transfer_amount": transfer_amount,
        "status": "validate"
    }

    serializer = DepositModelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.instance

def get_deposit(deposit_id):
    deposit_obj = DepositModel.objects.get(id=deposit_id)

    return deposit_obj


def get_deposit_str(deposit_obj):

    return (
        str(deposit_obj.investment.account_num) 
        + str(deposit_obj.user.username) 
        + str(deposit_obj.transfer_amount)
        )


def get_deposit_hashed(deposit_data_str):
    
    deposit_data_hashed = make_password(deposit_data_str)

    return deposit_data_hashed


def validate_deposit(hashed_data, deposit_obj):
    raw_data = get_deposit_str(deposit_obj)
    
    return check_password(raw_data, hashed_data)


def complete_deposit(deposit_obj):
        investment_obj = deposit_obj.investment

        # 총 자산 업데이트
        investment_obj.total_asset += deposit_obj.transfer_amount
        investment_obj.save()

        # 보유 현금 종목 업데이트
        try:
            investment_stock_obj = InvestmentStockModel.objects.get(investment=investment_obj, stock__isin="CASH")
        except:
            stock_obj = set_stock("CASH")
            investment_stock_obj = create_investment_stock(investment_obj, stock_obj, 0, 1)
            investment_stock_obj.save()

        investment_stock_obj.current_price += deposit_obj.transfer_amount
        investment_stock_obj.save()

        # 입금 상태 업데이트
        deposit_obj.status = "complete"
        deposit_obj.save()


def fail_deposit(deposit_obj):
    deposit_obj.status = "fail"
    deposit_obj.save()