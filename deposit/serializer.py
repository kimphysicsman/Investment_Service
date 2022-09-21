from dataclasses import field
from rest_framework import serializers

from deposit.models import Deposit as DepositModel

class DepositModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositModel
        fields = "__all__"