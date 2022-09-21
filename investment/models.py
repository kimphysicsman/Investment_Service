from django.db import models
from django.core.validators import RegexValidator

from user.models import User as UserModel


class Bank(models.Model):
    """
        증권사 오브젝트        
    """
    name = models.CharField("증권사명", max_length=128)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Investment(models.Model):
    """
        투자(계좌) 오브젝트
    """

    account_num_validator = RegexValidator(regex = r'^\d+$')

    user = models.ForeignKey(UserModel, verbose_name="고객", on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, verbose_name="증권사", on_delete=models.CASCADE)

    account_name = models.CharField("계좌명", max_length=128)
    account_num = models.CharField("계좌번호", max_length=13, validators=[account_num_validator],  unique=True)

    starting_fund = models.PositiveBigIntegerField("투자원금")
    total_asset = models.PositiveBigIntegerField("계좌총자산")

    def __str__(self):
        return f"{self.id} - {self.user.username}'s investment"


class AssetGroup(models.Model):
    """
        자산그륩 오브젝트
    """

    name = models.CharField("자산그륩명", max_length=128, unique=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Stock(models.Model):
    """
        종목 오브젝트
    """

    asset_group = models.ForeignKey(AssetGroup, verbose_name="자산그륩", on_delete=models.CASCADE)

    name = models.CharField("종목명", max_length=128,  unique=True)
    isin = models.CharField("ISIN", max_length=128, unique=True)
    
    insvestment = models.ManyToManyField(Investment, verbose_name="보유종목", related_name="stock", through="InvestmentStock")

    def __str__(self):
        return f"{self.id} - {self.name}"


class InvestmentStock(models.Model):
    investment = models.ForeignKey(Investment, verbose_name="투자", on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, verbose_name="보유종목", on_delete=models.CASCADE)

    order = models.PositiveIntegerField("보유수량")
    current_price = models.PositiveIntegerField("현재가")