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
    """고객이 보유한 투자(계좌) 정보 리스트 반환 함수

    Args:
        user_obj (UserModel): 고객 오브젝트

    Returns:
        list: 투자(계좌) 정보 리스트
    """
    
    investment_obj_list = InvestmentModel.objects.filter(user=user_obj)

    return InvestmentViewSerializer(investment_obj_list, many=True).data


def get_investment_detail(id):
    """고객이 보유한 투자(계좌) 상세 정보 반환 함수

    Args:
        id (int): 투자(계좌) PK

    Returns:
        dict: 투자(계좌) 상세 정보
    """
    

    investment_obj = InvestmentModel.objects.get(id=id)

    return InvestmentDtailViewSerializer(investment_obj).data


def get_investment_stocks(investment_id):
    """고객이 보유한 해당 투자(계좌)에 포함된 종목

    Args:
        investment_id (int): 투자(계좌) PK

    Returns:
        list: 보유 종목 정보 리스트
    """

    stock_obj_list = InvestmentStockModel.objects.filter(investment_id=investment_id)

    return InvestmentStockViewSerializer(stock_obj_list, many=True).data