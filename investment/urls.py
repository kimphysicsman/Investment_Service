from django.urls import path

from investment.views import (
    InvestmentView,
    InvestmentDetailView,
    StockView,
)


urlpatterns = [
    # /investments
    path('', InvestmentView.as_view()),
    path('/<int:id>', InvestmentDetailView.as_view()),
    path('/<int:id>/stocks', StockView.as_view()),
]

