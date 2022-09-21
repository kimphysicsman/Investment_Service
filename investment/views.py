from rest_framework import status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from investment.permissions import IsAuthenticated
from investment.services.investment_service import (
    get_investments
)


# 투자(계좌) 조회 기능
class InvestmentView(APIView):
    permission_classes = [IsAuthenticated]

    # 투자(계좌) 조회
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        investments_info =  get_investments(user)

        if len(investments_info) == 0:
            return Response({"detail": "투자(계좌)가 존재하지않습니다. "}, status=status.HTTP_404_NOT_FOUND)

        return Response(investments_info, status=status.HTTP_200_OK)