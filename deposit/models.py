from django.db import models

from user.models import User as UserModel
from investment.models import Investment as InvestmentModel

class Deposit(models.Model):
    """
        투자금 입금 내역
    """

    STATUS_CHOICES = (
        ("validate", "검증 상태"),
        ("complete", "입금 완료"),
        ("fail", "입금 실패"),
    )

    user = models.ForeignKey(UserModel, verbose_name="고객", on_delete=models.CASCADE)
    investment = models.ForeignKey(InvestmentModel, verbose_name="투자", on_delete=models.CASCADE)

    transfer_amount = models.PositiveBigIntegerField("거래금액")
    status = models.CharField("상태", max_length=128, choices=STATUS_CHOICES, default="validate")