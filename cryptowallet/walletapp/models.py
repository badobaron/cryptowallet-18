from django.db import models
from django.contrib.auth.models import User

# Create your models here.
currencies = (
    ("BTC","BTC"),
    ("BCH","BCH"),
    ("LTC","LTC"),
    ("LSK","LSK"),
    ("ETH","ETH"),
    ("DASH","DASH"),
    ("NEO", "NEO"))

class Wallet(models.Model):
    class Meta:
        unique_together=("currency","user")
    currency = models.CharField(max_length=4, choices=currencies)
    amount = models.FloatField(null=True)
    rate = models.FloatField(null=True)
    amount_pln = models.FloatField(null=True)               #powiązać ze stanem PLN i TradeHistory
    user = models.ForeignKey(User)
    def __str__(self):
        return self.name

class TradeHistory(models.Model):
    currency = models.CharField(max_length=4, choices=currencies)
    rate = models.FloatField()
    amount = models.FloatField(null=True)
    amount_pln = models.FloatField(null=True)
    timestamp = models.DateTimeField()
    wallet = models.ForeignKey(Wallet)

class UserBalance(models.Model):
    user = models.OneToOneField(User)
    balance_pln = models.FloatField(null=True, default=0.00)
