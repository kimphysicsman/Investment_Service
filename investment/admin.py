from django.contrib import admin

from investment.models import (
    Bank as BankModel,
    Investment as InvestmentModel,
    AssetGroup as AssetGroupModel,
    Stock as StockModel,
    InvestmentStock as InvestmentStockModel
)

admin.site.register(BankModel)
admin.site.register(InvestmentModel)
admin.site.register(AssetGroupModel)
admin.site.register(StockModel)
admin.site.register(InvestmentStockModel)