from django.urls import path, include

from investment.views import (
    InvestmentView,
    InvestmentDetailView,
    StockView,
)

# /investments
urlpatterns = [
    path('', InvestmentView.as_view()),
    path('/<int:id>', InvestmentDetailView.as_view()),
    path('/<int:id>/stocks', StockView.as_view()),
]
