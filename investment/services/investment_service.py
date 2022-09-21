from investment.serializers import (
    InvestmentDtailViewSerializer,
    InvestmentViewSerializer
)

from investment.models import (
    Investment as InvestmentModel,
)


def get_investments(user_obj):
    
    investment_obj_list = InvestmentModel.objects.filter(user=user_obj)

    return InvestmentViewSerializer(investment_obj_list, many=True).data


def get_investment_detail(id):

    investment_obj = InvestmentModel.objects.get(id=id)

    return InvestmentDtailViewSerializer(investment_obj).data
