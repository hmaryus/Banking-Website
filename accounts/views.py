from django.shortcuts import render, HttpResponseRedirect
from .models import UserProfile, Deposit, Withdraw
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    DepositForm,
    WithdrawForm,

)

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def transaction_history_view(request):
    deposits = Deposit.objects.filter(user=request.user)
    withdraws = Withdraw.objects.filter(user=request.user)

    deposits_history = [
        {"timestamp": entry.timestamp, "amount": entry.amount, "type": "Deposit"}
        for entry in deposits
    ]
    withdraws_history = [
        {"timestamp": entry.timestamp, "amount": -entry.amount, "type":"Withdraw"}
        for entry in withdraws
    ]

    all_history = sorted(deposits_history + withdraws_history, key=lambda x: x["timestamp"])

    args = {'user': request.user,
            'deposit': deposits,
            "withdraw": withdraws,
            "all_history": all_history
            }
    return render(request, "accounts/transactions_history.html", args)


class ProfileOverview(TemplateView):
        template_name = 'accounts/overview.html'

        def get(self, request):
            users = UserProfile.objects.filter(username=request.user.username).values()

            args = {'users': users}
            return render(request, self.template_name, args)


class ProfileView(TemplateView):
        template_name = 'accounts/profile.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['profile_image'] = self.request.user.profile_pic_url
            context['user'] = self.request.user
            return context


def withdraw_view(request):
        form = WithdrawForm(request.POST or None)

        if form.is_valid():
            withdraw = form.save(commit=False)
            withdraw.user = request.user

            # checks if user is trying to Withdraw more than his balance.
            if withdraw.user.account_balance >= withdraw.amount:
                # substracts users withdrawal from balance
                withdraw.user.account_balance -= withdraw.amount
                withdraw.user.save()
                withdraw.save()
                return HttpResponseRedirect(reverse('accounts:overview_profile'))

            else:
                messages.error(
                    request,
                    'You Can Not Withdraw More Than You Balance.'
                    )

        args = {"form": form}
        return render(request, "accounts/withdraw.html", args)


def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        # adds users deposit to balance.
        deposit.user.account_balance += deposit.amount
        deposit.user.save()
        deposit.save()
        return HttpResponseRedirect(reverse('accounts:overview_profile'))

    args = {"form": form}
    return render(request, "accounts/deposit.html", args)


def logout_view(request):
    return render(request, 'accounts/logout.html')


def register(request, *args, **kwargs):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    # else:
    #     form = RegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/reg_form.html', context)


@login_required()
def edit_profile(request):
    user = request.user
    form = EditProfileForm(request.POST or None, request.FILES, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            location = form.cleaned_data['location']
            card_nr = form.cleaned_data['card_nr']
            profile_pic = form.cleaned_data['profile_pic']
            #BANK ACCOUNT CREATION
            bank_id = 'RO' + (str(ord(first_name[0])) + str(ord(first_name[-1])))[-2:] + \
                            'BANK' + (str(ord(first_name[0])) + str(ord(first_name[-1])))[:3] + \
                            (str(ord(last_name[0])) + str(ord(last_name[-1])))[:3] + (card_nr[:3]) + (card_nr[-3:])
            #-------------------------

            user.bank_account = bank_id
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.phone_number = request.POST['phone_number']
            user.location = request.POST['location']
            user.card_nr = request.POST['card_nr']
            user.profile_pic = request.FILES['profile_pic'] if 'profile_pic' in request.FILES else user.profile_pic
            user.save()
            args = {'form': form, 'username': user.username}
            return HttpResponseRedirect(reverse('accounts:view_profile'), args)

    else:
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        phone_number = user.phone_number
        location = user.location
        card_nr = user.card_nr
        profile_pic = user.profile_pic
        form = EditProfileForm(initial={'first_name':first_name, 'last_name':last_name, 'email':email,
                                        'phone_number':phone_number, 'location':location, 'card_nr':card_nr,
                                        'profile_pic': profile_pic})
        args = {'form':form, 'username':user.username}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('accounts:view_profile'))
        else:
            args = {'form': form}
            return render(request, 'accounts/change_password.html', args)
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form':form}
        return render(request, 'accounts/change_password.html', args)