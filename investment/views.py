from rest_framework import status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from investment.permissions import IsAuthenticatedAndIsAuthor
from investment.services.investment_service import (
    get_investments,
    get_investment_detail,
    get_investment_stocks,
)


# 투자(계좌) 조회 기능
class InvestmentView(APIView):
    permission_classes = [IsAuthenticatedAndIsAuthor]

    # 투자(계좌) 조회
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        investments_info =  get_investments(user)

        if len(investments_info) == 0:
            return Response({"detail": "투자(계좌)가 존재하지않습니다. "}, status=status.HTTP_404_NOT_FOUND)

        return Response(investments_info, status=status.HTTP_200_OK)


# 투자(계좌) 상세 조회 기능
class InvestmentDetailView(APIView):
    permission_classes = [IsAuthenticatedAndIsAuthor]

    # 투자(계좌) 상세 조회
    def get(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        investments_info =  get_investment_detail(id)

        if len(investments_info) == 0:
            return Response({"detail": "투자(계좌)가 존재하지않습니다. "}, status=status.HTTP_404_NOT_FOUND)

        return Response(investments_info, status=status.HTTP_200_OK)



# 보유 종목 조회 기능
class StockView(APIView):
    permission_classes = [IsAuthenticatedAndIsAuthor]

    # 해당 투자의 보유 종목 조회
    def get(self, request, id):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        stocks_info = get_investment_stocks(id)

        if len(stocks_info) == 0:
            return Response({"detail": "보유 종목이 존재하지않습니다. "}, status=status.HTTP_404_NOT_FOUND)

        return Response(stocks_info, status=status.HTTP_200_OK)

