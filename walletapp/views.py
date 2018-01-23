from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .models import Wallet,TradeHistory,UserBalance
from .forms import SignUpForm


# Create your views here.

class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        balance_pln = UserBalance.objects.get(user=request.user).balance_pln
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html",{"wallets": wallets,"balance_pln" : balance_pln})

class AddWalletView(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ("currency","amount","rate")
    success_url = "/wallets"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddWalletView, self).form_valid(form)

class ModifyWalletView(LoginRequiredMixin, View):
    def get(self, request, curr):
        balance_pln = UserBalance.objects.get(user=request.user).balance_pln
        wallet = Wallet.objects.get(currency=curr, user=request.user)
        return render(request, "wallet_modify.html", {"wallet": wallet, "balance_pln" : balance_pln})
    def post(self, request, curr):
        wallet = Wallet.objects.get(currency=curr, user=request.user)

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
        wallet = Wallet.objects.get(currency=curr, user=request.user)
        wallet.delete()
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html",{"wallets": wallets})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserBalance.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('wallets')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class AddPlnView(LoginRequiredMixin, View):
    def get(self, request):
        balance_pln = UserBalance.objects.get(user=request.user).balance_pln
        return render(request, "balance_pln.html", {"balance_pln": balance_pln})
    def post(self, request):
        user_balance = UserBalance.objects.get(user=request.user)
        if "dodaj" in request.POST:
            user_balance.balance_pln += float(request.POST["amount"])
            user_balance.save()

        else:
            user_balance.balance_pln -= float(request.POST["amount"])
            user_balance.save()
        wallets = Wallet.objects.filter(user=request.user)
        return render(request, "wallet_view.html", {"wallets": wallets, "balance_pln": user_balance.balance_pln})


"""
class AddWalletView(CreateView):
    model = Wallet
    fields = ("currency","amount")
    success_url = "/wallets"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(AddWalletView, self).form_valid(form)
"""
