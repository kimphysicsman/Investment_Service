from rest_framework import serializers

from user.models import User as UserModel

class UserModelSerializer(serializers.ModelSerializer):
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user


    class Meta:
        model = UserModel
        fields = "__all__"

        extra_kwargs = {
            'password': {'write_only': True}
        }
