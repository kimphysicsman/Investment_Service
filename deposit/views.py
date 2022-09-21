from django.db import transaction

from rest_framework import status, exceptions, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from deposit.services.deposit_service import (
    create_deposit,
    get_deposit,
    get_deposit_str,
    get_deposit_hashed,
    validate_deposit,
    complete_deposit,
    fail_deposit,
)

from investment.services.batch_service import get_investment_simple

# 투자금 입금 View
class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # 투자금 입금 등록
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        account_number = request.data.get("account_number", None)
        user_name = request.data.get("user_name", None)
        transfer_amount = request.data.get("transfer_amount", None)

        if user.username != user_name:
            return Response({"detail": "입력 데이터를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            investment_obj = get_investment_simple(account_number)
        except:
            return Response({"detail": "투자(계좌)를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        if user != investment_obj.user:
            return Response({"detail": "입력 데이터를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            deposit_obj = create_deposit(user, account_number, transfer_amount)
        except:
            return Response({"detail": "입력 데이터를 확인해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # # 응답 데이터에 hash된 값 포함 시 사용
        # deposit_str = get_deposit_str(deposit_obj)
        # deposit_hashed = get_deposit_hashed(deposit_str)

        # return Response({
        #     "transfer_identifier": deposit_obj.id,
        #     "hashed_data" : deposit_hashed
        # }, status=status.HTTP_200_OK)

        return Response({ "transfer_identifier": deposit_obj.id }, status=status.HTTP_200_OK)

    
    # 투자금 입금 검증
    @transaction.atomic
    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "서비스를 이용하기 위해 로그인 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        deposit_id = request.data.get("transfer_identifier", None)

        if deposit_id:
            try:
                deposit_obj = get_deposit(deposit_id)
            except:
                return Response({"detail": "입금 내역을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        else :
            return Response({"detail": "입금 내역 식별자를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        if deposit_obj.status != "validate":
            return Response({"detail": "입금 내역 수정할 수 없습니다."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        hashed_data = request.data.get("signature", None)

        if not hashed_data:
            return Response({"detail": "hash 데이터를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            
        result = validate_deposit(hashed_data, deposit_obj)
        
        if result:
            try:
                with transaction.atomic():
                    complete_deposit(deposit_obj)
                    return Response({"status": result}, status=status.HTTP_200_OK)
            except:
                fail_deposit(deposit_obj)
        else:
            fail_deposit(deposit_obj)
        
        return Response({"status": result}, status=status.HTTP_409_CONFLICT)
