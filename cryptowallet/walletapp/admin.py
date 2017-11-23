from django.contrib import admin
from .models import UserBalance,Wallet
# Register your models here.

@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    pass

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass
