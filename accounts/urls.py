from . import views
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib import admin
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path
from accounts.views import (
    logout_view,
    register,
    edit_profile,
    ProfileView,
    ProfileOverview,
    deposit_view,
    withdraw_view,
    transaction_history_view,

)


app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name= 'accounts/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name= 'accounts/logout.html'), name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^overview/$', ProfileOverview.as_view(), name='overview_profile'),
    url(r'^profile/$', ProfileView.as_view(), name='view_profile'),
    url(r'^profile/edit$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^reset-password/$', PasswordResetView.as_view(template_name= 'accounts/reset_password.html',
                        email_template_name='accounts/reset_password_email.html',
                        success_url=reverse_lazy('accounts:password_reset_done')), name='reset_password'),
    url(r'^reset-password/done/$', PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'),
                                                                 name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,23})/$',
                                    PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html',
                                    success_url=reverse_lazy('accounts:password_reset_complete')),
                                    name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'),
                                                                        name='password_reset_complete'),
    url(r'^withdraw/$', views.withdraw_view, name='withdraw'),
    url(r'^deposit/$', views.deposit_view, name='deposit'),
    url(r'^history/$', views.transaction_history_view, name='transaction_history')

]