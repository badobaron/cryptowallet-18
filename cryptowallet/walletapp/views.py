from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Wallet,TradeHistory,UserBalance


# Create your views here.

class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        balance_pln = UserBalance.objects.get(user=request.user).balance_pln
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html",{"wallets": wallets,"balance_pln" : balance_pln})

class AddWalletView(CreateView):
    model = Wallet
    fields = ("currency","amount","rate")
    success_url = "/wallets"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddWalletView, self).form_valid(form)

class ModifyWalletView(LoginRequiredMixin, View):
    def get(self, request, curr):
        wallet = Wallet.objects.get(currency=curr)
        return render(request, "wallet_modify.html", {"wallet": wallet})
    def post(self, request, curr):
        wallet = Wallet.objects.get(currency=curr)
        if "dodaj" in request.POST:
            wallet.amount += float(request.POST["amount"])
            wallet.save()
        else:
            wallet.amount -= float(request.POST["amount"])
            wallet.save()
        balance_pln = UserBalance.objects.get(user=request.user).balance_pln
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html", {"wallets": wallets, "balance_pln" : balance_pln})



class DeleteWalletView(LoginRequiredMixin, View):
    def get(self, request, curr):
        wallet = Wallet.objects.get(currency=curr)
        wallet.delete()
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html",{"wallets": wallets})

"""
class AddWalletView(CreateView):
    model = Wallet
    fields = ("currency","amount")
    success_url = "/wallets"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddWalletView, self).form_valid(form)
"""
