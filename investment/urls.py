from django.urls import path, include

from investment.views import (
    InvestmentView
)

# /investments
urlpatterns = [
    path('', InvestmentView.as_view())

]
