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

class DeleteWalletView(LoginRequiredMixin, View):
    def get(self, request, curr):
        wallet = Wallet.objects.get(currency=curr)
        wallet.delete()
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html",{"wallets": wallets})


"""
class UserLoginView(View):
    def get(self, request):
        #form = UserLoginForm()
        return render(request, 'login_view.html', locals())

    def post(self,request):
        #form = UserLoginForm(request.POST)
        if form.is_valid():
            u = authenticate(username=form.cleaned_data['username'],
                             password=form.cleaned_data['password'])
            if u is not None:
                login(request, u)
                return render(request, 'login_view.html', locals())
            else:
                return render(request, 'login_view.html', locals())

class AddWalletView(CreateView):
    model = Wallet
    fields = ("currency","amount")
    success_url = "/wallets"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddWalletView, self).form_valid(form)
"""
