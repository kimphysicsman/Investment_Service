from investment.serializers import (
    InvestmentDtailViewSerializer,
    InvestmentViewSerializer,
    InvestmentStockViewSerializer
)

from investment.models import (
    Investment as InvestmentModel,
    InvestmentStock as InvestmentStockModel
)


def get_investments(user_obj):
    
    investment_obj_list = InvestmentModel.objects.filter(user=user_obj)

    return InvestmentViewSerializer(investment_obj_list, many=True).data


def get_investment_detail(id):

    investment_obj = InvestmentModel.objects.get(id=id)

    return InvestmentDtailViewSerializer(investment_obj).data


def get_investment_stocks(investment_id):

    stock_obj_list = InvestmentStockModel.objects.filter(investment_id=investment_id)

    return InvestmentStockViewSerializer(stock_obj_list, many=True).data