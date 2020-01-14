from django.shortcuts import redirect, render
from accounts.script.ExchangeRateScript import get_exchange_rates


def login_redirect(request):
    return redirect('/account/overview')


def home_view(request):
    result = get_exchange_rates()
    return render(request, 'home.html', context=result)
