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


class InvestmentDtailViewSerializer(serializers.ModelSerializer):
    """
        투자 상세 조회 Serializer
    """

    bank = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    income_percent = serializers.SerializerMethodField()


    def get_bank(self, obj):
        return obj.bank.name

    def get_total_income(self, obj):
        return obj.total_asset - obj.starting_fund

    def get_income_percent(self, obj):
        return (obj.total_asset - obj.starting_fund) * 100

    
    class Meta:
        model = InvestmentModel
        fields = [
            "id", "account_name", "bank", "account_num", 
            "total_asset", "starting_fund",
            "total_income", "income_percent"
        ]

        
class InvestmentViewSerializer(InvestmentDtailViewSerializer):
    """
        투자 조회 Serializer
    """

    class Meta:
        model = InvestmentModel
        fields = [
            "id", "account_name", "bank", "account_num", 
            "total_asset"
        ]

class InvestmentStockViewSerializer(InvestmentDtailViewSerializer):
    """
        보유 종목 조회 Serializer
    """
    stock = serializers.SerializerMethodField()
    asset_group = serializers.SerializerMethodField()
    assessment_value = serializers.SerializerMethodField()
    isin = serializers.SerializerMethodField()

    def get_stock(self, obj):
        return obj.stock.name

    def get_asset_group(self, obj):
        return obj.stock.asset_group.name

    def get_assessment_value(self, obj):
        return obj.order * obj.current_price

    def get_isin(self, obj):
        return obj.stock.isin

    class Meta:
        model = InvestmentStockModel
        fields = [
            "id", "stock", "asset_group", "assessment_value", "isin"
        ]