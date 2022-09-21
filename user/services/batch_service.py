import os

from user.serializers import UserModelSerializer
from user.models import User as UserModel

def create_user(username):
    """고객 오브젝트 생성 함수

    Args:
        username (str): 고객명

    Returns:
        UserModel: 생성된 고객 오브젝트
    """

    password = os.environ.get("USER_PASSWORD_DEFAULT", "0000")

    data = {
        "username": username,
        "password": password
    }

    serailizer = UserModelSerializer(data=data)
    serailizer.is_valid(raise_exception=True)
    serailizer.save()

    return serailizer.instance


def get_user(username):
    """고객 오브젝트 반환 함수
       DB에 없을 시 오브젝트 생성
    
    Args:
        username (str): 고객명

    Returns:
        UserModel: 고객 오브젝트
    """

    try:
        user_obj = UserModel.objects.get(username=username)
    except:
        return create_user(username)

    return user_obj