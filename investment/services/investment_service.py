from investment.serializers import (
    AssetGroupModelSerializer,
    StockModelSerializer,
    InvestmentModelSerializer,
    BankModelSerializer,
    InvestmentStockModelSerializer
)

from investment.models import (
    AssetGroup as AssetGroupModel,
    Stock as StockModel,
    Investment as InvestmentModel,
    Bank as BankModel,
    InvestmentStock as InvestmentStockModel
)


def get_investments(user_obj):
    
    investment_obj_list = InvestmentModel.objects.filter(user=user_obj)

    return InvestmentModelSerializer(investment_obj_list, many=True).data
