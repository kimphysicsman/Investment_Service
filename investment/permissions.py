from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status

from investment.models import Investment as InvestmentModel


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAuthenticatedAndIsAuthor(BasePermission):
    """
    모든 메소드에 대해서 로그인한 고객 본인의 계좌만 인가
    """

    SAFE_METHODS = ()
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        investment_id = view.kwargs.get('id', None)

        if investment_id:
            try:
                investment_author = InvestmentModel.objects.get(id=investment_id).user
            
            except InvestmentModel.DoesNotExist:
                response ={
                        "detail": "투자(계좌)를 찾을 수 없습니다.",
                    }
                raise GenericAPIException(status_code=status.HTTP_404_NOT_FOUND, detail=response)
        else:
            investment_author = user

        if user.is_authenticated and user == investment_author:
            return True

        if request.method in self.SAFE_METHODS:
            return True
        
        return False