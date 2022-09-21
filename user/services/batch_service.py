import os

from user.serializers import UserModelSerializer
from user.models import User as UserModel

def create_user(username):
    password = os.environ.get("USER_PASSWORD_DEFAULT", "0000")
    print(password)

    data = {
        "username": username,
        "password": password
    }

    serailizer = UserModelSerializer(data=data)
    serailizer.is_valid(raise_exception=True)
    serailizer.save()

    return serailizer.instance


def get_user(username):
    try:
        user_obj = UserModel.objects.get(username=username)
    except:
        return create_user(username)

    return user_obj