from rest_framework import serializers

from investment.models import (
    Bank as BankModel,
    Investment as InvestmentModel,
    AssetGroup as AssetGroupModel,
    Stock as StockModel,
    InvestmentStock as InvestmentStockModel
)


class BankModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankModel
        fields = "__all__"

class AssetGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroupModel
        fields = "__all__"

class InvestmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentModel
        fields = "__all__"

        read_only_fields = ["starting_fund", "total_asset"]

class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockModel
        fields = "__all__"

class InvestmentStockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentStockModel
        fields = "__all__"