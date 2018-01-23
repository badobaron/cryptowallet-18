"""cryptowallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from walletapp.views import WalletView, AddWalletView, ModifyWalletView, DeleteWalletView, signup, AddPlnView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wallets', WalletView.as_view(), name="wallets"),
    url(r'^add_wallet', AddWalletView.as_view(), name="add-wallet"),
    url(r'^modify/(?P<curr>([a-zA-Z0-9])+)', ModifyWalletView.as_view(), name="modify-wallet"),
    url(r'^delete/(?P<curr>([a-zA-Z0-9])+)', DeleteWalletView.as_view(), name="delete-wallet"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^add_pln/', AddPlnView.as_view(), name="add-pln"),
]
